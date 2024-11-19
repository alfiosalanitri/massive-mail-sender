import smtplib
import re
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.secret_key = os.urandom(24)

def load_configuration():
    load_dotenv(override=True)
    return {
        "login_password": os.getenv("LOGIN_PASSWORD"),
        "smtp_server": os.getenv("SMTP_SERVER"),
        "smtp_port": int(os.getenv("SMTP_PORT")),
        "smtp_user": os.getenv("SMTP_USER"),
        "smtp_password": os.getenv("SMTP_PASSWORD"),
        "mail_from": os.getenv("MAIL_FROM")
    }

# Load configs
app.config['APP_CONFIGS'] = load_configuration()

# Validate mail address
def is_valid_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

# Send mail to address
def send_email(email, subject, smtp_details, html_content, errors):
    if not is_valid_email(email):
        errors.append(f"Not valid mail: {email}")
        return
    
    msg = MIMEMultipart("alternative")
    msg["From"] = smtp_details["mail_from"]
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(smtp_details["smtp_server"], smtp_details["smtp_port"]) as server:
            server.starttls()
            server.login(smtp_details["smtp_user"], smtp_details["smtp_password"])
            server.sendmail(smtp_details["smtp_user"], email, msg.as_string())
        print(f"Email sent to: {email}")
    except Exception as e:
        errors.append(f"Email sent error {email}: {e}")
        print(f"Email sent error {email}: {e}")

@app.route("/", methods=["GET", "POST"])
def index():

    # only auth user
    if not session.get('logged_in'):
        return render_template('login.html')

    if request.method == "POST":

        email_list = request.form["email_list"].splitlines()
        subject = request.form["subject"]
        html_content = request.form["html_content"]
        
        errors = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(send_email, email, subject, app.config['APP_CONFIGS'], html_content, errors) for email in email_list]

            for future in futures:
                future.result()

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            flash("Emails sent with success!", "success")
        return redirect(url_for("index"))
    
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route('/do_login', methods=['POST'])
def do_admin_login():
    password = request.form['password']
    if password == app.config['APP_CONFIGS']['login_password']:
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        flash('Wrong password!', "error")
        return redirect(url_for('login')) 

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)