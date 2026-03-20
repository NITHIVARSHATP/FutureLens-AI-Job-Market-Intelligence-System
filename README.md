# 🤖 AI Job Market, Skill Demand & Job Displacement Prediction System

## 🌍 Overview

This project is a **machine learning-based system** designed to analyze job market data and predict future trends in employment. It identifies **in-demand skills**, forecasts **job growth**, and estimates the **risk of job displacement due to AI and automation**.

The system integrates **historical datasets** with **real-time signals** to provide intelligent insights for students and professionals.

---

## 🎯 Objectives

* 📊 Identify trending skills in the job market
* 🔮 Predict future demand for job roles
* 🤖 Estimate AI-based job displacement risk
* 🎓 Recommend skills and career paths

---

## ⚙️ Key Features

### 📊 Skill Demand Analysis

Extracts and analyzes job postings to identify **high-demand skills** such as Python, AI, Cloud, etc.

### 🔮 Job Growth Prediction

Predicts whether a job role will:

* 🚀 Grow
* 📈 Remain stable
* 📉 Decline

### 🤖 Automation Risk Detection

Classifies jobs into:

* ✅ Low Risk
* ⚠️ Medium Risk
* ❌ High Risk

### 🎓 Career Recommendation

Suggests skills required to stay relevant in an AI-driven job market.

---

## 📂 Datasets Used

### 1. Job Postings Dataset

* Source: Kaggle
* Contains job titles, skills, company details

### 2. Automation Risk Dataset

* Source: OECD / Frey & Osborne
* Provides probability of job automation

### 3. Future Job Trends Dataset

* Source: World Economic Forum
* Contains emerging and declining roles

### 4. Google Trends (Real-Time Data)

* Used to track **live skill demand**

---

## 🧠 System Architecture

```
Job Postings Data ──► Demand Analysis
                         │
Google Trends ─────────► Trend Score
                         │
Automation Dataset ───► Risk Score
                         │
                         ▼
              Hybrid Prediction Model
                         │
                         ▼
     Job Growth + AI Risk Classification
```

---

## 🛠 Technologies Used

* 🐍 Python
* 📚 Pandas, NumPy
* 🤖 Scikit-learn
* 📊 Matplotlib / Seaborn
* 🌐 PyTrends (Google Trends API)

---

## ⚙️ Implementation Workflow

1. 📂 Data Collection
2. 🧹 Data Cleaning & Preprocessing
3. 📊 Feature Engineering

   * Demand Score
   * Trend Score
   * Automation Risk
4. 🔗 Dataset Integration
5. 🧠 Model Building
6. 📉 Prediction & Visualization

---

## 🧮 Prediction Logic

The system uses a **hybrid scoring model**:

* Job Demand ↑ → Growth ↑
* Skill Trends ↑ → Growth ↑
* Automation Risk ↑ → Growth ↓

---

## 📊 Sample Output

| Job Role         | Growth Prediction | AI Risk   |
| ---------------- | ----------------- | --------- |
| AI Engineer      | 🚀 High Growth    | Low ✅     |
| Data Analyst     | 📈 Moderate       | Medium ⚠️ |
| Data Entry Clerk | 📉 Declining      | High ❌    |

---

## 🎓 Use Cases

* Students choosing career paths
* Professionals upgrading skills
* Organizations analyzing workforce trends

---

## 📌 Key Insight

> This system combines **historical automation data with real-time job market trends** to generate accurate predictions about the future of jobs.

---

## 👩‍💻 Author

**Nithivarsha T P - 036**
**Purushothaman B - 039**
**Srisaran J      - 306**

---