import os

env = os.environ.get

base_domain = env("BASE_DOMAIN")
# From ENV
cookie_kwargs = {"path": "/", "domain": base_domain}
database_url = env("DATABASE_URL")
redis_url = env("REDIS_URL")
secret = env("BOTTLE_SECRET", "this is no secret")
gmail_app_pwd = env("GMAIL_APP_PASSWORD")


# Constants
gmail_email = "pyjaipur.india@gmail.com"
cookie_name = "soa-token"
protocol = "https"

is_dev = base_domain is None
if is_dev:
    cookie_kwargs = {}
    base_domain = "localhost:8000"
    protocol = "http"
