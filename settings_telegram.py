import os

from dotenv import load_dotenv
load_dotenv()


URL = os.getenv('URL')
TOKEN = os.getenv("TOKEN")

SOCKS5_PROXY = os.getenv('SOCKS5_PROXY')
LOGIN_PROXY = os.getenv('LOGIN_PROXY')
PASSWORD_PROXY = os.getenv('PASSWORD_PROXY')
