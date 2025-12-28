from __future__ import annotations

import smtplib
from email.message import EmailMessage
from pathlib import Path

# Sender email address used for Gmail SMTP and app-specific password.
SENDER_EMAIL = "rezaaliasgarirenani@gmail.com"
SENDER_PASSWORD = "obcl ldkm nrhv twak"


# Verify the Gmail SMTP connection and credentials.
def check_gmail_connection(sender: str, app_password: str) -> None:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)


# Load the template text from disk.
def load_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# Render the template by replacing placeholders with real values.
def render_template(template: str, professor_last_name: str, phd_subject: str) -> str:
    replacements = {
        "[Professor's Last Name]": professor_last_name,
        "[Subject of the PhD position]": phd_subject,
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


# Build an email message with headers and body.
def build_message(sender: str, recipient: str, subject: str, body: str) -> EmailMessage:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)
    return message


# Send the email through Gmail SMTP using an app password.
def send_via_gmail(message: EmailMessage, app_password: str) -> None:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(message["From"], app_password)
        server.send_message(message)


# Collect inputs, render the email, and optionally send it.
def main() -> None:
    print("Stage 0: connecting to sender email.")
    check_gmail_connection(SENDER_EMAIL, SENDER_PASSWORD)
    print("Stage 0: connected to sender email.")

    template_path = Path(__file__).with_name("email_template.txt")
    template = load_template(template_path)

    professor_last_name = input("Professor last name: ").strip()
    professor_email = input("Professor email: ").strip()
    phd_subject = input("PhD position subject: ").strip()
    email_subject = input("Email subject: ").strip()
    print("Stage 1: target email, name, subject received.")

    body = render_template(template, professor_last_name, phd_subject)
    message = build_message(SENDER_EMAIL, professor_email, email_subject, body)
    print("Stage 2: email draft completed.")

    print("\n--- Preview ---\n")
    print(body)
    print("\n--- End Preview ---\n")

    confirm = input("Send this email now? (yes/no): ").strip().lower()
    if confirm == "yes":
        print("Email accepted to be sent.")
        send_via_gmail(message, SENDER_PASSWORD)
        print("Stage 3: email sent.")
    else:
        print("Canceled, not sent.")


# Run the script when executed directly.
if __name__ == "__main__":
    main()
