# 🧠 Resume Optimizer & Generator

A Streamlit-based web application that helps users **build, optimize, and generate professional resumes using AI**.

You can upload an existing resume and job description to receive **optimized suggestions**, or generate a **LaTeX resume from scratch** using structured inputs.

---

## 🚀 Features

- 📤 Upload PDF Resume
- 🧾 Enter Personal, Education, Experience, Skills & Project Details
- 📈 Optimize Resume using AI to Match Job Description
- 📝 Generate LaTeX-based Resume from Scratch
- 🧠 Integrated with Google Gemini via LangChain
- 📊 ATS Score Calculation & Enhancement Insights

---

## 🛠️ Technologies Used

- **LLMs:** Google Gemini (via LangChain)
- **Frontend:** Streamlit
- **Backend:** Python
- **Libraries:** asyncio, scikit-learn, dotenv, PyPDFLoader
- **Template Engine:** LaTeX
- **Workflow:** ReAct-style tool-augmented LLM pipeline

---

## 📂 Project Structure

Resume_Optimizer/
│
├── frontend.py # Main Streamlit App
├── backend.py # Core Logic & Prompt Engineering
├── resume.tex # LaTeX Resume Template
├── .env # Environment Variables (Google API Key)
└── README.md # Project Documentation


---

## 🔧 Setup Instructions

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/resume-optimizer.git
cd resume-optimizer
