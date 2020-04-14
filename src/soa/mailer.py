from soa import settings
import logging
import smtplib
from textwrap import dedent
import json

log = logging.getLogger("main")


def send(*, to, subject, message):
    if settings.is_dev:
        log.info(
            json.dumps({"to": to, "subject": subject, "message": message}, indent=2)
        )
        return
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(settings.gmail_email, settings.gmail_app_pwd)

    body = "\r\n".join(
        [
            "To: %s" % to,
            "From: PyJaipur <%s>" % settings.gmail_email,
            "Subject: %s" % subject,
            "",
            message,
        ]
    )
    try:
        server.sendmail(settings.gmail_email, [to], body)
    except Exception as e:
        log.exception(e)
    server.quit()


def send_otp(to, otp):
    message = dedent(
        f"""\
    Hello,

    Please open this url in your browser to login to Summer of Algorithms.

    { settings.protocol }://{ settings.base_domain }/otp?q={ otp }

    If you did not request a login link, please ignore this email.

    Thanks,
    PyJaipur
    """
    )
    send(to=to, subject="[SoA] Login link", message=message)
