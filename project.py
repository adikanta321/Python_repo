import tkinter as tk
from tkinter import messagebox, filedialog
import mysql.connector
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
import json
import nltk
from nltk.sem.chat80 import borders
from nltk.tokenize import sent_tokenize, word_tokenize
from heapq import nlargest
import re
import random
import smtplib
import os
from datetime import datetime, timedelta
from flask import Flask, request, render_template, redirect, session  # Use Flask if your project is web-based

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('punkt', force=True)
nltk.download('punkt_tab', force=True)
# Database Setup
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "123456",
    "database": "user_authentication"
}


def create_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            User_name VARCHAR(100) NOT NULL,
            Email VARCHAR(100) UNIQUE NOT NULL,
            Phone_number VARCHAR(10) UNIQUE NOT NULL,
            Password VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# User Authentication
def register_user(User_name,Email, Phone_number, Password):
    # Validate First Name
    if not User_name.strip():
        messagebox.showerror("Error", "User Name is required!")
        return

    # Validate Email (@gmail.com required)
    if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", Email):
        messagebox.showerror("Error", "Invalid Email! Must be in @gmail.com format.")
        return

    # Validate Phone Number (must be exactly 10 digits)
    if not re.match(r"^\d{10}$", Phone_number):
        messagebox.showerror("Error", "Phone number must be exactly 10 digits!")
        return

    # Validate Password (cannot be empty)
    if not Password.strip():
        messagebox.showerror("Error", "Password is required!")
        return

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (User_name, Email, Phone_number, Password) VALUES (%s, %s, %s, %s)",
                       (User_name, Email, Phone_number, Password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "User registered successfully!")
        show_home_screen()  # Redirect to the home screen after successful registration
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "This email or phone number is already registered!")

def login_user(Email, Password):
    if not Email.strip() or not Password.strip():  # Check if fields are empty
        messagebox.showerror("Error", "Email and Password cannot be empty!")
        return

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE Email=%s AND Password=%s", (Email, Password))
    user = cursor.fetchone()
    print(f"Debug: Retrieved User -> {user}")  # Debugging line

    if user:
        messagebox.showinfo("Success", "Login successful!")
        show_home_screen()  # Redirect to the home screen if login is successful
    else:
        messagebox.showerror("Error", "Invalid email or password. Please try again.")


# News Summarization
HISTORY_FILE = "history.json"
history = []


def fetch_article(url):
    try:
        if not url.startswith("http"):
            messagebox.showerror("Invalid URL", "Please enter a valid URL starting with http or https.")
            return ""
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.get_text() for p in paragraphs])
        if not article_text.strip():
            messagebox.showwarning("No Content", "The article does not contain any extractable text.")
            return ""
        return article_text
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch article: {e}")
        return ""


def summarize_text(text, num_sentences=3):
    if not text.strip():
        return "No valid content to summarize."
    sentences = sent_tokenize(text)
    if len(sentences) < num_sentences:
        return text
    word_frequencies = {}
    for word in word_tokenize(text):
        if word.isalnum():
            word_frequencies[word.lower()] = word_frequencies.get(word.lower(), 0) + 1
    max_freq = max(word_frequencies.values(), default=1)
    for word in word_frequencies:
        word_frequencies[word] /= max_freq
    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]
    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    return ' '.join(summary_sentences)


def save_as_pdf(summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary)
    file_path = "{}/news_summary.pdf".format(filedialog.askdirectory())
    if file_path:
        pdf.output(file_path)
        messagebox.showinfo("Success", "PDF saved successfully!")


def save_history(url, summary):
    history.append(f"• {url} - {summary[:50]}...")
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)
    history_text.insert(tk.END, "\n".join(history))
    history_text.config(state=tk.DISABLED)


def show_home_screen():
    for widget in root.winfo_children():
        widget.destroy()

    header_frame = tk.Frame(root, bg="#D8BFD8", height=50)
    header_frame.pack(fill="x")

    ad_logo = tk.Label(header_frame, text="AD News", font=("Poppins", 16, "bold"), bg="#D8BFD8")
    ad_logo.pack(side="left", padx=10)

    logout_button = tk.Button(header_frame, text="Logout", font=("Poppins", 12), bg=root.cget("bg"), fg="black",
                              command=show_login_screen)
    logout_button.pack(side="right", padx=10, pady=5)

    tk.Label(root, text="News", font=("Poppins", 20, "bold"), bg="#E3F2FD").pack(pady=10)

    frame = tk.Frame(root)
    frame.pack()

    url_entry = tk.Entry(frame, width=50, font=("Poppins", 12))
    url_entry.pack(side="left", padx=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    clear_button = tk.Button(button_frame, text="Clear", font=("Poppins", 12), bg=root.cget("bg"),
                             command=lambda: [url_entry.delete(0, tk.END), summary_text.delete(1.0, tk.END),save_history.delete(1.0,tk.END)])
    clear_button.grid(row=0, column=0, padx=5)

    save_pdf_button = tk.Button(button_frame, text="Save as PDF", font=("Poppins", 12), bg=root.cget("bg"),
                                command=lambda: save_as_pdf(summary_text.get(1.0, tk.END)))
    save_pdf_button.grid(row=0, column=1, padx=5)

    summarize_button = tk.Button(button_frame, text="Summarize", font=("Poppins", 12), bg="#1565C0", fg="white",
                                 command=lambda: summary_text.insert(tk.END,
                                                                     summarize_text(fetch_article(url_entry.get()), 3)))
    summarize_button.grid(row=0, column=2, padx=5)

    summary_text = tk.Text(root, height=10, width=70, font=("Poppins", 12))
    summary_text.pack(pady=10)

    save_history_button = tk.Button(root, text="Save History", font=("Poppins", 12),
                                    command=lambda: save_history(url_entry.get(), summary_text.get(1.0, tk.END)))
    save_history_button.pack(pady=10)

    global history_text
    history_text = tk.Text(root, height=10, width=70, font=("Poppins", 12), state=tk.DISABLED)
    history_text.pack(pady=10)

root = tk.Tk()  # Initialize the main application window
root.title("News Summarizer")
root.geometry("800x600")  # Set the window size (adjust as needed)


def show_sign_up_screen():
    global  username_entry, email_entry, phone_entry, pass_entry

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Sign Up", font=("Poppins", 20, "bold")).pack(pady=20, anchor="w", padx=20)

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=10)

    # Last Name
    tk.Label(frame, text="Username", font=("Poppins", 12)).grid(row=1, column=0, sticky="w", pady=5)
    username_entry = tk.Entry(frame, width=30, font=("Poppins", 12))
    username_entry.grid(row=1, column=1, pady=5)

    # Email
    tk.Label(frame, text="Email", font=("Poppins", 12)).grid(row=2, column=0, sticky="w", pady=5)
    email_entry = tk.Entry(frame, width=30, font=("Poppins", 12))
    email_entry.grid(row=2, column=1, pady=5)

    # Phone Number
    tk.Label(frame, text="Phone Number", font=("Poppins", 12)).grid(row=3, column=0, sticky="w", pady=5)
    phone_entry = tk.Entry(frame, width=30, font=("Poppins", 12))
    phone_entry.grid(row=3, column=1, pady=5)

    # Password
    tk.Label(frame, text="Password", font=("Poppins", 12)).grid(row=4, column=0, sticky="w", pady=5)
    pass_entry = tk.Entry(frame, width=30, font=("Poppins", 12), show="*")
    pass_entry.grid(row=4, column=1, pady=5)

    # Button Frame
    button_frame = tk.Frame(root)
    button_frame.pack(padx=20, pady=10)

    signup_button = tk.Button(button_frame, text="Register", font=("Poppins", 12), bg="#1565C0", fg="white",
                              command=lambda: register_user(username_entry.get(), email_entry.get(), phone_entry.get(),
                                                            pass_entry.get()))

    signup_button.grid(row=0, column=0, padx=5)

    back_button = tk.Button(button_frame, text="Back to Login Page", font=("Poppins", 12), bg="gray", fg="white",
                            command=show_login_screen)
    back_button.grid(row=0, column=1, padx=5)

def send_otp(email_or_phone):
    otp = str(random.randint(1000, 9999))
    messagebox.showinfo("OTP Sent", f"Your OTP is: {otp}")
    return otp


def reset_password(email_or_phone, new_password):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET Password=%s WHERE Email=%s OR Phone_number=%s",
                   (new_password, email_or_phone, email_or_phone))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Password reset successfully! Please login with your new password.")
    show_login_screen()


def show_forgot_password_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Forgot Password", font=("Poppins", 20, "bold")).pack(pady=20)

    tk.Label(root, text="Enter Email / Phone Number", font=("Poppins", 12)).pack()
    email_phone_entry = tk.Entry(root, width=30, font=("Poppins", 12))
    email_phone_entry.pack(pady=5, ipady=5)

    def handle_otp():
        email_or_phone = email_phone_entry.get()
        if not email_or_phone.strip():
            messagebox.showerror("Error", "Email or Phone Number is required!")
            return
        global sent_otp
        sent_otp = send_otp(email_or_phone)
        show_otp_screen(email_or_phone)

    send_otp_button = tk.Button(root, text="Send OTP", font=("Poppins", 12), bg="#1565C0", fg="white",
                                command=handle_otp)
    send_otp_button.pack(pady=10)

    back_button = tk.Button(root, text="Back to Login Page", font=("Poppins", 12), bg="gray", fg="white",
                            command=show_login_screen)
    back_button.grid(row=0, column=1, padx=5)



def show_otp_screen(email_or_phone):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Enter OTP", font=("Poppins", 12)).pack()
    otp_entry = tk.Entry(root, width=30, font=("Poppins", 12))
    otp_entry.pack(pady=5, ipady=5)


def show_reset_password_screen(email_or_phone):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Reset Password", font=("Poppins", 20, "bold")).pack(pady=20)

    tk.Label(root, text="New Password", font=("Poppins", 12)).pack()
    new_password_entry = tk.Entry(root, width=30, font=("Poppins", 12), show="*")
    new_password_entry.pack(pady=5, ipady=5)

    tk.Label(root, text="Re-type Password", font=("Poppins", 12)).pack()
    retype_password_entry = tk.Entry(root, width=30, font=("Poppins", 12), show="*")
    retype_password_entry.pack(pady=5, ipady=5)

    def confirm_reset():
        new_password = new_password_entry.get()
        retype_password = retype_password_entry.get()
        if new_password != retype_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        reset_password(email_or_phone, new_password)

    reset_button = tk.Button(root, text="Reset Password", font=("Poppins", 12), bg="#1565C0", fg="white",
                             command=confirm_reset)
    reset_button.pack(pady=10)

def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    header_frame = tk.Frame(root, bg="#D8BFD8", height=50)
    header_frame.pack(fill="x")

    signup_button = tk.Button(header_frame, text="Sign Up", font=("Poppins", 12), bg=root.cget("bg"),
                              command=show_sign_up_screen)
    signup_button.pack(side="right", padx=10, pady=10)

    tk.Label(root, text="Login", font=("Poppins", 20, "bold")).pack(pady=20)

    # Use "Email" instead of "First Name" (Fix)
    tk.Label(root, text="Email / Phone_number",font=("Poppins", 12)).place(x=95,y=150)
    email_entry = tk.Entry(root, width=30, font=("Poppins", 12))
    email_entry.pack(pady=15,ipady=5)

    tk.Label(root, text="Password", font=("Poppins", 12)).place(x=180,y=210)
    password_entry = tk.Entry(root, width=30,font=("Poppins", 12), show="*")
    password_entry.pack(pady=15, ipady=5)

    # Fix: Pass email_entry.get() instead of first_name_entry.get()
    login_button = tk.Button(root, text="Login", font=("Poppins", 12), bg="#1565C0", fg="white",
                             command=lambda: login_user(email_entry.get(), password_entry.get()))
    login_button.pack(pady=18)
    forgot_password_button = tk.Button(root, text="Forgot Password?", font=("Poppins", 10), fg="blue",
                                       command=show_forgot_password_screen)
    forgot_password_button.pack(pady=5)






create_db()
show_login_screen()
root.mainloop()


