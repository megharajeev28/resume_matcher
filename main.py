import os
import json
import requests
import re
from dotenv import load_dotenv
from parser import get_text_from_file
from hard_matcher import hard_match

# Load environment variables from .env file
load_dotenv()

def extract_qualifications(jd_text):
    """
    Extracts qualifications from the job description text using regex.
    """
    qualifications_match = re.search(r'Qualifications:(.*)', jd_text, re.DOTALL)
    if qualifications_match:
        qualifications_text = qualifications_match.group(1).strip()
        # Split by new line, remove empty lines, and strip whitespace
        qualifications = [q.strip() for q in qualifications_text.split('\n') if q.strip()]
        return qualifications
    return []

def semantic_match_with_llm(resume_text, jd_text):
    """
    Uses a Large Language Model to semantically match resume content to a job description.
    The LLM is prompted to return a structured JSON object for reliable parsing.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        return 0, "API key not found."
    
    # Extract qualifications from the JD
    qualifications = extract_qualifications(jd_text)
    if not qualifications:
        return 0, "Could not extract qualifications from job description."

    qualifications_list = "\\n".join(qualifications)

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    prompt = f"""
    You are a professional resume analysis tool. Your task is to analyze a resume against a job description.

    Here is the job description:
    ---
    {jd_text}
    ---

    Here is the resume:
    ---
    {resume_text}
    ---

    Analyze the resume and generate a relevance score from 0 to 100 for each of the following qualifications. Provide a brief reasoning for each score.
    
    Qualifications to assess:
    {qualifications_list}

    Respond with a JSON object. Do not include any text before or after the JSON.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "qualificationScores": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "qualification": {"type": "STRING"},
                                "score": {"type": "INTEGER", "description": "The relevance score from 0-100."},
                                "reasoning": {"type": "STRING", "description": "A brief explanation for the score."}
                            }
                        }
                    }
                }
            }
        }
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes
        
        result = response.json()
        
        # Check if the result has the expected structure
        if "candidates" in result and len(result["candidates"]) > 0:
            content_part = result["candidates"][0].get("content", {}).get("parts", [{}])[0]
            if content_part and "text" in content_part:
                json_string = content_part["text"]
                llm_data = json.loads(json_string)
                
                qualification_scores = llm_data.get("qualificationScores", [])
                
                if not qualification_scores:
                    return 0, "LLM returned no qualification scores."
                    
                total_score = sum(item["score"] for item in qualification_scores)
                average_score = total_score / len(qualification_scores)
                
                reasoning = "Based on scores for individual qualifications."
                return int(average_score), reasoning
            else:
                return 0, "Unexpected API response structure."
        else:
            return 0, "No candidates found in API response."
            
    except requests.exceptions.RequestException as e:
        return 0, f"API request failed: {e}"
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        return 0, f"Failed to parse JSON response: {e}"


def generate_relevance_score(resume_path, jd_path):
    """Combines hard and soft matches to generate a final score and verdict."""
    
    # 1. Parse documents
    resume_text = get_text_from_file(resume_path)
    jd_text = get_text_from_file(jd_path)
    
    if not resume_text or not jd_text:
        return 0, "Low", ["Error: Could not read files."]
    
    # 2. Hard Match
    hard_score, found_skills, missing_skills = hard_match(resume_text, jd_path)
    
    # Check if all key skills are found. If so, return a perfect score.
    if not missing_skills:
        return 100, "High", missing_skills
    
    # 3. Semantic Match
    semantic_score, _ = semantic_match_with_llm(resume_text, jd_path)
    
    # 4. Final Weighted Score
    final_score = (hard_score * 0.7) + (semantic_score * 0.3)
    
    # 5. Verdict Logic
    if final_score >= 80:
        verdict = "High"
    elif final_score >= 50:
        verdict = "Medium"
    else:
        verdict = "Low"
        
    return int(final_score), verdict, missing_skills
