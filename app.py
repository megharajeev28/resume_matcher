import streamlit as st
import tempfile
import os
from main import generate_relevance_score

# Set page title and favicon
st.set_page_config(
    page_title="Resume Relevance System",
    page_icon="📄",
    layout="wide"
)

# Title and introduction
st.title("Automated Resume Relevance Check System")
st.markdown("Upload a resume and a job description to get a relevance score and personalized feedback.")

# File uploaders
st.subheader("Upload Resume (PDF/DOCX/TXT):")
resume_file = st.file_uploader("Drag and drop resume here", type=["pdf", "docx", "txt"], key="resume_uploader")

st.subheader("Upload Job Description (PDF/DOCX/TXT):")
jd_file = st.file_uploader("Drag and drop job description here", type=["pdf", "docx", "txt"], key="jd_uploader")

# Check Relevance button
if st.button("Check Relevance", use_container_width=True):
    if resume_file and jd_file:
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.name)[1]) as temp_resume:
            temp_resume.write(resume_file.read())
            temp_resume_path = temp_resume.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(jd_file.name)[1]) as temp_jd:
            temp_jd.write(jd_file.read())
            temp_jd_path = temp_jd.name

        try:
            # Generate scores and skills
            final_score, verdict, missing_skills = generate_relevance_score(temp_resume_path, temp_jd_path)

            # Display results with dynamic styling
            st.markdown("<br>", unsafe_allow_html=True)
            if verdict == "High":
                st.success("Analysis complete!")
                st.markdown(f"## <p style='color:green;'>Overall Relevance: {verdict}</p>", unsafe_allow_html=True)
            elif verdict == "Medium":
                st.warning("Analysis complete!")
                st.markdown(f"## <p style='color:yellow;'>Overall Relevance: {verdict}</p>", unsafe_allow_html=True)
            else:
                st.error("Analysis complete!")
                st.markdown(f"## <p style='color:red;'>Overall Relevance: {verdict}</p>", unsafe_allow_html=True)

            # Display final score
            st.header("Final Score")
            st.markdown(f"<p style='font-size: 50px; font-weight: bold; color: { 'green' if verdict == 'High' else ('red' if verdict == 'Low' else 'yellow') };'>{final_score:.2f}%</p>", unsafe_allow_html=True)
            st.progress(final_score / 100)

            # Display missing skills if any
            if missing_skills:
                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("Missing Key Skills")
                st.markdown(
                    "<p style='color: #F55555;'>"
                    + ", ".join(missing_skills)
                    + "</p>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                st.success("All Key Skills Found!")

        except Exception as e:
            st.error(f"An error occurred during the relevance check: {e}")
        finally:
            # Clean up temporary files
            os.remove(temp_resume_path)
            os.remove(temp_jd_path)
    else:
        st.warning("Please upload both a resume and a job description.")
