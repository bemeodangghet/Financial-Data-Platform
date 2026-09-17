import os

from dotenv import load_dotenv

load_dotenv()

METALS_API_URL = os.getenv("METALS_API_URL")

METAL_SYMBOLS = ["XAU", "XAG", "XPD", "HG", "XPT"]

REQUEST_TIMEOUT = 10