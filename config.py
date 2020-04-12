import os

PROXIES = {
    "http": "http://192.168.41.218:7890",
    "https": "http://192.168.41.218:7890",
}

LOGIN_FORM = {
    "email": os.getenv("CC_EMAIL", ""),
    "passwd": os.getenv("CC_PASSWD", ""),
    "code": "",
}

ENABLE_SERVER_CHAN = False
SERVER_CHAN_KEY = os.getenv("SERVER_JIANG_KEY", "")

LOG_FILE = "./cc_auto_check_in.log"
