import streamlit as st
import asyncio
from backend import save_uploaded_file,extract_text_from_pdf,prompt_optimize_resume,llm_output,prompt,agent


# ---------- PAGE START ----------
st.set_page_config(page_title="Resume Optimizer", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>Resume Optimizer & Generator</h1>", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.header("📄 Upload Resume & Job Description")
uploaded_file = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.sidebar.text_area("Paste Job Description Here", height=200)

# ---------- MAIN TABS ----------
tabs = st.tabs(["🧾 Personal Info", "🧠 Skills", "💼 Experience", "🚀 Projects", "🎓 Education", "📈 Optimize","📝 Generate Resume"])

# ---------- PERSONAL INFO TAB ----------
with tabs[0]:
    st.subheader("Personal Information")
    with st.form("personal_info_form"):
        full_name = st.text_input("Full Name")
        location = st.text_input("Location")
        job_title = st.text_input("Job Title")
        linkedin_url = st.text_input("LinkedIn URL")
        email = st.text_input("Email")
        github_url = st.text_input("GitHub URL")
        phone = st.text_input("Phone Number")
        submitted_info = st.form_submit_button("Save Info")

    if submitted_info:
        st.success("✅ Personal Info Saved")

# ---------- SKILLS TAB ----------
with tabs[1]:

    st.subheader("Add Skills")

    # Initialize skill list in session_state if not present
    if "skill_list" not in st.session_state:
        st.session_state.skill_list = []

    with st.form("skills_form"):
        skills = st.text_area(
            "Enter your skills (comma-separated)",
            placeholder="Python, React, SQL, Machine Learning"
        )
        submitted_skills = st.form_submit_button("Save Skills")

    if submitted_skills:
        st.session_state.skill_list = [s.strip() for s in skills.split(",") if s.strip()]
        st.success("✅ Skills Saved")

    # Display saved skills if any
    if st.session_state.skill_list:
        st.subheader("Your Skills")
        st.write(st.session_state.skill_list)


# ---------- EXPERIENCE TAB ----------
with tabs[2]:
    st.subheader("Add Work Experience")

    if "experiences" not in st.session_state:
        st.session_state.experiences = []

    with st.form("experience_form"):
        company = st.text_input("Company Name")
        role = st.text_input("Role/Position")
        duration = st.text_input("Duration (e.g. Jan 2020 - Dec 2022)")
        description = st.text_area("Description")
        submitted_exp = st.form_submit_button("Add Experience")

    if submitted_exp:
        st.session_state.experiences.append({
            "company": company,
            "role": role,
            "duration": duration,
            "description": description
        })
        st.success("✅ Experience Added")

    # Show all experiences
    if st.session_state.experiences:
        st.subheader("Your Experiences")
        for idx, exp in enumerate(st.session_state.experiences):
            st.markdown(f"**{exp['role']} at {exp['company']}**")
            st.markdown(f"Duration: {exp['duration']}")
            st.markdown(exp['description'])
            st.markdown("---")


# ---------- PROJECTS TAB ----------
with tabs[3]:
    st.subheader("Add Projects")

    if "projects_list" not in st.session_state:
        st.session_state.projects_list = []

    with st.form("projects_form"):
        project_title = st.text_input("Project Title")
        project_desc = st.text_area("Project Description")
        tech_stack = st.text_input("Technologies Used (comma-separated)")
        submitted_proj = st.form_submit_button("Add Project")

    if submitted_proj:
        st.session_state.projects_list.append({
            "title": project_title,
            "description": project_desc,
            "tech_stack": tech_stack
        })
        st.success("✅ Project Added")

    # Display saved projects
    if st.session_state.projects_list:
        st.subheader("Your Projects")
        for proj in st.session_state.projects_list:
            st.markdown(f"**{proj['title']}**")
            st.markdown(proj['description'])
            st.markdown(f"**Tech Stack:** {proj['tech_stack']}")
            st.markdown("---")


# ---------- EDUCATION TAB ----------
with tabs[4]:
    st.subheader("Add Education")

    if "education_list" not in st.session_state:
        st.session_state.education_list = []

    with st.form("education_form"):
        institute = st.text_input("Institute Name")
        degree = st.text_input("Degree / Program")
        edu_duration = st.text_input("Duration (e.g. 2019 - 2023)")
        submitted_edu = st.form_submit_button("Add Education")

    if submitted_edu:
        st.session_state.education_list.append({
            "institute": institute,
            "degree": degree,
            "duration": edu_duration
        })
        st.success("✅ Education Added")

    # Show all education entries
    if st.session_state.education_list:
        st.subheader("Your Education History")
        for edu in st.session_state.education_list:
            st.markdown(f"**{edu['degree']}**, {edu['institute']} ({edu['duration']})")
            st.markdown("---")




# ---------- COLLECT ALL USER DATA ----------
if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)
    resume_text = asyncio.run(extract_text_from_pdf(file_path))

user_data = {
    "personal_info": {
        "full_name": st.session_state.get("full_name", full_name if "full_name" in locals() else ""),
        "location": st.session_state.get("location", location if "location" in locals() else ""),
        "job_title": st.session_state.get("job_title", job_title if "job_title" in locals() else ""),
        "linkedin_url": st.session_state.get("linkedin_url", linkedin_url if "linkedin_url" in locals() else ""),
        "email": st.session_state.get("email", email if "email" in locals() else ""),
        "github_url": st.session_state.get("github_url", github_url if "github_url" in locals() else ""),
        "phone": st.session_state.get("phone", phone if "phone" in locals() else "")
    },
    "skills": st.session_state.get("skill_list", []),
    "experiences": st.session_state.get("experiences", []),
    "projects": st.session_state.get("projects_list", []),
    "education": st.session_state.get("education_list", []),
    "job_description": job_description,
    "resume_text": [page.page_content for page in resume_text] if uploaded_file else []
}

# ---------- OPTIMIZE TAB ---------- #

with tabs[5]:
    st.subheader("📈 Optimize Resume")

    if uploaded_file and job_description:
        if st.button("⚡ Run Optimization"):
            with st.spinner("Analyzing and optimizing your resume..."):
                prompt_optimize = prompt_optimize_resume(user_data)
                response = llm_output(prompt_optimize)

                # Display as Markdown
                st.markdown(response.content)

    elif not uploaded_file:
        st.warning("📤 Please upload your resume to enable optimization.")
    elif not job_description:
        st.warning("✍️ Please paste a job description in the sidebar to continue.")

# ------------ Generate Resume ---------- #

import base64
with tabs[6]:
    st.subheader("🛠️ Generate Resume From Scratch")

    if st.button("🛠️ Generate Resume from Inputs"):
        with st.spinner("Generating your resume from the information provided..."):
            with open("resume.tex", "r", encoding="utf-8") as file:
                latex_content = file.read()
            prompt_generate = prompt(user_data,latex_content)  
            response = llm_output(prompt_generate)

            st.markdown(response.content)
            