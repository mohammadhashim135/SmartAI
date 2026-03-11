# 🤖 SmartAI Hub – AI Problem Solver

SmartAI Hub is an AI-powered platform that provides tools for solving everyday problems related to **security, health, learning, and media awareness**.

---

## 🛠️ Tools

| Tool | What it does |
|------|-------------|
| 🔐 **Scam Detector** | Analyzes messages for phishing, fraud & scam signals |
| 💊 **Medicine Checker** | Drug info, side effects, contraindications & interactions |
| 📰 **Fake News Analyzer** | Fact-checks headlines, articles & claims |
| 📚 **Study Assistant** | Summarizes notes, generates flashcards, practice questions |
| 🏷️ **Text Classifier** | Detects sentiment, topic, intent, tone & urgency |

---

## 🏗️ Architecture

```
User → Streamlit UI → Tool Selection → AI API → Structured JSON → Visual Result
```

All tools use an AI model via an API.  
Responses are parsed as **structured JSON** and rendered as visual dashboards.

---

## 💡 Key Features

- **Zero heavy ML models** — no downloading gigabyte models
- **Structured AI responses** — tools return JSON parsed into dashboards
- **Dark theme UI** — clean and professional interface
- **5 tools in 1** — unified AI platform
- **Real-world problems** — cybersecurity, healthcare, education, media literacy

---

# Overview

SmartAI Hub combines multiple AI utilities into a single application built with **Streamlit**.  
Users can analyze messages, check medicines, detect fake news, summarize notes, and classify text.

---

# Features 🚀

- AI powered analysis tools
- Instant responses using AI APIs
- Structured JSON outputs
- Clean and interactive Streamlit UI
- Modular tool architecture

---

# Tech Stack 🛠

- **Python**
- **Streamlit**
- **AI API integration**
- **JSON parsing**
- **Git & GitHub**

---

# Installation & Setup 🏗

## 1. Clone the Repository

```bash
git clone https://github.com/mohammadhashim135/SmartAI.git
cd SmartAI
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it.

### Windows
```bash
.venv\Scripts\activate
```

### Mac / Linux
```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create Environment Variables

Create a `.env` file in the root directory.

Example:

```
OPENAI_API_KEY=your_api_key_here
```

---

## 5. Run the Application

```bash
streamlit run app.py
```

---

# Usage Guide 📝

1. Open the Streamlit app
2. Select a tool
3. Enter the required input
4. Click analyze
5. View AI results

---

# Project Structure 📂

```bash
SmartAI/
├── app.py
├── requirements.txt
├── README.md
└── tools/
    ├── __init__.py
    ├── ai_client.py
    ├── scam_detector.py
    ├── medicine_checker.py
    ├── fake_news.py
    └── summarizer.py
```

---

---
## **Contributing** 🤝
Contributions are welcome! If you’d like to improve feel free to fork the repo and submit a pull request.

### **Steps to Contribute:**

### **1. Fork the repository**

### **2. Create a new branch:**

```bash
git checkout -b feature-branch
```

### **3. Make your changes and commit:**

```bash
git commit -m "Added new feature"
```
### **4. Push to the branch:**

```bash
git push origin feature-branch
```
### **5. Open a Pull Request**
---
## **License** 📜
This project is licensed under the MIT License.

💡 Developed with ❤️ by [Mohammad Hashim](https://github.com/mohammadhashim135/SmartAI.git)


