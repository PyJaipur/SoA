from soa import settings
import logging
import smtplib
from textwrap import dedent

log = logging.getLogger("main")


def send(*, to, subject, message):
    gmail_sender = "pyjaipur.india@gmail.com"
    gmail_passwd = settings.gmail_app_pwd

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    body = "\r\n".join(
        [
            "To: %s" % to,
            "From: PyJaipur <%s>" % gmail_sender,
            "Subject: %s" % subject,
            "",
            message,
        ]
    )
    try:
        server.sendmail(gmail_sender, [to], body)
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
