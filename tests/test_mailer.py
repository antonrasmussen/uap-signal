from uap_signal.config import Settings
from uap_signal.mailer import markdown_to_email_html, send_email, send_failure_alert


def _settings(**overrides) -> Settings:
    base = dict(
        database_path=".uap_signal.db",
        provider="openai",
        anthropic_api_key=None,
        openai_api_key="sk-test",
        model="gpt-4.1-mini",
        max_items=25,
        request_timeout_seconds=30,
        email_provider="smtp",
        email_from="from@example.com",
        email_to="to@example.com",
        alert_email_to="alert@example.com",
        smtp_host="smtp.gmail.com",
        smtp_port=587,
        smtp_user="from@example.com",
        smtp_password="app-password",
        resend_api_key="",
        reports_dir="reports",
        state_dir="state",
    )
    base.update(overrides)
    return Settings(**base)


def test_markdown_to_email_html_wraps_body():
    html = markdown_to_email_html("# Hello\n\nWorld", title="Test")
    assert "<h1>Hello</h1>" in html
    assert "World" in html
    assert "<!DOCTYPE html>" in html


def test_send_email_smtp_success(monkeypatch):
    calls = {}

    class FakeSMTP:
        def __init__(self, host, port):
            calls["host"] = host
            calls["port"] = port

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def starttls(self):
            calls["tls"] = True

        def login(self, user, password):
            calls["login"] = (user, password)

        def sendmail(self, sender, recipients, message):
            calls["sender"] = sender
            calls["recipients"] = recipients
            calls["message"] = message

    monkeypatch.setattr("uap_signal.mailer.smtplib.SMTP", FakeSMTP)
    ok = send_email(_settings(), "Subject", "<p>hi</p>", "hi")
    assert ok is True
    assert calls["host"] == "smtp.gmail.com"
    assert calls["recipients"] == ["to@example.com"]
    assert "Subject" in calls["message"]


def test_send_email_resend_provider(monkeypatch):
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

    def fake_post(url, headers=None, json=None, timeout=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        return FakeResponse()

    monkeypatch.setattr("uap_signal.mailer.httpx.post", fake_post)
    ok = send_email(
        _settings(email_provider="resend", resend_api_key="re_test"),
        "Subject",
        "<p>hi</p>",
        "hi",
    )
    assert ok is True
    assert captured["url"] == "https://api.resend.com/emails"
    assert captured["json"]["to"] == ["to@example.com"]


def test_send_failure_alert_uses_alert_recipient(monkeypatch):
    seen = {}

    def fake_send(settings, subject, html_body, text_body, to=None):
        seen["subject"] = subject
        seen["to"] = to
        return True

    monkeypatch.setattr("uap_signal.mailer.send_email", fake_send)
    send_failure_alert(_settings(), "boom")
    assert seen["to"] == "alert@example.com"
    assert "FAILED" in seen["subject"]
