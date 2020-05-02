import os

# 设置其他域名，也许需要代理才可以访问， 比如：cordcloud.org
CC_HOST = ""

# 看情况是否开启代理
PROXIES = {
    # "http": "http://127.0.0.1:7890",
    # "https": "http://127.0.0.1:7890",
}

# 登录CordCloud的帐号密码
LOGIN_FORM = {
    "email": os.getenv("CC_EMAIL", ""),
    "passwd": os.getenv("CC_PASSWD", ""),
    "code": "",
}

# server酱配置(非必填)
SERVER_CHAN_CONFIG = {
    "enable": False,  # True打开
    "key": os.getenv("SERVER_CHAN_KEY", "")
}

# 日志文件位置（可以不改）
LOG_FILE = "./cc_auto_check_in.log"

# 邮件通知配置(非必填)
EMAIL_CONFIG = {
    "enable": False,  # True打开
    "user": os.getenv("CC_MAIL_USER", ""),  # 用于发送通知的邮箱
    "pw": os.getenv("CC_MAIL_PW", ""),  # 用于发送通知的邮箱密码
    "host": os.getenv("CC_MAIL_HOST", ""),  # SMTP服务的host
    "port": os.getenv("CC_MAIL_PORT"),  # SMTP服务的端口，默认端口可不填
    "receivers": [""],  # 接收人邮箱地址
}
