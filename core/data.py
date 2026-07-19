import os

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
BOT_ID = os.environ.get('BOT_ID')
OWNER_ID = os.environ.get('OWNER_ID')
TELEGRAM = os.environ.get('TELEGRAM')
DONATE = os.environ.get('DONATE')
DISCORD = os.environ.get('DISCORD')
NICKNAME = os.environ.get('NICKNAME')
SURVIVAL = os.environ.get('SURVIVAL')
STOLB = os.environ.get('STOLB')