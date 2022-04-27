import requests


class Lark(object):
    def __init__(self):
        pass

    @staticmethod
    def send_message(data):
        print(data)
        res = requests.post("https://open.feishu.cn/open-apis/bot/v2/hook/00e93570-c21a-464a-a0b9-6a708eb5d6cc", data=data,
                            headers={"Content-Type": "application/json"})
        if res.status_code != 200:
            import pdb
            pdb.set_trace()
            raise Exception("send lark message failed")
