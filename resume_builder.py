import streamlit as st
from groq import Groq
#set-up page configuration
st.set_page_config(
    page_title="Resume Builder",
    page_icon="📃",
    layout="centered"
)
#API set up
try:
    client =Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API key error! Please check your API key")
#UI Design
st.title("Resume Builder📄")
st.write("Enter your basic details below")
name = st.text_input("Enter your name")
phone_number = st.text_input("Enter your phone number")
email_id = st.text_input("Enter your email id")
domain = st.text_input("Enter the domain in which you want me to generate your resume")
col1, col2, col3 = st.columns([1,2,3])
with col2: #positioning generate button
    generate_button =st.button("Generate Resume", type="secondary", use_container_width=True)
if generate_button:
    if not domain.strip():
        st.warning("Please enter a topic")
    else:
        with st.spinner("Your resume is being prepared..."):
            #PROMPT ENGINEERING
            prompt = f"""
            Act as a talented high qualified HR in a top product based company 
            create an outstanding professional resume, where the resume should get shortlisted in every company
            STRICT REQUIREMENT : The resume should be **ATS friendly**
            Name = {name}
            Phone number = {phone_number}
            Email ID = {email_id}
            Domain = {domain}
            Rules:
            1) Just using the above details create a professional resume on your own 
            2) Make sure it should include all fields like summary, professional experience, key skills or technical skills, Projects
            3) Add all those content based on the domain they have given in a professional manner
            4) Use bulletins and follow ATS, make it precise short, clear and neat one
            5) It should easily read and understandable by the recruiters
            6) Highlight relevant keywords and skills 
            7) Keep it simple clean and neat write it in a single page A4
            8) Use line breaks and bullet points, no markdown symbols
            9) PDF or word document not just a text file
            10) It should look like a human created one, never tell anywhere that this is created using AI
            11) NOTES at the end are not required
            """
            #sending request to groq
            try:
                resume_generated = client.chat.completions.create( #apikey.convo as chat.complete the convo.create response
                    messages=[{"role": "user", "content": prompt}], #role - who, content - prompt given
                    model ="llama-3.3-70b-versatile"
                )
                ai_response = resume_generated.choices[0].message.content
                st.success("Your RESUME is Ready!!!")
                st.text(ai_response)
                st.download_button("Download your Resume", ai_response, file_name="resume.txt")
            except Exception as e:
                st.error(f"Error : {e}")

