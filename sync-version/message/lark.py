import requests


class Lark(object):
    def __init__(self):
        pass

    @staticmethod
    def send(head, lines):
        elements = []
        for line in lines:
            if len(elements) != 0:
                elements.append("""{"tag": "hr" }""")
            elements.append('''{
              "tag": "div",
              "fields": [
                {
                  "is_short": false,
                  "text": {
                    "tag": "lark_md",
                    "content": "%s"
                  }
                }
              ]
            }''' % line)

        data = """
        {
            "msg_type": "interactive",
            "card": {
                "config": {
                        "wide_screen_mode": true,
                        "enable_forward": true
                },
                "elements": [%s],
                "header": {
                        "title": {
                                "content": "%s",
                                "tag": "plain_text"
                        }
                }
            }
        } """ % (",".join(elements), head)

        print(data)
        res = requests.post("https://open.feishu.cn/open-apis/bot/v2/hook/00e93570-c21a-464a-a0b9-6a708eb5d6cc", data=data,
                            headers={"Content-Type": "application/json"})
        if res.status_code != 200:
            raise Exception("send lark message failed")
