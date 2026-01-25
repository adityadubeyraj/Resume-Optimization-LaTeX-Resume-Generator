# backend.py

import os
import asyncio
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Save uploaded file
def save_uploaded_file(uploaded_file, save_path="uploaded_resume.pdf"):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

# Extract PDF text asynchronously
async def extract_text_from_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    return pages

# prompt for generate resume
def prompt(user_data,latex_template):
    prompt = f"""
You are a LaTeX resume builder.
I have a LaTeX resume template and a Python dictionary that contains all the data to be filled in.

Your job is to:

1.Populate the LaTeX template using only the data available in the dictionary.
2. If a section (like Experience, Projects, Achievements, etc.) is missing or empty in the dictionary, completely remove that section from the LaTeX output.
3. Maintain proper LaTeX formatting, spacing, and indentation.
4. Do not modify the LaTeX structure other than inserting or removing content as needed.
5. If any field like link, github, or points is not present for an item, skip rendering it.

latex_template:{latex_template}
user_data : {user_data}
output:
Use the following LaTeX resume template (below) and fill only the parts that have data in the dictionary.
Remove any section (like Experience, Projects, etc.) if that key is empty or not present.
Return only the final LaTeX code with the populated values.
"""

    return prompt

def prompt_optimize_resume(user_data):
    # Build prompt
    description="You are an expert resume optimizer with deep knowledge of various industries and job requirements.",
    instructions="""
                        # Resume Enhancement Process
                        
                        ## Analysis Phase
                        1. Analyze the provided job description thoroughly
                        - Extract key requirements, skills, and qualifications
                        - Identify industry-specific terminology and buzzwords
                        - Note preferred experience levels and education requirements
                        
                        2. Evaluate the current resume (payload) against job requirements
                        - Identify strengths that already align with the job description
                        - Spot gaps and improvement opportunities
                        - Determine which sections need enhancement
                        
                        ## Enhancement Phase  
                        3. Modify the resume content to improve job alignment while preserving core facts:
                        - Rephrase experience descriptions using industry-relevant terminology
                        - Highlight transferable skills that match job requirements
                        - Restructure accomplishments to demonstrate relevant outcomes
                        - Ensure all modifications maintain factual accuracy of:
                            * Educational background and institutions
                            * Certification names and credentials
                            * Employment history timeline and company names
                            * Core technical skills and technologies
                        
                        4. DO NOT fabricate or add:
                        - New jobs or positions not in original payload
                        - Skills or technologies not listed in original payload
                        - Educational degrees or certifications not listed in original payload
                        - Projects that don't exist in the original payload
                        
                        ## Scoring and Reporting
                        5. Score the original resume against the job description
                        6. Score the enhanced resume against the job description
                        7. Provide a detailed comparison showing improvements
                        
                        ## Important Guidelines
                        - Focus on professional enhancement through better wording, not factual changes
                        - Maintain the person's actual career trajectory and capabilities
                        - Use industry-standard terminology appropriate for the target position
                        - Eliminate irrelevant content that doesn't support the job application
                        - Fix grammatical errors and improve overall professional tone
                        """,
    expected_output="""
                        # Resume Enhancement Report
                        
                        ## Job Description Analysis
                        {Summary of key requirements and skills from the job description}
                        
                        ## Original Resume Assessment
                        {Brief evaluation of original resume's alignment with job requirements}
                        
                        ## Enhanced Resume Payload
                        ```json
                        {Complete enhanced JSON payload with all optimized fields}
                        ```
                        
                        ## Improvement Summary
                        - Experience Descriptions: {Specific improvements made}
                        - Skills Presentation: {How skills were better aligned}
                        - Project Descriptions: {How projects were reframed to match requirements}
                        - Overall Language Enhancement: {Terminology improvements}
                        
                        ## Scoring Comparison
                        | Category | Original Score | Enhanced Score | Improvement |
                        |----------|---------------|----------------|-------------|
                        | Relevant Experience | {score}/100 | {score}/100 | +{points} |
                        | Skills Match | {score}/100 | {score}/100 | +{points} |
                        | Education & Certs | {score}/100 | {score}/100 | +{points} |
                        | Overall Fit | {score}/100 | {score}/100 | +{points} |
                        
                        ## Overall Match Percentage: {Original score}% → {Enhanced score}%
                        
                        ## Key Improvements Made
                        1. {First major improvement}
                        2. {Second major improvement}
                        3. {Third major improvement}
                        
                        ## Unchanged Elements (Core Facts Preserved)
                        - All employment history dates and company names
                        - Educational credentials and institutions
                        - Certification titles
                        - Core technical skills

                        """
    full_resume_text = "\n\n".join(user_data["resume_text"])
    job_description = user_data["job_description"]

    prompt_template = f"""
                            # Agent Description:
                            {description}

                            # Instructions:
                            {instructions}

                            # Expected Output:
                            {expected_output}

                            # User Resume:
                            {full_resume_text}

                            # Job Description:
                            {job_description}
                            """


    return prompt_template

def llm_output(prompt):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)
    response = llm.invoke(prompt)
    return response

@tool
def calculate_ats_score(input: str) -> str:
    """
    Calculates the ATS score. Input format: "resume: <text>, jd: <text>"
    """
    try:
        resume_text, job_description = input.split("jd:")
        resume_text = resume_text.replace("resume:", "").strip()
        job_description = job_description.strip()

        texts = [resume_text, job_description]
        vectorizer = CountVectorizer().fit_transform(texts)
        vectors = vectorizer.toarray()
        score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
        return f"ATS Score: {round(score * 100, 2)}%"
    except Exception as e:
        return f"Error parsing input: {e}"


def agent(prompt):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)
    # Register the tool
    tools = [calculate_ats_score]

    # Create the agent
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
        )
    response = agent.run(prompt)
    return response
