import b_discord as d
import clan_config
import royale_api

clan_id = clan_config.clan_id
chests_to_notify = ["epic","giant","legendary","magical","superMagical"]
chest_display_names = {"epic":"Epic","giant":"Giant","legendary":"Legendary","magical":"Magical","superMagical":"Super Magical"}
CHESTCOUNT_TO_NOTIFY = 5

def player_chest_notice():
    members = royale_api.get_clan_members(clan_id)
    member_chests = royale_api.get_upcoming_chest_cycles(members)
    member_notications = []
    for i, member in enumerate(members):
        name = member['name']
        tag = member['tag']
        chests = member_chests[i]
        if d.is_discord_user(name):
            for chest_type in chests_to_notify:
                chest_count = chests.get(chest_type)
                if chest_count < CHESTCOUNT_TO_NOTIFY:
                    discordtag = d.id_with_mention(name)
                    chestname = chest_display_names[chest_type]
                    notication_text = "{} - {} Chest is arriving in {} more chests!".format(discordtag, chestname, chest_count+1)
                    member_notications.append(notication_text)
    notice = "__**\U0001F4B0 Upcoming Chests \U0001F4B0**__\n"
    if len(member_notications) > 0:
        notice += "\n".join(member_notications)
    else:
        notice += "No upcoming chests for you guys at the moment.. \U0001F625 Hang tight!"
    d.post(notice)


if __name__== "__main__":
    player_chest_notice()