# =========================
# 🔹 IMPORTS
# =========================
import requests
import pandas as pd
import re
import ast
from collections import Counter, defaultdict
import os
from dotenv import load_dotenv

import spacy
from spacy.matcher import PhraseMatcher

# Load environment variables
load_dotenv()

# =========================
# 🔹 CONFIG
# =========================
APP_ID = os.getenv('APP_ID')
APP_KEY = os.getenv('APP_KEY')

BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search/{}"

# Broad role coverage (AI + software + business + routine)
ROLES = [
    "data scientist", "machine learning engineer", "ai engineer", "data analyst",
    "software engineer", "backend developer", "frontend developer",
    "business analyst", "project manager", "accountant",
    "graphic designer", "content writer",
    "data entry operator", "customer support executive"
]

PAGES_PER_ROLE = 5     # increase if you want more data
RESULTS_PER_PAGE = 45  # max allowed by Adzuna is 50

# =========================
# 🔹 NLP (spaCy)
# =========================
nlp = spacy.load("en_core_web_sm")

SKILLS = [
    # Programming
    "python","java","c","c++","r","scala","matlab","javascript","typescript",
    # Data
    "sql","mysql","postgresql","mongodb","nosql","redis","snowflake","bigquery",
    # DS Core
    "data analysis","data analytics","data science","statistics","linear algebra","probability",
    # ML/DL
    "machine learning","ml","deep learning","dl","neural networks","cnn","rnn","lstm","transformers",
    # NLP/AI
    "nlp","natural language processing","artificial intelligence","ai",
    "generative ai","gen ai","llm","gpt","computer vision","reinforcement learning",
    # Libs
    "tensorflow","pytorch","keras","scikit-learn","xgboost","lightgbm",
    "opencv","nltk","spacy","huggingface",
    # Viz
    "matplotlib","seaborn","plotly","tableau","power bi",
    # Big Data
    "hadoop","spark","pyspark","hive","kafka","flink",
    # Cloud
    "aws","amazon web services","azure","gcp","google cloud",
    # MLOps
    "mlops","docker","kubernetes","ci cd","jenkins","airflow","fastapi","flask",
    # Tools
    "git","github","gitlab","linux","bash","shell scripting",
    # Business
    "excel","data storytelling","business intelligence","a b testing",
    # Emerging
    "prompt engineering","retrieval augmented generation","rag","vector database","pinecone","weaviate"
]

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(s) for s in SKILLS]
matcher.add("SKILLS", patterns)

def normalize_skill(s):
    m = {
        "ml":"machine learning",
        "dl":"deep learning",
        "ai":"artificial intelligence",
        "gen ai":"generative ai",
        "gpt":"generative ai"
    }
    return m.get(s, s)

def extract_skills_nlp(text):
    doc = nlp(text)
    matches = matcher(doc)
    found = set()
    for _, start, end in matches:
        span = doc[start:end].text.lower()
        found.add(normalize_skill(span))
    return list(found)

def extract_experience(text):
    m = re.search(r'(\d+)\+?\s*years', text.lower())
    return m.group() if m else "Not specified"

# =========================
# 🔹 CLEAN HELPERS
# =========================
def clean_text(t):
    t = str(t).lower()
    t = re.sub(r'\n', ' ', t)
    t = re.sub(r'[^a-zA-Z0-9\s]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def ai_risk_label(skills):
    s = set(skills)
    if any(k in s for k in ["machine learning","deep learning","artificial intelligence","nlp"]):
        return "Safe"
    if any(k in s for k in ["excel"]) or "data entry" in " ".join(s):
        return "High Risk"
    return "Moderate"

def scope_from_desc(desc, skills):
    # simple heuristic summary
    if any(k in skills for k in ["machine learning","deep learning","nlp","artificial intelligence"]):
        return "Build models, analyze data, deploy ML/AI systems"
    if any(k in skills for k in ["sql","excel","data analysis"]):
        return "Analyze data, create reports, support decisions"
    if "data entry" in desc:
        return "Input and manage data, repetitive tasks"
    if any(k in skills for k in ["javascript","frontend","backend"]):
        return "Develop applications, build and maintain systems"
    return "General role responsibilities based on domain and tools"

# =========================
# 🔹 FETCH DATA
# =========================
rows = []

for role in ROLES:
    for page in range(1, PAGES_PER_ROLE + 1):
        url = BASE_URL.format(page)
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": RESULTS_PER_PAGE,
            "what": role,
            "where": "India",
            "sort_by": "date"
        }
        try:
            r = requests.get(url, params=params, timeout=20)
            data = r.json()
        except Exception as e:
            print("API error:", e)
            continue

        for job in data.get("results", []):
            raw_desc = job.get("description", "")
            desc_clean = clean_text(raw_desc)

            skills = extract_skills_nlp(raw_desc)
            exp = extract_experience(raw_desc)

            rows.append({
                "job_id": job.get("id"),
                "role": role,
                "job_title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "posted_date": job.get("created"),
                "job_description": desc_clean,
                "skills": skills,
                "experience_required": exp,
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
            })

df = pd.DataFrame(rows)

# =========================
# 🔹 CLEANING
# =========================
df.drop_duplicates(subset=["job_id"], inplace=True)
df.dropna(subset=["job_title","job_description"], inplace=True)

# skills column safety
def safe_list(x):
    if isinstance(x, list):
        return list(set(x))
    if isinstance(x, str):
        try:
            return list(set(ast.literal_eval(x)))
        except:
            return []
    return []

df["skills"] = df["skills"].apply(safe_list)
df = df[df["skills"].map(len) > 0]

# salary
df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce").fillna(0)
df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce").fillna(0)
df["avg_salary"] = (df["salary_min"] + df["salary_max"]) / 2

# date
df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
df = df[df["posted_date"].notna()]

df.reset_index(drop=True, inplace=True)

# =========================
# 🔹 FEATURE ENGINEERING
# =========================

# Job count per role
job_count = df["role"].value_counts().to_dict()
df["job_count_per_role"] = df["role"].map(job_count)

# Skill frequency (global)
all_skills = [s for lst in df["skills"] for s in lst]
skill_freq = dict(Counter(all_skills))
df["skill_frequency"] = [skill_freq] * len(df)

# Emerging skills (low freq)
emerging = [k for k, v in skill_freq.items() if v < 5]
df["emerging_skills"] = [emerging] * len(df)

# Growth rate (proxy: normalized job count)
mx = max(job_count.values()) if job_count else 1
growth_map = {r: c / mx for r, c in job_count.items()}
df["growth_rate"] = df["role"].map(growth_map)

# AI risk label
df["ai_risk"] = df["skills"].apply(ai_risk_label)

# Scope
df["scope"] = df.apply(lambda r: scope_from_desc(r["job_description"], r["skills"]), axis=1)

# =========================
# 🔹 DEMAND TREND (TIME SERIES)
# =========================
# jobs per day per role
trend_df = (
    df.groupby([df["posted_date"].dt.date, "role"])
      .size()
      .reset_index(name="job_count")
)

# role-level trend label (simple slope over time)
trend_label = {}
for role, g in trend_df.groupby("role"):
    g = g.sort_values("posted_date")
    if len(g) < 2:
        trend_label[role] = "Stable"
        continue
    # simple diff: last vs first
    if g["job_count"].iloc[-1] > g["job_count"].iloc[0]:
        trend_label[role] = "Growing"
    elif g["job_count"].iloc[-1] < g["job_count"].iloc[0]:
        trend_label[role] = "Declining"
    else:
        trend_label[role] = "Stable"

# =========================
# 🔹 ROLE-LEVEL SUMMARY (WHAT YOU SHOW)
# =========================
summary_rows = []

for role, g in df.groupby("role"):
    avg_salary = g["avg_salary"].replace(0, pd.NA).mean()
    top_skills = [s for s, _ in Counter([x for lst in g["skills"] for x in lst]).most_common(10)]
    risk_counts = g["ai_risk"].value_counts().to_dict()

    summary_rows.append({
        "role": role,
        "job_count": len(g),
        "demand_trend": trend_label.get(role, "Stable"),
        "avg_salary": float(avg_salary) if pd.notna(avg_salary) else None,
        "top_skills": top_skills,
        "ai_risk_distribution": risk_counts,
        "emerging_skills": emerging[:10],
        "scope_example": scope_from_desc(" ".join(g["job_description"].head(3)), top_skills)
    })

summary_df = pd.DataFrame(summary_rows).sort_values("job_count", ascending=False)

# =========================
# 🔹 SAVE OUTPUTS
# =========================
df.to_csv("jobs.csv", index=False)
trend_df.to_csv("role_daily_trend.csv", index=False)
summary_df.to_csv("role_summary_output.csv", index=False)

print("✅ Done!")
print("Files saved:")
print("- jobs.csv (row-level data)")
print("- role_daily_trend.csv (time-series)")
print("- role_summary_output.csv (your demo output)")
print("\nSample summary:")
print(summary_df.head())