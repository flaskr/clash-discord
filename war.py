import b_discord as d
import clan_config
import royale_api
import time

clan_id = clan_config.clan_id
COLLECTION_BATTLES = 3

def collection_day_data(war):
    current_participants = war.get('participants')
    participants_with_battles_remaining = [p for p in current_participants if p['battlesPlayed'] < COLLECTION_BATTLES]
    notice = "__**Collection Day Notice**__\nThanks for participating in the war! Don't forget to finish your battles \U0001F609\n" 
    player_collections = []
    for p in participants_with_battles_remaining:
        name = d.id_with_mention(p.get('name'))
        battles = "{}/{}".format(p.get('battlesPlayed'), COLLECTION_BATTLES)
        player_collections.append({"name": name, "battles": battles})
    return player_collections

def max_number_of_battles(standings):
    participant_counts = [c['participants'] for c in standings]
    battles = max(participant_counts)
    return battles

def war_day_stats(standings, clan_tag):
    current_pos = 0
    current_battle = 0
    clan_forecast = 0
    forcasted_pos = 0
    num_battles = max_number_of_battles(standings)
    for index, clan in enumerate(standings):
        each_clan_remaining = num_battles - clan['battlesPlayed']
        clan['forecast'] = (each_clan_remaining)/2 + clan['wins']
        if clan['tag'] == clan_tag:
            current_pos = index +1
            remaining = each_clan_remaining
            clan_forecast = clan['forecast']
    forecasts = [c['forecast'] for c in standings]
    forecasts.sort(reverse=True)
    forcasted_pos = forecasts.index(clan_forecast) + 1
    return (current_pos, remaining, forcasted_pos)

def war_day_winrate(war):
    participants = war['participants']
    total_battles_played = 0
    total_battles_won = 0
    for participant in participants:
        total_battles_played += participant['battlesPlayed']
        total_battles_won += participant['wins']
    if total_battles_played == 0:
        return "0"
    return str(int(total_battles_won / total_battles_played * 100))

def timeleft(endtime):
    milliseconds_left = endtime - time.time()
    m, s = divmod(milliseconds_left, 60)
    h, m = divmod(m, 60)
    return "%dh %02dm" % (h, m)

def war_day_sib_members(war):
    participants_with_zero_battles = [p for p in war['participants'] if p['battlesPlayed'] == 0]
    if len(participants_with_zero_battles) == 0:
        return "Nobody :)"
    participant_names = [d.id_with_mention(p.get('name')) for p in participants_with_zero_battles]
    return "\n".join(participant_names)

if __name__== "__main__":
    d.post('!war')

