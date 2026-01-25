🧠 Resume Optimizer & Generator
This Streamlit web app helps users build, optimize, and generate professional resumes using AI. Upload your existing resume and job description, and the app provides optimized suggestions. You can also generate a LaTeX resume from scratch based on inputs.

🚀 Features
📤 Upload your PDF Resume
🧾 Enter Personal, Education, Experience, Skills & Project details
📈 Optimize resume using AI to match the job description
📝 Generate LaTeX-based resume from scratch
🧠 Integrated with Google Gemini Pro via LangChain
📊 ATS Score calculation and resume enhancement insights
🛠️ Technologies Used
Streamlit
LangChain
Google Gemini API
Python Libraries: asyncio, scikit-learn, dotenv, PyPDFLoader
📂 Project Structure
Resume_Optimizer/ │ ├── frontend.py # Main Streamlit App

├── backend.py # Core Logic & Prompt Engineering

├── resume.tex # LaTeX Resume Template

├── .env # Environment Variables (Google API Key)

└── README.md # This file

🔧 Setup Instructions
Clone the repository:

git clone https://github.com/yourusername/resume-optimizer.git
cd resume-optimizer
Install dependencies

pip install -r requirements.txt
Set up environment variables: Create a .env file with your Google API Key: GOOGLE_API_KEY=your_google_api_key

Run the app

streamlit run frontend.py
How It Works
User Inputs Resume & Job Description
LLM (Gemini) analyzes & optimizes content
Outputs enhanced version + ATS Score
Option to generate new resume using LaTeX template
