from __future__ import annotations

import mimetypes
import smtplib
from email.message import EmailMessage
from pathlib import Path

from phd_email_scraper import extract_job_details

# Sender email address used for Gmail SMTP and app-specific password.
SENDER_EMAIL = "rezaaliasgarirenani@gmail.com"
SENDER_PASSWORD = "obcl ldkm nrhv twak"
# CV PDF path to attach.
CV_PATH = "/home/reza-aliasgari-renani/Downloads/CV_Reza_Aliasgari_Renani.pdf"
# Job posting URL used to try automatic email extraction.
JOB_URL = "https://oulunyliopisto.varbi.com/en/what:job/jobID:882192/"
# Email subject used for all outgoing messages.
EMAIL_SUBJECT = "PhD Applicant"


# Verify the Gmail SMTP connection and credentials.
def check_gmail_connection(sender: str, app_password: str) -> None:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)


# Load the template text from disk.
def load_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# Render the template by replacing placeholders with real values.
def render_template(
    template: str,
    professor_last_name: str,
    phd_subject: str,
    university_name: str,
) -> str:
    replacements = {
        "[Professor's Last Name]": professor_last_name,
        "[Subject of the PhD position]": phd_subject,
        "[University Name]": university_name,
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


# Build an email message with headers and body.
def build_message(
    sender: str,
    recipient: str,
    subject: str,
    body: str,
    cv_path: Path,
) -> EmailMessage:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    mime_type, _ = mimetypes.guess_type(cv_path.name)
    if mime_type:
        maintype, subtype = mime_type.split("/", 1)
    else:
        maintype, subtype = "application", "octet-stream"

    cv_data = cv_path.read_bytes()
    message.add_attachment(cv_data, maintype=maintype, subtype=subtype, filename=cv_path.name)
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

    job_url = JOB_URL.strip()
    professor_last_name = ""
    professor_email = ""
    phd_subject = ""
    university_name = ""
    if job_url:
        print("Stage 1: attempting to extract details from URL.")
        try:
            scraped = extract_job_details(job_url)
        except Exception as exc:
            print(f"Stage 1: failed to read URL: {exc}")
            scraped = {}

        scraped_email = scraped.get("professor_email")
        if scraped_email:
            print(f"Stage 1: professor email extracted: {scraped_email}")
            use_extracted = input("Use this email? (yes/no): ").strip().lower()
            if use_extracted == "yes":
                professor_email = scraped_email
        else:
            print("Stage 1: no professor email found; please enter it manually.")

        scraped_last_name = scraped.get("professor_last_name")
        if scraped_last_name:
            print(f"Stage 1: professor last name extracted: {scraped_last_name}")
            use_extracted = input("Use this last name? (yes/no): ").strip().lower()
            if use_extracted == "yes":
                professor_last_name = scraped_last_name
        else:
            print("Stage 1: no professor last name found; please enter it manually.")

        scraped_subject = scraped.get("phd_subject")
        if scraped_subject:
            print(f"Stage 1: PhD subject extracted: {scraped_subject}")
            use_extracted = input("Use this PhD subject? (yes/no): ").strip().lower()
            if use_extracted == "yes":
                phd_subject = scraped_subject
        else:
            print("Stage 1: no PhD subject found; please enter it manually.")

        scraped_university = scraped.get("university_name")
        if scraped_university:
            print(f"Stage 1: university name extracted: {scraped_university}")
            use_extracted = input("Use this university name? (yes/no): ").strip().lower()
            if use_extracted == "yes":
                university_name = scraped_university
        else:
            print("Stage 1: no university name found; please enter it manually.")

    if not professor_last_name:
        professor_last_name = input("Professor last name: ").strip()
    if not professor_email:
        professor_email = input("Professor email: ").strip()
    if not phd_subject:
        phd_subject = input("PhD position subject: ").strip()
    if not university_name:
        university_name = input("University name: ").strip()
    email_subject = EMAIL_SUBJECT
    print("Stage 2: target email, name, subject, university received.")

    cv_path = Path(CV_PATH).expanduser()
    if not cv_path.is_file():
        raise SystemExit(f"CV file not found: {cv_path}")
    print(f"Stage 3: CV found and will be attached: {cv_path.name}")

    body = render_template(template, professor_last_name, phd_subject, university_name)
    message = build_message(SENDER_EMAIL, professor_email, email_subject, body, cv_path)
    print("Stage 4: email draft completed.")

    print("\n--- Preview ---\n")
    print(body)
    print("\n--- End Preview ---\n")

    confirm = input("Send this email now? (yes/no): ").strip().lower()
    if confirm == "yes":
        print("Email accepted to be sent.")
        send_via_gmail(message, SENDER_PASSWORD)
        print("Stage 5: email sent.")
    else:
        print("Canceled, not sent.")


# Run the script when executed directly.
if __name__ == "__main__":
    main()
