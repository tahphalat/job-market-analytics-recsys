# CEDT Internship 2026 — Project Portfolio

Welcome to the central repository for my internship preparation projects.  
This monorepo contains applications demonstrating **data engineering**, **analytics**, and **user-facing data products**.

## 📂 Projects

### 1. [📊 JobScope Analytics](./dsde)
> **Data-Driven Job Market Analytics Platform**
>
> An end-to-end data engineering project that transforms raw job postings into actionable insights.
>
> * **Focus:** ETL Pipelines, Batch Data Processing, Data Quality, Analytics Systems  
> * **Tech Stack:** Python, Pandas, Parquet, Streamlit, Altair  
> * **Key Feature:** Optimized for cloud deployment with memory-efficient processing (~90% reduction)
>
> 🔗 **Live Demo (Streamlit Dashboard):**  
> https://jobscope.streamlit.app  
>
> The Streamlit app provides an interactive analytics dashboard for exploring cleaned and structured job market data.

---

### 2. [🌐 JobScope Website](./web)
> **Web-Based Analytics Interface**
>
> A modern web application built as an **alternative interface** for viewing and exploring JobScope insights,
> complementing the Streamlit dashboard.
>
> * **Focus:** Data Presentation, UI/UX for Analytics, Component-Based Architecture  
> * **Tech Stack:** TypeScript, Next.js (App Router), Tailwind CSS  
> * **Purpose:** Offer an additional, web-native way to explore JobScope data beyond Streamlit
>
> 🔗 **Live Demo (Website):**  
> https://job-market-analytics-recsys.vercel.app

---

## 🚀 Getting Started

Each project is independent.  
Please navigate to the respective directory for specific installation and usage instructions.

```bash
# Clone the repository
git clone https://github.com/tahphalat/job-market-analytics-recsys.git

# 🔹 Run JobScope Analytics (Streamlit)
cd dsde
pip install -r requirements.txt
streamlit run src/app_streamlit.py

# 🔹 Run JobScope Website
cd web
npm install
npm run dev
