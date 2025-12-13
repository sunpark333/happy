# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
# wtite up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = int(getenv("API_ID", "34080993"))
API_HASH = getenv("API_HASH", "a2b9a77aa510a94dd6ad0e467c51ee7c")
BOT_TOKEN = getenv("BOT_TOKEN", "8270781366:AAEkDcNNnCSdrfZ-GcBNruVXdZSyVk1XcKQ")
OWNER_ID = list(map(int, getenv("OWNER_ID", "6127154811").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://riderits57_db_user:HDylKADKpgmUGbDF@pushpabhau.vkuiapi.mongodb.net/?appName=pushpabhau")
LOG_GROUP = getenv("LOG_GROUP", "-1003313824760")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1003322366997"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500"))
WEBSITE_URL = getenv("WEBSITE_URL", "upshrink.com")
AD_API = getenv("AD_API", "52b4a2cf4687d81e7d3f8f2b7bc2943f618e78cb")
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", YTUB_COOKIES)
DEFAULT_SESSION = getenv("DEFAULT_SESSION", None)  # added old method of invite link joining
INSTA_COOKIES = getenv("INSTA_COOKIES", INST_COOKIES)
