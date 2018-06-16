# clash-discord
#### *Discord bot in Python for Clash Royale clan messages.*
This bot pulls data from RoyaleApi and publishes useful updates to a discord channel.
Documentation is under development and code has not been generalised.*

### Requirements:
```py
requests
discord.py from https://github.com/Rapptz/discord.py
```

### Features:
* Upcoming Chests notifications for discord channel users (scheduled)
* War notifications (scheduled and can be triggered via !war command)
  * The bot will detect whether it is in Collection or War day
  	* War Day - Show current battle stats and tag users to remind them
  	* Collection Day - Tags users to remind them to finish their battles
* Ranking information (scheduled)
  * Ranks the clan members according to configured scoring system. Data is obtained from /warlog endpoint which provides data from the last 10 wars.

### Configuration:
* Configure the following in ```clan_config.py```:
  * clan_id
  * royaleapi api key
  * discord bot token
  * discord webhook url
  * discord_users - mapping of discord ids to clash-royale tags/names for reminders
    * enable dev mode in discord, and right click on users to see their discord id

### Deployment:
* The repository includes the files for deploying on Heroku (requirements.txt and Procfile)
* chests.py and war.py has been set up to Heroku scheduler for daily reminders
* rank.py has been set up to run twice a month to provide ranking information