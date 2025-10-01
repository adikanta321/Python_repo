# 📰 News Summarizer with User Authentication

A desktop application built using **Python and Tkinter** that allows users to:

- Sign up and log in with secure authentication.
- Fetch news articles from the internet using a URL.
- Automatically summarize long articles into short points.
- Save the summary as a **PDF file**.
- Keep a history of summarized articles.
- Reset forgotten passwords using **OTP (sent via email)**.

---

## 🚀 Features

1. **User Authentication**
   - Sign up with username, email, phone, and password.
   - Login securely.
   - Forgot password feature using OTP sent to Gmail.

2. **News Summarization**
   - Paste a news article URL.
   - App extracts the content and summarizes into 3 short sentences.

3. **Save & History**
   - Save summaries as PDF.
   - Maintain history of summarized articles inside the app.

4. **PDF Export**
   - Generate clean summaries into PDF for offline use.

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** → For user interface  
- **MySQL** → For storing user accounts  
- **NLTK** → For summarizing articles  
- **BeautifulSoup** → For extracting article text  
- **FPDF** → For saving summary as PDF  
- **smtplib** → For sending OTP via Gmail  

---

## 📸 Screenshot

**Login Page-View**

---

## ⚙️ Installation & Setup

1. Clone this project:
   ```bash
   git clone https://github.com/adikanta321/Python_repo/blob/main/News_summarize.py
   cd news-summarizer
