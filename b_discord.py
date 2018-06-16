import clan_config
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

url = clan_config.discord_webhook_url
users = clan_config.discord_users

def post(message):
    msg = DHook(url,msg=message)
    msg.post()

def id_with_mention(cr_name):
    cr_name = cr_name.lower()
    if cr_name in users:
        return '<@{}>'.format(users.get(cr_name).get('id'))
    else:
        return cr_name

def is_discord_user(cr_name):
    cr_name = cr_name.lower()
    return cr_name in users