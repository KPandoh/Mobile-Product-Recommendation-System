# 📱 GalaxyMatch AI
### AI-Powered Samsung Smartphone Recommendation System

An intelligent recommendation system that helps users discover the most suitable Samsung Galaxy smartphone based on their preferences using a **Weighted Sum Model** enhanced with **Generative AI** for personalized explanations.

---

## 📖 Project Overview

Choosing the right smartphone can be overwhelming due to the wide variety of Samsung Galaxy devices available across different price ranges and use cases.

**GalaxyMatch AI** simplifies this decision-making process by combining:

- 📊 Data-driven recommendation algorithms
- 🤖 Generative AI for natural language understanding
- 📱 Samsung Galaxy device specifications
- 🎯 Personalized recommendations based on user preferences

Instead of simply displaying specifications, the system understands user needs and recommends the best Samsung smartphone while explaining *why* it is the ideal choice.

---

# 🎯 Problem Statement

Customers often struggle to identify the Samsung smartphone that best fits their requirements due to numerous choices with varying specifications, prices, and target audiences.

This project aims to build an intelligent recommendation system that provides personalized Samsung Galaxy phone recommendations using feature-based scoring and AI-generated explanations.

---

# 🚀 Objectives

- Recommend Samsung smartphones based on user preferences.
- Support both predefined personas and natural language user input.
- Rank devices using a transparent Weighted Sum Model.
- Generate human-like explanations using Generative AI.
- Visualize device data using Exploratory Data Analysis (EDA).

---

# 🏗 System Architecture

```text
                    User

                      │
                      ▼

        Select Persona / Describe Yourself

                      │
                      ▼

        Generative AI Preference Extraction
      (Budget, Camera, Gaming, Battery etc.)

                      │
                      ▼

            Preference Weight Generator

                      │
                      ▼

          Weighted Sum Recommendation Model

                      │
                      ▼

         Rank Samsung Galaxy Smartphones

                      │
                      ▼

      AI Explanation + Recommendation Output
```

---

# 🧠 Recommendation Workflow

```text
Samsung Dataset
       │
       ▼
Data Cleaning
       │
       ▼
Feature Engineering
       │
       ▼
Feature Normalization
       │
       ▼
Weighted Sum Model
       │
       ▼
Top 3 Recommendations
       │
       ▼
Generative AI Explanation
```

---

# 📊 Dataset

The project uses a curated Samsung Galaxy smartphone dataset containing devices from the **2024–2025 Galaxy lineup**.

### Features

| Feature |
|----------|
| Model Name |
| Price (INR) |
| RAM |
| Storage |
| Camera (MP) |
| Battery (mAh) |
| Screen Size |
| Target Segment |
| Processor |
---

# ⚙ Feature Engineering

Additional intelligent features are generated from the raw dataset.

- Camera Score
- Performance Score
- Battery Score
- Display Score
- Value for Money Score

These engineered features improve recommendation quality.

---

# 📈 Exploratory Data Analysis (EDA)

The project includes:

- Price Distribution
- Battery Capacity Distribution
- RAM Comparison
- Price vs Camera Analysis
- Target Segment Distribution
- Correlation Heatmap

---

# 🧮 Recommendation Algorithm

The recommendation engine uses a **Weighted Sum Model**.

```
Final Score =
(Camera Score × W₁)
+
(Performance Score × W₂)
+
(Battery Score × W₃)
+
(Value Score × W₄)
```

The weights dynamically change depending on user preferences.

Example:

Photography User

```
Camera       40%
Battery      20%
Performance  20%
Value        20%
```

Gaming User

```
Performance  45%
Battery      25%
Display      20%
Value        10%
```

---

# 🤖 Generative AI Integration

Generative AI is used for two tasks.

### Preference Extraction

Example input

> I am a college student with a budget of ₹35,000. I play BGMI and need good battery life.

↓

AI extracts

```json
{
  "budget": 35000,
  "gaming": 0.45,
  "battery": 0.30,
  "camera": 0.10,
  "value": 0.15
}
```

---

### Recommendation Explanation

Instead of

> Galaxy S24 FE

The AI generates

> The Galaxy S24 FE is recommended because it offers flagship-level performance, a vibrant AMOLED display, and long battery life while staying within your preferred budget.

---

# 💻 Tech Stack

| Category | Technology |
|-----------|------------|
| Programming | Python |
| Data Analysis | Pandas |
| Numerical Computing | NumPy |
| Visualization | Matplotlib |
| Machine Learning | Scikit-Learn |
| Notebook Interface | Jupyter Notebook |
| Interactive UI | ipywidgets |
| AI | OpenAI / Google Gemini API |

---

# 📂 Project Structure

```
GalaxyMatch-AI/
│
├── data/
│   ├── samsung_dataset.csv
│   └── cleaned_dataset.csv
│
├── notebooks/
│   ├── EDA.ipynb
│   ├── Feature_Engineering.ipynb
│   └── Recommendation_System.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── scoring.py
│   ├── recommendation.py
│   ├── ai_explanation.py
│   └── utils.py
│
├── images/
│
├── README.md
│
└── requirements.txt
```

---

# 👥 Team Responsibilities

## 👨‍💻 Member 1 — Data Engineer

Responsibilities

- Dataset Collection
- Data Cleaning
- Missing Value Handling
- Feature Engineering
- Data Normalization

Deliverables

- Clean Dataset
- EDA
- Processed CSV

---

## 👨‍💻 Member 2 — Recommendation Engineer

Responsibilities

- Weighted Sum Algorithm
- Score Calculation
- Ranking System
- Evaluation

Deliverables

- Recommendation Engine
- Ranking Module

---

## 👨‍💻 Member 3 — Frontend & UI Developer

Responsibilities

- Jupyter UI
- User Forms
- Dropdown Menus
- Interactive Widgets
- Result Visualization

Deliverables

- Interactive Interface

---

## 👨‍💻 Member 4 — AI & Documentation

Responsibilities

- Prompt Engineering
- AI Integration
- Explanation Generation
- Presentation
- Report
- GitHub Documentation

Deliverables

- AI Module
- Project Report
- Presentation

---

# 📸 Sample Recommendation

Input

```
Budget

₹40,000

Preference

Photography

Battery

High
```

Output

```
⭐ Galaxy A55 5G

Match Score

92%

Reason

Excellent camera performance,
premium AMOLED display,
long battery life,
fits your budget.
```

---

# 📅 Development Timeline

| Phase | Task |
|--------|------|
| Day 1 | Dataset Collection, Cleaning, EDA & Feature Engineering |
| Day 2 | Recommendation Algorithm |
| Day 3 | AI Integration |
| Day 4 | UI Development |
| Day 5 | Testing & Documentation |

---

# 🔮 Future Improvements

- Collaborative Filtering
- User Review Analysis
- Real-time Price Tracking
- Samsung Store API Integration
- Fine-Tuned LLM
- Mobile Application
- Cloud Deployment
- Voice-Based Recommendation

---

# 📚 References

- Samsung Official Specifications
- Scikit-Learn Documentation
- Pandas Documentation
- NumPy Documentation
- Matplotlib Documentation
- OpenAI API
- Google Gemini API
- Claude

---

# 📄 License

This project is developed for academic purposes as part of a Generative AI coursework project.

---

# ⭐ Acknowledgements

Special thanks to the faculty members and project mentors for their guidance throughout the development of this recommendation system.
