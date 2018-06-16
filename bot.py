import discord
import logging
import asyncio
import clan_config
import war
import clan_config
import royale_api

clan_id = clan_config.clan_id
clan_badge_image = clan_config.clan_badge_url
logging.basicConfig(level=logging.INFO)

client = discord.Client()


def embed_war_notice(current_pos, battles_remaining, forcasted_pos, winrate, timeleft_str, war_day_sib_str):
    embed = discord.Embed(title='Some war stats:', color=discord.Colour.magenta())
    embed.set_author(name='War Day', icon_url=clan_badge_image)
    embed.add_field(name='Time Remaining',value=str(timeleft_str))
    embed.add_field(name='Current Rank (est.)',value=str(current_pos))
    embed.add_field(name='Forecasted Rank (Beta)',value=str(forcasted_pos))
    embed.add_field(name='Win Rate',value=str(winrate + "%"))
    embed.add_field(name='Battles Remaining',value=str(battles_remaining))
    embed.add_field(name='Not fought yet',value=str(war_day_sib_str))
    return embed

def embed_collection_notice(timeleft_str, player_collections):
    embed = discord.Embed(title="Thanks for participating in the war! Don't forget to finish your battles \U0001F609", color=discord.Colour.dark_magenta())
    embed.set_author(name='Collection Day', icon_url=clan_badge_image)
    embed.add_field(name='Time Remaining',value=str(timeleft_str))
    battles_str = ""
    for p in player_collections:
        battles_str += "{}: {}\n".format(p['name'],p['battles'])
    embed.add_field(name='Battles',value=battles_str)
    return embed

def get_war_embed():
    current_war = royale_api.get_war_data(clan_id)
    if current_war.get('state') == "collectionDay":
        data = war.collection_day_data(current_war)
        timeleft_str = war.timeleft(current_war['collectionEndTime'])
        return embed_collection_notice(timeleft_str, data)
    elif current_war.get('state') == "warDay":
        current_pos, remaining, forcasted_pos = war.war_day_stats(current_war.get('standings'), clan_id)
        winrate = war.war_day_winrate(current_war)
        timeleft_str = war.timeleft(current_war['warEndTime'])
        war_day_sib_str = war.war_day_sib_members(current_war)
        return embed_war_notice(current_pos, remaining, forcasted_pos, winrate, timeleft_str, war_day_sib_str)
    else:
        return discord.Embed(title='No war going on atm..', color=discord.Colour.dark_gold())

def get_ranking_embed():
    warlog = royale_api.war_log(clan_id)
    return discord.Embed(title='Not implemented yet..', color=discord.Colour.dark_gold())

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!war'):
        e = discord.Embed(title='Checking war stats..', colour=discord.Colour.dark_gold())
        tmp = await client.send_message(message.channel, embed=e)
        embed = get_war_embed()
        await client.edit_message(tmp, embed=embed)
    elif message.content.startswith('!rank'):
        e = discord.Embed(title='Checking ranking stats..', colour=discord.Colour.dark_gold())
        tmp = await client.send_message(message.channel, embed=e)
        embed = get_ranking_embed()
        await client.edit_message(tmp, embed=embed)

client.run(clan_config.discord_bot_token)