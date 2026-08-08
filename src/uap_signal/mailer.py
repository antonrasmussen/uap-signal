"""Email sending via SMTP or Resend."""

from __future__ import annotations

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import httpx
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

from uap_signal.config import Settings

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"


def markdown_to_email_html(md_text: str, title: str | None = None) -> str:
    body_html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("email_wrapper.html.j2")
    return template.render(title=title or "UAP Signal", body_html=body_html)


def send_email(
    settings: Settings,
    subject: str,
    html_body: str,
    text_body: str,
    to: str | None = None,
) -> bool:
    recipient = to or settings.email_to
    if not recipient:
        logger.error("EMAIL_TO is not configured")
        return False

    provider = (settings.email_provider or "smtp").lower()
    if provider == "resend":
        return _send_resend(settings, subject, html_body, text_body, recipient)
    return _send_smtp(settings, subject, html_body, text_body, recipient)


def send_markdown_email(
    settings: Settings,
    subject: str,
    markdown_body: str,
    to: str | None = None,
) -> bool:
    html_body = markdown_to_email_html(markdown_body, title=subject)
    return send_email(settings, subject, html_body, markdown_body, to=to)


def _send_smtp(
    settings: Settings,
    subject: str,
    html_body: str,
    text_body: str,
    recipient: str,
) -> bool:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.email_from
    msg["To"] = recipient
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            if settings.smtp_user and settings.smtp_password:
                server.login(settings.smtp_user, settings.smtp_password)
            server.sendmail(settings.email_from, [recipient], msg.as_string())
        logger.info("Email sent via SMTP to %s", recipient)
        return True
    except Exception as exc:
        logger.error("SMTP send failed: %s", exc)
        return False


def _send_resend(
    settings: Settings,
    subject: str,
    html_body: str,
    text_body: str,
    recipient: str,
) -> bool:
    if not settings.resend_api_key:
        logger.error("RESEND_API_KEY not configured")
        return False

    try:
        response = httpx.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {settings.resend_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": settings.email_from,
                "to": [recipient],
                "subject": subject,
                "html": html_body,
                "text": text_body,
            },
            timeout=30,
        )
        response.raise_for_status()
        logger.info("Email sent via Resend to %s", recipient)
        return True
    except Exception as exc:
        logger.error("Resend send failed: %s", exc)
        return False


def send_failure_alert(settings: Settings, error_message: str) -> None:
    alert_to = settings.alert_email_to or settings.email_to
    subject = "[ALERT] UAP Signal Pipeline FAILED"
    body = f"The uap-signal daily pipeline failed.\n\nError:\n{error_message}"
    send_email(settings, subject, f"<pre>{body}</pre>", body, to=alert_to)
