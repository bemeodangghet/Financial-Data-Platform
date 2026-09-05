import os
from dotenv import load_dotenv


load_dotenv()

EXCHANGE_RATE_API_URL = os.getenv("EXCHANGE_RATE_API_URL")

REQUEST_TIMEOUT = 10


