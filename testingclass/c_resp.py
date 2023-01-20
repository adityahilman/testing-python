import requests

class jsonPayload:
    def __init__(self, app_url:str, response_code, timestamp:str):
        self.app_url = app_url
        self.response_code = response_code
        self.timestamp = timestamp
        

    def jsonDown(self):
        jsonDownPayload = {
            "incident": {
                "state": "open",
                "resource": {
                    "labels": {
                        "host": self.app_url,
                        "response_code": self.response_code,
                        "timestamp": self.timestamp
                    }
                }
            }		
        }

        print(jsonDownPayload)

        postWebhook = requests.post("http://localhost:9000/healthcheck-webhook", json=jsonDownPayload)
        return postWebhook

    def jsonUp(self):
        jsonUpPayload = {
            "incident": {
                "state": "closed",
                "resource": {
                    "labels": {
                        "host": self.app_url,
                        "response_code": self.response_code,
                        "timestamp": self.timestamp
                    }
                }
            }		
        }

        postWebhook = requests.post("http://localhost:9000/healthcheck-webhook", json=jsonUpPayload)
        return postWebhook