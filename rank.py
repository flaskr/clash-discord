import b_discord as d
import clan_config
import royale_api
import datetime

clan_id = clan_config.clan_id

def player_warlog_stats(warlog):
    players = {}
    for war in warlog:
        for p in war['participants']:
            tag = p['tag']
            if tag in players:
                player = players[tag]
                player['cardsEarned'].append(p['cardsEarned'])
                player['wins'] += p['wins']
                if p['battlesPlayed'] == 0:
                    player['battlesPlayed'] += 1
                else:
                    player['battlesPlayed'] += p['battlesPlayed']
                players[tag] = player
            else:
                player = {}
                player['cardsEarned'] = [p['cardsEarned']]
                player['wins'] = p['wins']
                player['battlesPlayed'] = p['battlesPlayed']
                players[tag] = player
    for tag, stats in players.items():
        stats['cardsEarned'] = int(sum(stats['cardsEarned']) / float(len(stats['cardsEarned'])))
        stats['winRate'] = int(stats['wins']/stats['battlesPlayed']*100)
    return players

def ranking_data(warlog):
    members = royale_api.get_clan_members(clan_id)
    warstats = player_warlog_stats(warlog)
    ranking_data = []
    for m in members:
        tag = m['tag']
        if tag in warstats:
            s = warstats[tag]
            score = s['wins'] * 1000 + s['winRate'] * 50 + s['cardsEarned']
            ranking_data.append({'tag':m['tag'], 'name':m['name'], 'wins':s['wins'], 'winRate':s['winRate'], 'cardsEarned':s['cardsEarned'], 'score':score})
        else:
            ranking_data.append({'tag':m['tag'], 'name':m['name'], 'wins': 0, 'winRate': 0, 'cardsEarned': 0, 'score':0 })    
    sorted_players = sorted(ranking_data, key=lambda k: k['score'], reverse=True) 
    return sorted_players

def formatted_ranking(data):
    name_lengths = [len(x['name']) for x in data]
    max_name_length = str(max(name_lengths))
    header_format = "|  # | {:"+max_name_length+"s} | Wins | Win Rate | Avg. Cards |\n"
    output  = header_format.format("Name")
    row_format = "| {:2d} | {:"+max_name_length+"s} |  {:2d}  |   {:3d}%   |     {:3d}    |\n"
    for i, p in enumerate(data):
        player_row = row_format.format(i+1, p['name'], p['wins'], p['winRate'], p['cardsEarned'])
        output += (player_row)
    return output.strip()

def isfirstsunday(date):
    return date.weekday() == 6 and date.day <= 7

def isthirdsunday(date):
    return date.weekday() == 6 and 15 <= date.day and date.day < 22

if __name__== "__main__":
    today = datetime.datetime.today()
    if isfirstsunday(today) or isthirdsunday(today):
        warlog = royale_api.war_log(clan_id)    
        data = ranking_data(warlog)
        ranking_table = formatted_ranking(data)
        midindex = ranking_table.index("\n", 1500) #max 2000 characters are allowed
        first_half = ranking_table[:midindex];
        second_half = ranking_table[midindex+1:];
        d.post("__**Bi-weekly Ranking**__")
        d.post("```"+first_half+"```")
        d.post("```"+second_half+"```")