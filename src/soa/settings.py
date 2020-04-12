import os

env = os.environ.get

database_url = env("DATABASE_URL")
redis_host = env("REDIS_HOST")
