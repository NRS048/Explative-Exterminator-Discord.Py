import discord
import re
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
from datetime import datetime

startTime = datetime.now()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#TOKEN(login), ADMINEXEMPT(can admins swear), CHANNELID(where is the leaderboard), MSGID(what message is the leaderbaord)
TOKEN = os.environ.get("TOKEN")

jsonPath = " "

#empty list for swear words
swear_location = []

intents = discord.Intents.all()

client = discord.Client(intents=intents)

adminId = 0 #Bot Admin Id

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for swear words"))

@client.event
async def on_message(message):
    #end if user is the bot
    if message.author == client.user:
        return

    with open(jsonPath,'r') as file:
        dataread = json.load(file)
    
        dataread["leaderboard"].sort(key=lambda x: x["swear_count"], reverse=True)
    
        id1 = dataread["leaderboard"][0]["id_number"]
        id2 = dataread["leaderboard"][1]["id_number"]
        id3 = dataread["leaderboard"][2]["id_number"]
        id4 = dataread["leaderboard"][3]["id_number"]
        id5 = dataread["leaderboard"][4]["id_number"]
    
        num1 = dataread["leaderboard"][0]["swear_count"]
        num2 = dataread["leaderboard"][1]["swear_count"]
        num3 = dataread["leaderboard"][2]["swear_count"]
        num4 = dataread["leaderboard"][3]["swear_count"]
        num5 = dataread["leaderboard"][4]["swear_count"]
    
        embedvar=discord.Embed(title="Top 5 users who swear the most in this server:", color=0xFF7600)
        embedvar.add_field(name=num1, value="<@"+str(id1)+">")
        embedvar.add_field(name=num2, value="<@"+str(id2)+">")
        embedvar.add_field(name=num3, value="<@"+str(id3)+">")
        embedvar.add_field(name=num4, value="<@"+str(id4)+">")
        embedvar.add_field(name=num5, value="<@"+str(id5)+">")
        embedvar.set_footer(text="you all swear too often")
        
        #list of swear words
        blackList = dataread['Data'][0]['blackList']
        adminExempt = dataread['RunData'][0]['ADMINEXEMPT']

        file.close()

    if message.content.startswith('$dump'):
        if message.channel.type == discord.ChannelType.private:
            if message.author.id == adminId:
                await message.channel.send("uptime:")
                await message.channel.send(datetime.now() - startTime)
                await message.channel.send(file=discord.File(jsonPath))
                return

    if message.content.startswith('$reboot'):
        if message.channel.type == discord.ChannelType.private:
            if message.author.id == adminId:
                os.system('sudo reboot')

    if message.content.startswith("$commands"):
        await message.channel.send("Server Commands:\n$leaderboard_here\n$addword\n$removeword\n$startfilter\n$stopfilter\n$status",)
        if message.channel.type == discord.ChannelType.private:
            if message.author.id == adminId:
                await message.channel.send('DM commands (just for you)\n$dump\n$reboot')

    if message.channel.type == discord.ChannelType.private:
        await message.channel.send("this bot only works in servers")
        return

    if message.content == "$leaderboard_here":
        if message.author.guild_permissions.administrator:
            await message.delete()
            with open(jsonPath,'r+') as file:
                data = json.load(file)
                data['RunData'][0]['CHANNELID'] = message.channel.id

                messageReply = await message.channel.send(embed=embedvar)
                data['RunData'][0]['MSGID'] = messageReply.id

                file.seek(0)
                json.dump(data, file, indent = 4)
                file.truncate()
                file.close()

    if message.content.startswith("$addword"):
        if message.author.guild_permissions.administrator:
            await message.delete()
            m = re.split("\s", message.content.lower())
            with open(jsonPath,'r+') as file:
                data = json.load(file)
                Bl = data['Data'][0]['blackList']
                if m[1] in Bl:
                    await message.channel.send("that word already exists in your filter database", delete_after=5.0)
                    file.close()
                    return
                else:
                    pass
                Bl.append(m[1])
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
            n = re.split("\s", message.content.lower())
            with open(jsonPath,'r+') as file:
                data = json.load(file)
                Bl = data['Data'][0]['blackList']
                if n[1] in Bl:
                    pass
                else:
                    await message.channel.send("that word is not in your filter database", delete_after=5.0)
                    file.close()
                    return
                del Bl[Bl.index(n[1])]
                await message.channel.send("deleting word", delete_after=5.0)
                await message.channel.send(n[1], delete_after=5.0)
                file.seek(0)
                json.dump(data, file, indent = 4)
                file.truncate()
                file.close()
                return
            
    if message.content.startswith("$stopfilter"):
        if message.author.guild_permissions.administrator:
            await message.delete()
            with open(jsonPath,'r+') as file:
                data = json.load(file)
                filterlist = data['RunData'][0]['nonfilterchannels']
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
            with open(jsonPath,'r+') as file:
                data = json.load(file)
                filterlist = data['RunData'][0]['nonfilterchannels']
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
            with open(jsonPath,'r') as file:
                data = json.load(file)
                if message.channel.id in data['RunData'][0]['nonfilterchannels']:
                    await message.channel.send('this channel is not being filtered', delete_after=5.0)
                else:
                    await message.channel.send('this channel is being filtered', delete_after=5.0)
                file.close()
                return

    if message.content.startswith("$commands"):
        if message.author.guild_permissions.administrator:
            await message.channel.send("Commands:\n$leaderboard_here\n$addword\n$removeword\n$startfilter\n$stopfilter\n$status", delete_after=10.0)
            if message.channel.type == discord.ChannelType.private:
                if message.author.id == adminId:
                    await message.channel.send('DM commands (just for you, bot admin)\n$dump\n$reboot')

    if message.channel.id in dataread['RunData'][0]['nonfilterchannels']:
            return

    #end if user is admin
    if adminExempt == "TRUE":
        if message.author.guild_permissions.administrator:
            return

    #split message into parts of a list, removing spaces 
    x = re.split("\s|!|\.|,|\?|\*", message.content.lower())

    #declare var for swears found in message - leaderboard
    swears = 0

    #check if swear is in the list
    check = any(item in x for item in blackList)
    if check is True:
        
        #if swear word found at a location, load into location list
        for index, elem in enumerate(x):
            if elem in blackList:
                
                swear_location.insert(1, index)

            #replace all parts of list with "----"    
            for i in range(len(x)):
                if x[i] in blackList:
                    x[i] = '----'
                    swears += 1
        
        #delete message
        await message.delete()

        #create embed with users profile pic, name, and the filtered message
        embed2=discord.Embed(title="Filtered Message", description="Author: <@"+str(message.author.id)+">", color=0x00FFAE)
        embed2.add_field(name="Message:", value=(" ".join(x)))
        embed2.set_thumbnail(url=message.author.avatar)
        embed2.set_footer(text="you all swear too much")

        #system to re-send any attachments that were on the message
        if message.attachments:
            await message.channel.send(embed=embed2)
            for i in message.attachments:
                await message.channel.send(i)
        else:
            await message.channel.send(embed=embed2)
            

        #leaderboard system
        id = message.author.id

        #data for what sub-section the swear data is in
        json_location = 0

        #open json leaderboard
        with open(jsonPath,'r+') as file:
            data = json.load(file)
            #search for pre-existing Id
            for i in data["leaderboard"]:
                json_location += 1
                if i['id_number'] == id:
                    #ask for amount of new swears
                    #print("ID found, editing leaderboard level")

                    #print existing swears
                    #print(int(i["swear_count"]))

                    #add pre-existing and new amount of swears, and print
                    total_swears = (int(i["swear_count"]))+(int(swears))
                    #print(total_swears)

                    #set the swear amount on the leaderboard to the amount calculated
                    data['leaderboard'][json_location-1]['swear_count'] = total_swears
            
                    #go to correct spot, resend data to json file, and cut off excess data
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
                    file.close()
                    break

            else:
                #create new "account" on leaderboard
                print("ID not found, creating new instance on leaderboard")

                def write_json(new_data):
                    # Join new_data with data inside emp_details
                    data["leaderboard"].append(new_data)
                    # Sets file's current position at offset.
                    file.seek(0)
                    # convert back to json.
                    json.dump(data, file, indent = 4)

                # python object to be appended
                y = {"id_number": id, "swear_count": swears}
                write_json(y)
                file.close()

        #system for leaderboard updating after every swear
        with open(jsonPath,'r+') as file:
            data = json.load(file)
            
            channelLB = client.get_channel(dataread['RunData'][0]['CHANNELID'])
            msgidLB = int(dataread['RunData'][0]['MSGID'])
            #edit leaderboard message
            msg = await channelLB.fetch_message(msgidLB)
            await msg.edit(content=None, embed=embedvar)
            file.close()

    else:
        #return if no swears
        return

#login
client.run(TOKEN)
