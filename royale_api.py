import http.client
import json
import clan_config

from datetime import datetime

api_key = clan_config.cr_api_key
current_war_url = "/clan/{}/war"
current_warlog_url = "/clan/{}/warlog"
clan_members_url = "/clan/{}?keys=members"
upcoming_chests_url = "/player/{}/chests?exclude=upcoming"

def get_json(url):
    conn = http.client.HTTPSConnection("api.royaleapi.com")
    headers = {
        'auth': api_key,
        }
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    decoded_data = data.decode("utf-8")
    return json.loads(decoded_data)

def get_war_data(clan_id):
    current_war_request_url = current_war_url.format(clan_id)
    return get_json(current_war_request_url)

def get_clan_members(clan_id):
    members_url = clan_members_url.format(clan_id)
    return get_json(members_url).get('members')

def combined_member_tags(members):
    membertags = [m['tag'] for m in members]
    return ",".join(membertags)

def get_upcoming_chest_cycles(members):
    joined_membertags = combined_member_tags(members)
    chest_request_url = upcoming_chests_url.format(joined_membertags)
    return get_json(chest_request_url)

def war_log(clan_id):
    warlog_url = current_warlog_url.format(clan_id)
    return get_json(warlog_url)

def current_season(warlog):
    return max([w['seasonNumber'] for w in warlog])

if __name__== "__main__":
    pass