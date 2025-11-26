
# 📧 Email Threat Analyzer  
### Hybrid Spam Detection (Multinomial Naive Bayes + Heuristic Engine)

A cyber-security themed web application that analyzes email text and predicts whether it is **SPAM** or **SAFE**, using a hybrid system combining:

- **TF-IDF + Multinomial Naive Bayes machine learning model**, and  
- **Custom heuristic scoring engine** (keyword detection + uppercase anomaly detection)

This produces a more realistic and accurate threat score than basic ML-only models.

---

## 🔥 Features

### 🧠 Machine Learning
- Multinomial Naive Bayes (fast & reliable)
- TF-IDF vectorizer (1–3 n-grams)
- Cleaned training dataset (`spam.csv`)
- High accuracy on standard spam datasets

### 🛡️ Heuristic Engine
Boosts model probability using:
- High-risk keyword matches (e.g., “urgent”, “verify now”)
- Uppercase pattern detection (“URGENT”, “FREE”)
- Weighted risk boost formula:
  ```
  boost = 0.5 * keyword_score + 0.3 * uppercase_score
  adjusted_prob = raw_prob + boost
  ```

### 🎨 UI (Tailwind CSS Dashboard)
- Cyber-security dark mode interface  
- Inline result analysis panel  
- Shows raw probability + heuristic breakdown  
- Fully responsive UI  

### ⚙️ Flask Backend
- Loads saved TF-IDF model  
- Loads Multinomial Naive Bayes model  
- Processes messages through ML + heuristics  

---

## 📁 **Project Structure (Updated)**  
Your current real project structure:

```
PythonProject/
│── app.py
│── README.md
│── requirements.txt
│── test_tf_numpy.py
│── .gitignore
│
├── models/
│   ├── ann.h5
│   ├── best_ann.h5
│   ├── best_cnn.h5
│   ├── cnn.h5
│   ├── log_reg_model.pkl
│   ├── logreg_model.pkl
│   ├── nb_model.pkl
│   ├── svm_model.pkl
│   ├── tfidf.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── tokenizer.pkl
│
├── templates/
│   ├── index.html
│   ├── result.html
│
└── static/
    └── style.css
```

Only the needed files for the app to run are:
- `models/nb_model.pkl`
- `models/tfidf.pkl`
- `templates/index.html`
- `templates/result.html`
- `static/style.css`
- `app.py`

---

## 🧪 Dataset  
This project uses the Email Spam Collection dataset** (`spam.csv`).  
It contains labeled messages such as:

- `ham` = SAFE  
- `spam` = malicious  

---

## 🚀 Installation

Clone the repo
```
git clone https://github.com/your-username/email-threat-analyzer.git
cd email-threat-analyzer
```
### 1. Create virtual environment
```
python -m venv .venv
```

Activate:
```
.venv\Scripts\activate
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Run Flask App
```
python app.py
```

Visit in browser:
```
http://127.0.0.1:5000/
```

---

## 🖥️ How Prediction Works

1. Input text → cleaned  
2. TF‑IDF vectorized  
3. Naive Bayes gives a spam probability  
4. Heuristic engine computes:
   - matched spam keywords  
   - uppercase suspicion score  
   - boost  
5. Final probability → spam or safe  

---

## 📦 Requirements
```
flask pandas scikit-learn joblib tensorflow
---

## 👨‍💻 Developer  
**Aksh Patel**  
Cyber Security • Machine Learning • Python Development
