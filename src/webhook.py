import discord #import discord and webhook interactions
from discord import Webhook
import aiohttp #run webhook "service"
import requests #for webhook channel moving
import re
import os #for .json and .env file interactions
from dotenv import load_dotenv
import json #interact with json file save system
from datetime import datetime #support uptime

load_dotenv()

startTime = datetime.now()

adminId = #--------------------------------------------------------------Add Admin's Discord ID here
jsonpath = r'' #--------------------------------------------------------------Add the path to your json file

BOT_TOKEN = os.getenv("BOT_TOKEN") #take secure data from .env file
WEBHOOK_ID = os.getenv("WEBHOOK_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

intents = discord.Intents.default() #discord intents
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    swear_list = []
    censor_list = []
    swear_dict = {}

    new_swears = 0

    if message.author == client.user: #ensure bot it not listening to ittself or it's webhook/other bots
        return
    if message.author.bot:
        return
    
    if message.content.startswith('$dump'):
        if message.channel.type == discord.ChannelType.private:
            if message.author.id == adminId:
                await message.channel.send("uptime: {}".format(datetime.now() - startTime))
                await message.channel.send(file=discord.File(jsonpath))
                return
    
    if message.content.startswith("$commands"):
        await message.channel.send("Server Commands:\n$leaderboard\n$addword [word]\n$removeword [word]\n$startfilter\n$stopfilter\n$status\n$addcensor [word] [censor]",)
        if message.channel.type == discord.ChannelType.private:
            if message.author.id == adminId:
                await message.channel.send('DM commands (just for you)\n$dump\n$reboot')
    
    if message.content.startswith('$reboot'):
        if message.channel.type == discord.ChannelType.private:
            if message.author.id == adminId:
                os.system('sudo reboot')
                exit(0)

    if message.channel.type == discord.ChannelType.private: #if message sent in dm, stop process(except for $dump command that admins can use)
        await message.channel.send("this bot only works in servers")
        return

    txt = message.content.lower() #change name for search and censor

    f = open(jsonpath, "r")
    data = json.load(f)
    
    data["leaderboard"].sort(key=lambda x: x["swear_count"], reverse=True)

    id1 = data["leaderboard"][0]["id_number"]
    id2 = data["leaderboard"][1]["id_number"]
    id3 = data["leaderboard"][2]["id_number"]
    id4 = data["leaderboard"][3]["id_number"]
    id5 = data["leaderboard"][4]["id_number"]

    num1 = data["leaderboard"][0]["swear_count"]
    num2 = data["leaderboard"][1]["swear_count"]
    num3 = data["leaderboard"][2]["swear_count"]
    num4 = data["leaderboard"][3]["swear_count"]
    num5 = data["leaderboard"][4]["swear_count"]

    embedvar=discord.Embed(title="Swear Count", color=0x309C00)
    embedvar.add_field(name=num1, value="<@"+str(id1)+">")
    embedvar.add_field(name=num2, value="<@"+str(id2)+">")
    embedvar.add_field(name=num3, value="<@"+str(id3)+">")
    embedvar.add_field(name=num4, value="<@"+str(id4)+">")
    embedvar.add_field(name=num5, value="<@"+str(id5)+">")
    embedvar.set_footer(text="you all swear too often")

    #----------------------------------------------------------- auxiliary commands -------------

    if message.content.startswith("$leaderboard"):
        await message.delete()
        await message.channel.send(embed=embedvar, delete_after=60)
        return

    if message.content.startswith("$addcensor"):
        if message.author.guild_permissions.administrator:
            await message.delete()
            m = re.split("\s", message.content.lower())
            if len(m) == 3:
                with open(jsonpath,'r+') as file:
                    data = json.load(file)
                    for r in data["Data"][0]["blacklist"]:
                        if m[1] in r["word"]:
                            data["Data"][0]["blacklist"][data["Data"][0]["blacklist"].index(r)]["cen"] = m[2]
                            file.seek(0)
                            json.dump(data, file, indent = 4)
                            file.truncate()
                            file.close()
                            return
            else:
                await message.channel.send("remember, the proper format for this command is:\n```$addcensor [word in blacklist] [new word replacement]```", delete_after=15)
                return


    if message.content.startswith("$addword"):
        if message.author.guild_permissions.administrator:
            await message.delete()
            m = re.split("\s", message.content.lower())
            with open(jsonpath,'r+') as file:
                data = json.load(file)
                for r in data["Data"][0]["blacklist"]:
                    if m[1] in r["word"]:
                        await message.channel.send("that word already exists in your filter database", delete_after=5.0)
                        file.close()
                        return
                else:
                    data['Data'][0]['blacklist'].append({"word": m[1], "cen": ("-" * len(m[1]))})
                    file.seek(0)
                    json.dump(data, file, indent = 4)
                    file.truncate()
                    file.close()
                    await message.channel.send('adding word', delete_after=5.0)
                    await message.channel.send(m[1], delete_after=5.0)
                    return
                
    if message.content.startswith("$removeword"):
        if message.author.guild_permissions.administrator:
            await message.delete()
            m = re.split("\s", message.content.lower())
            with open(jsonpath,'r+') as file:
                data = json.load(file)
                for r in data["Data"][0]["blacklist"]:
                    if m[1] in r["word"]:
                        del data["Data"][0]["blacklist"][data["Data"][0]["blacklist"].index(r)]
                        await message.channel.send("deleting word", delete_after=5.0)
                        await message.channel.send(m[1], delete_after=5.0)
                        file.seek(0)
                        json.dump(data, file, indent = 4)
                        file.truncate()
                        file.close()
                        return
                else:
                    await message.channel.send("that word is not in your filter database", delete_after=5.0)
                    file.close()
                    return
    
    if message.content.startswith("$stopfilter"):
        if message.author.guild_permissions.administrator:
            await message.delete()
            with open(jsonpath,'r+') as file:
                data = json.load(file)
                filterlist = data['rundata'][0]['nonfilter']
                if message.channel.id in filterlist:
                    await message.channel.send('this channel is already not being filtered', delete_after=5.0)
                    file.close()
                    return
                else:
                    filterlist.append(message.channel.id)
                    await message.channel.send('stopping filtering', delete_after=5.0)
                    file.seek(0)
                    json.dump(data, file, indent = 4)
                    file.truncate()
                    file.close()
                    return

    if message.content.startswith("$startfilter"):
        if message.author.guild_permissions.administrator:
            await message.delete()
            with open(jsonpath,'r+') as file:
                data = json.load(file)
                filterlist = data['rundata'][0]['nonfilter']
                if message.channel.id not in filterlist:
                    await message.channel.send('this channel is already being filtered', delete_after=5.0)
                    return
                del filterlist[filterlist.index(message.channel.id)]
                await message.channel.send("starting filtering", delete_after=5.0)
                file.seek(0)
                json.dump(data, file, indent = 4)
                file.truncate()
                file.close()
                return
    
    if message.content.startswith("$status"):
        if message.author.guild_permissions.administrator:
            await message.delete()
            with open(jsonpath,'r') as file:
                data = json.load(file)
                if message.channel.id in data['rundata'][0]['nonfilter']:
                    await message.channel.send('this channel is not being filtered', delete_after=5.0)
                else:
                    await message.channel.send('this channel is being filtered', delete_after=5.0)
                file.close()
                return
            
    #----------------------------------------------------------- end auxiliary commands ---------
    
    if message.channel.id in data['rundata'][0]['nonfilter']:
        return

    if data['rundata'][0]["ADMINEXEMPT"]: #check if admins are allowed to swear in the server
        if message.author.guild_permissions.administrator: #if yes, and user is an admin, stop process
            return

    for r in data["Data"][0]["blacklist"]: #take dictionary form from json and split into two differend lists.
        swear_list.append(r["word"])
        censor_list.append(r["cen"])

    def combine_lists_to_dictionary(keys, values):
        combined_dict = {}
        for i in range(len(keys)):
            if i < len(values):
                combined_dict[keys[i]] = values[i]
            else:
                combined_dict[keys[i]] = None
        return combined_dict

    def contains_swear(text, blacklist):
        # Exclude certain words from being matched
        exclusion_words = ['if i leave this empty it breaks']  # Add any words you want to exclude from matching
        
        # Create a pattern to match the blacklist words, excluding exclusion words
        pattern = r"\b(?!" + "|".join(map(re.escape, exclusion_words)) + r")(" + "|".join(map(re.escape, blacklist)) + r")\b"

        # Search for matches using the pattern
        match = re.search(pattern, text, flags=re.IGNORECASE)

        if match:
            return True
        else:
            return False

    #for find in range(len(swear_list)): #find swear words by looping through swear list
    #    found = re.search(swear_list[find], txt)
    #    if found: # if found, leave "found" variable to be detected by next section
    #        break

    if contains_swear(txt, swear_list):
        swear_dict = combine_lists_to_dictionary(swear_list, censor_list)

        def replace_words(text, blacklist, replacements, new_swears):
            new_swears = 0
            for word in blacklist:
                pattern = r"\b" + re.escape(word.lower()) + r"\b"
                if re.search(pattern, text.lower()):
                    text = re.sub(pattern, replacements.get(word.lower(), ""), text, flags=re.IGNORECASE)
                    new_swears = new_swears + len(re.findall(pattern, txt))
            return [text, new_swears]
        txt += " " #allow program to not run out of space

        #for swear in range(len(swear_list)): #loop through swear list
        #    for match in re.finditer(swear_list[swear], txt): #find location of word
        #        #print(match.start(), match.end())
        #        txt = txt[:match.start()] + censor_list[swear] + txt[match.start()+(match.end()-match.start()):] #replace word and splice sentance back together

        #print(cenTxt)
        webJson = { "channel_id": message.channel.id } #json for new webhook location
        headers = { "Authorization": "Bot " + BOT_TOKEN } #auth for webhook secure interactions

        r = requests.patch('https://discordapp.com/api/webhooks/' + WEBHOOK_ID, json=webJson, headers=headers) #move channel using api interactions
        if message.author.avatar == None: #set avatar of webhook, if default it is the user's color default, if modified it is the user's normal avatar
            av = message.author.default_avatar
        else:
            av = message.author.avatar
        
        async def anythingContent(url, x): #function to send webhook with new message
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(url, session=session)
                await webhook.send(content=x, username=message.author.display_name, avatar_url=av)
        
        async def anything(url): #function to send webhook with new message
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(url, session=session)
                await webhook.send(content=replace_words(txt, swear_list, swear_dict, new_swears)[0], username=message.author.display_name, avatar_url=av)

        await message.delete() #delete old swear message
        
        if message.attachments:
            await anything(WEBHOOK_URL) #send new message
            for i in message.attachments:
                await anythingContent(WEBHOOK_URL, i)
                #await message.channel.send(i)
        else:
            await anything(WEBHOOK_URL) #send new message

        
#------------------------------------------------------------------------- area that deals with adding swears to the leaderboard secion of the json file -------------

        with open(jsonpath,'r+') as file:   # open json save file
            data = json.load(file)
            for i in data["leaderboard"]: # check if the user's id is already saved
                if i["id_number"] == message.author.id:
                    #print("user has an entry")
                    def add_swears(lst, unique_id):
                        for item in lst:
                            if item["id_number"] == unique_id:
                                item["swear_count"] += replace_words(txt, swear_list, swear_dict, new_swears)[1] #add the amount of new swears to their running total
                                break
                    add_swears(data["leaderboard"], message.author.id)
                    file.seek(0)
                    # convert back to json.
                    json.dump(data, file, indent = 4)
                    file.truncate()
                    file.close()
                    break
            else: # if the user does not have a save instance, make a new one
                print('no entry for this user, adding now')
                new_data = {"id_number": int(message.author.id),"swear_count": int(replace_words(txt, swear_list, swear_dict, new_swears)[1])}
                data["leaderboard"].append(new_data)
                file.seek(0)
                json.dump(data, file, indent = 4)
                file.close()


#-------------------------------------------------------------------------

        return
    else:
        return #if no swears, end loop

client.run(BOT_TOKEN)
