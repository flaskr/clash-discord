import json
import requests
import time

class DHook:
    def __init__(self, url, msg):
        self.url = url 
        self.msg = msg

    @property
    def json(self,*arg):
        data = {}
        if self.msg: data["content"] = self.msg
        if 'content' not in data:
            print('You cannot post an empty payload.')
        if empty: data['embeds'] = []
        return json.dumps(data, indent=4)

    def post(self):
        headers = {'Content-Type': 'application/json'}
        result = requests.post(self.url, data=self.json, headers=headers)
        if result.status_code == 400:
            print("Post Failed, Error 400")
        else:
            print("Payload delivered successfuly")
            print("Code : "+str(result.status_code))
            time.sleep(2)
