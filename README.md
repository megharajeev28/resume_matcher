Automated Resume Relevance Check System

Project Overview
This is an AI-powered application designed to automate and streamline the process of matching resumes to job descriptions. The system analyzes a candidate's resume against a specific job description, providing a detailed relevance score and a breakdown of their skills.

The application combines two core matching methods:

Hard Matching: Identifies and scores the presence of specific keywords and key skills.

Semantic Matching: Uses the Gemini AI to perform a deeper, contextual analysis, understanding the relevance of projects, experience, and soft skills to the job description.

The final relevance score is a weighted combination of these two methods, providing a balanced and accurate assessment.

Features
AI-Powered Relevance Scoring: Utilizes the Gemini API for nuanced semantic analysis.

Dynamic UI: The Streamlit-based web interface provides a clean, user-friendly experience with a dynamic theme.

Conditional Feedback: The application provides instant visual feedback with a progress bar and a final score that is color-coded based on relevance (Green for high, Yellow for medium, and Red for low).

Missing Skills Identification: Clearly lists the key skills from the job description that were not found in the resume.

Secure API Key Management: Uses python-dotenv to securely manage API keys, which is a best practice for development and deployment.

Support for Multiple File Types: Accepts resumes and job descriptions in PDF, DOCX, and TXT formats.

Installation and Setup
Follow these steps to get the application up and running on your local machine.

1. Clone the Repository
First, clone this repository to your local machine:

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies:

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

3. Install Dependencies
Install all the required Python libraries using pip:

pip install streamlit python-dotenv requests openai

4. Set Up Your API Key
Create a file named .env in the root of your project directory. Add your OpenAI API key to this file as follows:

OPENAI_API_KEY="YOUR_API_KEY_HERE"

Note: Replace "YOUR_API_KEY_HERE" with your actual API key. The .gitignore file is configured to prevent this file from being pushed to your GitHub repository.

5. Run the Application
With all the prerequisites in place, you can now run the Streamlit application from your terminal:

streamlit run app.py

This will launch the application in your web browser.

Usage
Upload Files: Use the "Browse files" buttons to upload a resume and a job description (in PDF, DOCX, or TXT format).

Analyze: Click the Check Relevance button.

Review Results: The application will display a final relevance score, an overall verdict (High, Medium, or Low), and a list of any key skills that were not found.
