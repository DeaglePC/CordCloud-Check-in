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

SERVER_CHAN_CONFIG = {
    "enable": False,
    "key": os.getenv("SERVER_CHAN_KEY", "")
}

LOG_FILE = "./cc_auto_check_in.log"

EMAIL_CONFIG = {
    "enable": False,
    "user": os.getenv("CC_MAIL_USER", ""),
    "pw": os.getenv("CC_MAIL_PW", ""),
    "host": os.getenv("CC_MAIL_HOST", ""),
    "port": os.getenv("CC_MAIL_PORT"),
    "receivers": [""],
}
