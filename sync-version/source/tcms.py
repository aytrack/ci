import os
import yaml
import requests
import time


class Tcms(object):
    """
    user interface to Tcms
    """
    def __init__(self, token=None):
        if token is None:
            # use default token in ${HOME}/.tcctl.yml
            tcctl_config_path = os.getenv("HOME", "/root") + "/.tcctl.yml"
            print("use {}".format(tcctl_config_path))
            f = open(tcctl_config_path)
            data = yaml.load(f, Loader=yaml.Loader)
            f.close()
            
            self.token = data["token"]
        else:
            self.token = token

    def case_versions(self, trigger_id):
        """ get case's version info in tcms

        :param trigger_id: the command of tcctl run will return trigger_id
        :return: cases slice
        """
        self.wait(trigger_id)

        res = requests.get("https://tcms.pingcap.net/api/v1/triggers/{}/affected-version/cases".format(trigger_id),
                           headers={"Authorization": "Bearer {}".format(self.token)})
        if res.status_code != 200:
            raise Exception("requests exception")

        return res.json()["cases"]

    def wait(self, trigger_id):
        """ wait tcms job done

        :param trigger_id: the command of tcctl run will return trigger_id
        :return: None
        """
        for i in range(3600):
            print("sleep 10 seconds")
            time.sleep(10)
            res = requests.get("https://tcms.pingcap.net/api/v1/plan-executions?trigger_ids={}&count=100".format(trigger_id),
                               headers={"Authorization": "Bearer {}".format(self.token)})

            if res.status_code != 200:
                print("unknown status_code {}".format(res.status_code))
                continue

            done = True
            for item in res.json()["data"]:
                print(item["status"])
                if item["status"].lower() not in ["failure", "success", "error", "cancelled"]:
                    done = False
                    break
            if done:
                return

        raise Exception("waiting time is too long")
