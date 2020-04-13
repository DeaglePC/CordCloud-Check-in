# coding: utf-8
import requests
import json
import logging

import yagmail
from requests import HTTPError

from config import LOGIN_FORM, LOG_FILE, SERVER_CHAN_CONFIG, PROXIES, EMAIL_CONFIG

formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
file_handler = logging.FileHandler(filename=LOG_FILE, encoding='utf-8')
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
    LOGIN_URL = "https://cordcloud.org/auth/login"
    CHECK_IN_URL = "https://cordcloud.org/user/checkin"

    def __init__(self, proxies=None, server_chan_config=None, email_config=None):
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
            user=EMAIL_CONFIG["user"],
            password=EMAIL_CONFIG["pw"],
            host=EMAIL_CONFIG["host"],
            port=EMAIL_CONFIG["port"],
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
        resp = self._sess.post(self.LOGIN_URL, data=LOGIN_FORM, proxies=self.proxies)
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
        resp = self._sess.post(self.CHECK_IN_URL, proxies=self.proxies)
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
        proxies=PROXIES,
        server_chan_config=SERVER_CHAN_CONFIG,
        email_config=EMAIL_CONFIG,
    ).check_in()
