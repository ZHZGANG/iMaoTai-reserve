import requests
# create an interface class for notification
class NotificationInterface:
    def send(self, title: str, body: str) -> (bool, str):
        raise NotImplementedError

# # 消息推送
# def send_msg(title, content):
#     if config.PUSH_TOKEN is None:
#         return
#     url = 'http://www.pushplus.plus/send'
#     r = requests.get(url, params={'token': config.PUSH_TOKEN,
#                                   'title': title,
#                                   'content': content})
#     logging.info(f'通知推送结果：{r.status_code, r.text}')

class InvalidTokenError(Exception):
    pass

class PushplusNotifier(NotificationInterface):
    """
    a concrete class for pushplus notification
    """
    def __init__(self, token: str, url: str = 'http://www.pushplus.plus/send'):
        if not token:
            raise InvalidTokenError('Pushplus token is not provided.')
        self.token = token
        self.url = url
    def send(self, title: str, body: str) -> (bool,str):
        params = {
            'token': self.token,
            'title': title,
            'content': body
        }
        resp = requests.get(self.url, params=params)
        return True if resp.status_code == 200 else False, resp.text

