import streamlit as st
import google.generativeai as genai

API_KEY = "API"  #API key is removed due to git warning 
genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain"
}

def initialize_model():
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-001", generation_config=generation_config)
    return model

def generate_resume(name, job_title):
    context = f"""
    You are a professional resume writer. Please generate a professional resume for an individual named {name}, applying for the role of {job_title}.
    The resume should include:
    - A *Professional Summary* summarizing {name}'s expertise in {job_title}.
    - *Relevant Work Experience* with dummy companies and projects, tailored to a {job_title} role.
    - *Educational Background*, with placeholders for degree, university, and graduation year.
    - *Technical Skills*, specifically aligned with {job_title}.
    - Format the resume professionally in *Markdown*.
    - Use placeholders like [Your Email Address], [Your Phone Number], [Your LinkedIn URL (optional)], [Your University Name], and [Your Graduation Year] where necessary.
    """

    model = initialize_model()
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(context)
    if isinstance(response.text, str):
        resume_text = response.text
    else:
        resume_text = response.parts[0].text 

    return clean_resume_text(resume_text)

def clean_resume_text(text):
    text = text.replace("[Add Email Address]", "[Your Email Address]")
    text = text.replace("[Add Phone Number]", "[Your Phone Number]")
    text = text.replace("[Add LinkedIn Profile URL (optional)]", "[Your LinkedIn URL (optional)]")
    text = text.replace("[University Name]", "[Your University Name]")
    text = text.replace("[Graduation Year]", "[Your Graduation Year]")
    return text

# Streamlit UI Setup
st.title("AI-Generated Resume Maker")

# Inputs for Name and Job Title
name = st.text_input("Enter your name:")
job_title = st.text_input("Enter your desired job title:")

# Button to Generate Resume
if st.button("Generate Resume"):
    if name.strip() and job_title.strip():
        cleaned_resume_text = generate_resume(name, job_title)
        st.markdown(cleaned_resume_text)
    else:
        st.warning("Please enter both name and job title.")
