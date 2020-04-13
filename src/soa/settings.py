import os

env = os.environ.get
base_domain = env("BASE_DOMAIN")
cookie_kwargs = {"path": "/", "domain": base_domain} if base_domain is not None else {}

database_url = env("DATABASE_URL")
redis_host = env("REDIS_HOST")
secret = env("BOTTLE_SECRET", "this is no secret")
cookie_name = "soa-token"
mailer_credentials = env("MAILER_CREDENTIALS")
if mailer_credentials is not None:
    with open("credentials.json", "w") as fl:
        fl.write(mailer_credentials)
