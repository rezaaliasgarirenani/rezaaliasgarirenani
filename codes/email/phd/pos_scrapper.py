from __future__ import annotations

import re
import urllib.request
from html import unescape
from typing import Optional

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


# Clean a PhD subject line by removing generic prefixes.
def clean_phd_subject(subject: str) -> str:
    subject = normalize_text(subject)
    subject = re.sub(
        r"^ph\.?d\.?\s+positions?\s+(?:in|on|for)\s+",
        "",
        subject,
        flags=re.IGNORECASE,
    )
    subject = re.sub(
        r"^ph\.?d\.?\s+positions?\s+",
        "",
        subject,
        flags=re.IGNORECASE,
    )
    return subject.strip(" -–—:|")


# Normalize whitespace in extracted text.
def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


# Remove any HTML tags from a text fragment.
def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


# Parse meta tags into attribute dictionaries.
def parse_meta_tags(html: str) -> list[dict[str, str]]:
    tags: list[dict[str, str]] = []
    for tag in re.findall(r"<meta\b[^>]*>", html, flags=re.IGNORECASE):
        attrs = {}
        for key, value in re.findall(r'([a-zA-Z:-]+)\s*=\s*["\'](.*?)["\']', tag):
            attrs[key.lower()] = unescape(value)
        if attrs:
            tags.append(attrs)
    return tags


# Extract a meta content value by attribute key/value pair.
def extract_meta_content(html: str, key: str, value: str) -> Optional[str]:
    key = key.lower()
    value = value.lower()
    for attrs in parse_meta_tags(html):
        if attrs.get(key, "").lower() == value:
            content = attrs.get("content")
            if content:
                return normalize_text(content)
    return None


# Extract the HTML <title> value.
def extract_title(html: str) -> Optional[str]:
    match = re.search(r"<title\b[^>]*>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    return normalize_text(strip_tags(unescape(match.group(1))))


# Extract the first <h1> value.
def extract_h1(html: str) -> Optional[str]:
    match = re.search(r"<h1\b[^>]*>(.*?)</h1>", html, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    return normalize_text(strip_tags(unescape(match.group(1))))


# Guess a university name from a title-like string.
def guess_university_from_title(text: str) -> Optional[str]:
    for separator in [" - ", " | ", " — ", " – "]:
        if separator in text:
            candidate = text.split(separator)[-1].strip()
            if 3 <= len(candidate) <= 80:
                return candidate
    match = re.search(r"\bat\s+([^,;|]+)", text, flags=re.IGNORECASE)
    if match:
        return normalize_text(match.group(1))
    return None


# Fetch the HTML content for a given URL.
def fetch_html(url: str, timeout: int = 10) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; phd-email/1.0)"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


# Extract possible email addresses from HTML.
def extract_email_candidates(html: str) -> list[str]:
    candidates: list[str] = []

    for match in re.findall(r"mailto:([^\"'>\s]+)", html, flags=re.IGNORECASE):
        email = unescape(match.split("?", 1)[0])
        if EMAIL_REGEX.fullmatch(email):
            candidates.append(email)

    for match in EMAIL_REGEX.findall(html):
        candidates.append(match)

    seen = set()
    unique: list[str] = []
    for email in candidates:
        if email not in seen:
            seen.add(email)
            unique.append(email)
    return unique


# Extract a last name candidate from an email address.
def extract_last_name_from_email(email: str) -> Optional[str]:
    local = email.split("@", 1)[0]
    parts = [part for part in re.split(r"[._-]+", local) if part]
    for part in reversed(parts):
        if len(part) >= 2 and part.isalpha():
            return part.capitalize()
    return None


# Extract a professor email from HTML.
def extract_professor_email_from_html(html: str) -> Optional[str]:
    emails = extract_email_candidates(html)
    if emails:
        return emails[0]
    return None


# Extract a professor last name from HTML.
def extract_professor_last_name_from_html(html: str) -> Optional[str]:
    email = extract_professor_email_from_html(html)
    if not email:
        return None
    return extract_last_name_from_email(email)


# Extract a PhD subject from HTML.
def extract_phd_subject_from_html(html: str) -> Optional[str]:
    for key, value in [("property", "og:title"), ("name", "twitter:title")]:
        meta_title = extract_meta_content(html, key, value)
        if meta_title:
            return clean_phd_subject(meta_title)
    heading = extract_h1(html) or extract_title(html)
    if heading:
        return clean_phd_subject(heading)
    return None


# Extract a university name from HTML.
def extract_university_name_from_html(html: str) -> Optional[str]:
    for key, value in [
        ("property", "og:site_name"),
        ("name", "application-name"),
        ("name", "site_name"),
    ]:
        meta_site = extract_meta_content(html, key, value)
        if meta_site:
            return meta_site

    title = extract_title(html) or ""
    university = guess_university_from_title(title)
    if university:
        return university

    h1_text = extract_h1(html) or ""
    return guess_university_from_title(h1_text)


# Attempt to find a professor email from a job post URL.
def extract_professor_email(url: str) -> Optional[str]:
    html = fetch_html(url)
    return extract_professor_email_from_html(html)


# Extract all job details needed for the email from a URL.
def extract_job_details(url: str) -> dict[str, Optional[str]]:
    html = fetch_html(url)
    return {
        "professor_email": extract_professor_email_from_html(html),
        "professor_last_name": extract_professor_last_name_from_html(html),
        "phd_subject": extract_phd_subject_from_html(html),
        "university_name": extract_university_name_from_html(html),
    }
