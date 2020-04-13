import base64
import pickle
import os.path
from textwrap import dedent
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText


# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def send(*, to, subject, message):
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    service = build("gmail", "v1", credentials=creds)
    m = MIMEText(message)
    m["to"] = to
    m["from"] = "pyjaipur.india@gmail.com"
    m["subject"] = subject
    b = m.as_string().encode()
    payload = {"raw": base64.urlsafe_b64encode(b).decode()}
    r = service.users().messages().send(userId="me", body=payload).execute()


def send_otp(to, otp):
    message = dedent(
        f"""\
    Hello,

    Please open this url in your browser to login to Summer of Algorithms.

    https://soa.pyjaipur.org/otp?q={ otp }

    Thanks,
    PyJaipur
    """
    )
    send(to=to, subject="[SoA] Login link", message=message)
