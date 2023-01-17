
class jsonPayload:
    def __init__(self, app_url, response_code, timestamp):
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