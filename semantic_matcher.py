import openai

def semantic_match_with_llm(resume_text, job_description_text):
    """Uses an LLM to assess semantic fit."""
    prompt = f"""
    You are an expert resume reviewer. Your task is to compare a candidate's resume with a job description.
    
    Analyze the following resume and job description and provide a score from 0-100 on how well the candidate's experience and skills align with the role's requirements. Also, provide a brief explanation.
    
    ---
    Job Description:
    {job_description_text[:2000]} # Truncate to save tokens and cost
    
    ---
    Resume:
    {resume_text[:2000]} # Truncate to save tokens and cost
    
    ---
    
    Provide the output in the following JSON format:
    {{
        "semantic_score": <score_number_0_to_100>,
        "explanation": "<brief_explanation_of_the_fit>"
    }}
    """
    
    try:
        # We'll use a simple completion model for this MVP
        response = openai.chat.completions.create(
            model="gpt-4-turbo",  # Or "gpt-3.5-turbo" for lower cost/speed
            messages=[
                {"role": "system", "content": "You are a helpful and accurate resume analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        import json
        result = json.loads(response.choices[0].message.content)
        
        return result['semantic_score'], result['explanation']
        
    except Exception as e:
        print(f"Error with LLM semantic match: {e}")
        return 0, "Could not perform semantic analysis."