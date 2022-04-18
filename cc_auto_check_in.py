# coding: utf-8
import requests
import json
import logging

import yagmail
from requests import HTTPError

CONFIG_FILE_NAME = "config.json"


class Config:
    def __init__(self, config_file: str):
        with open(config_file, "r") as f:
            data = f.read()

        self._config = json.loads(data)
        for k in self._config:
            self.__setattr__(k, self._config[k])


try:
    cfg = Config(CONFIG_FILE_NAME)
except Exception as err:
    print("{}: use config.py now".format(err))
    import config as cfg

formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
file_handler = logging.FileHandler(filename=cfg.LOG_FILE, encoding='utf-8')
file_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

NOTIFY_MSG_PREFIX = "[CordCloud 续命通知]"


class ServerChan:
    """
    server 酱通知
    """

    def __init__(self, key):
        self._server_url = f"https://sc.ftqq.com/{key}.send"

    def send_msg(self, text: str, desp: str = ""):
        resp = requests.post(self._server_url, data={"text": text, "desp": desp})
        resp.raise_for_status()


class CordCloudClient:
    LOGIN_PATH = "/auth/login"
    CHECK_IN_PATH = "/user/checkin"

    def __init__(self, login_form, host="", proxies=None, server_chan_config=None, email_config=None):
        self._login_form = login_form
        self._host = host if host else "cordcloud.site"
        self._sess = requests.session()

        self.proxies = proxies
        self._server_chan_config = server_chan_config
        self._email_config = email_config

        self._server_chan = None
        self._yagmail = None

        self._init_server_chan()
        self._init_yagmail()

    def _init_server_chan(self):
        self._server_chan = ServerChan(
            self._server_chan_config["key"]
        ) if self._server_chan_config["enable"] else None

    def _init_yagmail(self):
        self._yagmail = yagmail.SMTP(
            user=self._email_config["user"],
            password=self._email_config["pw"],
            host=self._email_config["host"],
            port=self._email_config["port"],
        ) if self._email_config["enable"] else None

    @staticmethod
    def _get_msg(resp_content: bytes):
        return json.loads(str(resp_content, encoding='utf-8')).get("msg", "")

    def _notify(self, msg):
        text = ": ".join([NOTIFY_MSG_PREFIX, msg])

        if self._server_chan:
            try:
                self._server_chan.send_msg(text=text)
            except Exception as err:
                logger.error(str(err))

        if self._yagmail:
            try:
                self._yagmail.send(self._email_config["receivers"], text, text)
            except Exception as err:
                logger.error(str(err))

    def _login(self) -> bool:
        resp = self._sess.post(
            "".join(["http://", self._host, self.LOGIN_PATH]),
            data=self._login_form,
            proxies=self.proxies,
        )
        try:
            resp.raise_for_status()
        except HTTPError as err:
            msg = "login failed! {}".format(err)
            logger.error(msg)
            self._notify(msg)
            return False

        print(self._get_msg(resp.content))
        return True

    def _check_in(self):
        resp = self._sess.post("".join(["http://", self._host, self.CHECK_IN_PATH]), proxies=self.proxies)
        try:
            resp.raise_for_status()
        except HTTPError as err:
            msg = "check in failed! {}".format(err)
            logger.error(msg)
            self._notify(msg)
            return

        msg = self._get_msg(resp.content)
        print(msg)
        logger.info(msg)
        self._notify(msg)  # 通知结果

    def check_in(self):
        if not self._login():
            return
        self._check_in()


if __name__ == '__main__':
    CordCloudClient(
        cfg.LOGIN_FORM,
        host=cfg.CC_HOST,
        proxies=cfg.PROXIES,
        server_chan_config=cfg.SERVER_CHAN_CONFIG,
        email_config=cfg.EMAIL_CONFIG,
    ).check_in()
