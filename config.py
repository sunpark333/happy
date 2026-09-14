# devgagan
# Credentials are read here in config.py.
# You can still override values from environment variables if needed.

from os import getenv


def _value(name, default):
    val = getenv(name)
    if val is not None and val != "":
        return val
    return default


def _int_value(name, default):
    val = _value(name, default)
    return int(val)


# VPS --- FILL COOKIES 🍪 in """ ... """ 
INST_COOKIES = """
# write your Instagram cookies here
"""

YTUB_COOKIES = """
# write your YouTube cookies here
"""

API_ID = _int_value("API_ID", "37407296")
API_HASH = _value("API_HASH", "41676d595a28fa85ca494c2a7af3f94e")
BOT_TOKEN = _value("BOT_TOKEN", "8967297114:AAGnkSWOwSZ50-YNNr1eu6RTh_Bo5TEsv5Q")
OWNER_ID = [
    int(owner_id)
    for owner_id in _value("OWNER_ID", "8632638153").replace(",", " ").split()
]
MONGO_DB = _value("MONGO_DB", "mongodb+srv://yadavronak504:YKTfRQ0qc2ZpcF8Z@cluster0.oanfyk2.mongodb.net/?appName=Cluster0")
LOG_GROUP = _value("LOG_GROUP", "-1003729200703")
CHANNEL_ID = _int_value("CHANNEL_ID", "-1004326829993")
FREEMIUM_LIMIT = _int_value("FREEMIUM_LIMIT", "10000")
PREMIUM_LIMIT = _int_value("PREMIUM_LIMIT", "50000")
WEBSITE_URL = _value("WEBSITE_URL", "")
AD_API = _value("AD_API", "")
STRING = _value("STRING", "") or None
YT_COOKIES = _value("YT_COOKIES", YTUB_COOKIES)
DEFAULT_SESSION = _value("DEFAULT_SESSION", "") or None
INSTA_COOKIES = _value("INSTA_COOKIES", INST_COOKIES)
