import os

env = os.environ.get
base_domain = env("BASE_DOMAIN")
is_dev = base_domain is None

cookie_kwargs = {"path": "/", "domain": base_domain}
protocol = "https"
if is_dev:
    cookie_kwargs = {}
    base_domain = "localhost:8000"
    protocol = "http"

database_url = env("DATABASE_URL")
redis_host = env("REDIS_HOST")
secret = env("BOTTLE_SECRET", "this is no secret")
cookie_name = "soa-token"
gmail_app_pwd = env("GMAIL_APP_PASSWORD")
