def hard_match(resume_text, job_description_text):
    """Performs a hard match based on skills."""
    # This is a simplified example. In a real system, you'd
    # use a more robust way to identify skills from the JD.
    # For now, let's assume the JD lists "required skills"
    # in a structured way, or you can manually define them.

    # Example: List of skills to look for.
    required_skills = ['Python', 'SQL', 'machine learning', 'data analysis', 'Docker']
    
    found_skills = []
    missing_skills = []
    
    # Normalize the text for better matching (lowercase)
    resume_text_lower = resume_text.lower()
    
    for skill in required_skills:
        if skill.lower() in resume_text_lower:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
            
    # Calculate a score based on the number of skills found
    score = (len(found_skills) / len(required_skills)) * 50  # Let's say hard match is 50% of the total score
    
    return score, found_skills, missing_skills