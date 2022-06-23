import discord
import re
import os
from os.path import join, dirname
from dotenv import load_dotenv
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='$')

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

#TOKEN(login), ADMINEXEMPT(can admins swear), ADMINLEADERBOARD(who can acess leaderboard)
TOKEN = os.environ.get("TOKEN")
adminExempt = os.environ.get("ADMINEXEMPT")
adminLeaderboard = os.environ.get("ADMINLEADERBOARD")

#list of swear words
blackList = ["4r5e", "5h1t", "5hit", "a55", "anal", "anus", "ar5e", "arrse", "arse", "ass", "asshat", "ass-fucker", "asses", "assfucker", "assfukka", "asshole", "assholes", "asswhole", "a_s_s", "b!tch", "b00bs", "b17ch", "b1tch", "ballbag", "balls", "ballsack", "bastard", "beastial", "beastiality", "bellend", "bestial", "bestiality", "bi+ch", "biatch", "bitch", "bitcher", "bitchers", "bitches", "bitchin", "bitching", "bloody", "blow job", "blowjob", "blowjobs", "bollock", "bollok", "boner", "boob", "boobs", "booobs", "boooobs", "booooobs", "booooooobs", "bunny fucker", "butt", "butthole", "buttmuch", "buttplug", "c0ck", "c0cksucker", "clitoris", "clits", "cock", "cock-sucker", "cockface", "cockhead", "cockmunch", "cockmuncher", "cocks", "cocksuck", "cocksucked", "cocksucker", "cocksucking", "cocksucks", "cocksuka", "cocksukka", "cokmuncher", "coksucka", "cum", "cummer", "cumming", "cums", "cumshot", "cunilingus", "cunillingus", "cunnilingus", "cunt", "cuntlick", "cuntlicker", "cuntlicking", "cunts", "cyalis", "cyberfuc", "cyberfuck", "cyberfucked", "cyberfucker", "cyberfuckers", "cyberfucking", "d1ck", "dick", "dickhead", "dildo", "dildos", "dink", "dinks", "dirsa", "dlck", "dog-fucker", "doggin", "dogging", "donkeyribber", "doosh", "duche", "dyke", "ejaculate", "ejaculated", "ejaculates", "ejaculating", "ejaculatings", "ejaculation", "ejakulate", "f u c k", "f u c k e r", "f4nny", "fag", "fagging", "faggitt", "faggot", "faggs", "fagot", "fagots", "fags", "fanny", "fannyflaps", "fannyfucker", "fanyy", "fatass", "fcuk", "fcuker", "fcuking", "feck", "fecker", "felching", "fellate", "fellatio", "fingerfuck", "fingerfucked", "fingerfucker", "fingerfuckers", "fingerfucking", "fingerfucks", "fistfuck", "fistfucked", "fistfucker", "fistfuckers", "fistfucking", "fistfuckings", "fistfucks", "flange", "fook", "fooker", "fuck", "fucka", "fucked", "fucker", "fuckers", "fuckhead", "fuckheads", "fuckin", "fucking", "fuckings", "fuckingshitmotherfucker", "fuckme", "fucks", "fuckwhit", "fuckwit", "fudge packer", "fudgepacker", "fuk", "fuker", "fukker", "fukkin", "fuks", "fukwhit", "fukwit", "fux", "fux0r", "f_u_c_k", "gangbang", "gangbanged", "gangbangs", "gaylord", "gaysex", "goatse", "hardcoresex", "heshe", "hoar", "hoare", "hoer", "homo", "hore", "horniest", "horny", "hotsex", "jack-off", "jackoff", "jap", "jerk-off", "jism", "jiz", "jizm", "jizz", "kawk", "knob", "knobead", "knobed", "knobend", "knobhead", "knobjocky", "knobjokey", "kock", "kondum", "kondums", "kum", "kummer", "kumming", "kums", "kunilingus", "l3i+ch", "l3itch", "labia", "lust", "lusting", "m0f0", "m0fo", "m45terbate", "ma5terb8", "ma5terbate", "masochist", "master-bate", "masterb8", "masterbat*", "masterbat3", "masterbate", "masterbation", "masterbations", "masturbate", "mo-fo", "mof0", "mofo", "mothafuck", "mothafucka", "mothafuckas", "mothafuckaz", "mothafucked", "mothafucker", "mothafuckers", "mothafuckin", "mothafucking", "mothafuckings", "mothafucks", "mother fucker", "motherfuck", "motherfucked", "motherfucker", "motherfuckers", "motherfuckin", "motherfucking", "motherfuckings", "motherfuckka", "motherfucks", "muff", "mutha", "muthafecker", "muthafuckker", "muther", "mutherfucker", "n1gga", "n1gger", "nazi", "nigg3r", "nigg4h", "nigga", "niggah", "niggas", "niggaz", "nigger", "niggers", "nob", "nob jokey", "nobhead", "nobjocky", "nobjokey", "numbnuts", "nutsack", "orgasim", "orgasims", "orgasm", "orgasms", "p0rn", "pawn", "pecker", "penis", "penisfucker", "phonesex", "phuck", "phuk", "phuked", "phuking", "phukked", "phukking", "phuks", "phuq", "pigfucker", "pimpis", "piss", "pissed", "pisser", "pissers", "pisses", "pissflaps", "pissin", "pissing", "pissoff", "poop", "porn", "porno", "pornography", "pornos", "prick", "pricks", "pron", "pube", "pusse", "pussi", "pussies", "pussy", "pussys", "rectum", "retard", "rimjaw", "rimming", "sex", "sh!+", "sh!t", "sh1t", "shag", "shagger", "shaggin", "shagging", "shemale", "shi+", "shit", "shitdick", "shite", "shited", "shitey", "shitfuck", "shitfull", "shithead", "shiting", "shitings", "shits", "shitted", "shitter", "shitters", "shitting", "shittings", "shitty", "skank", "slut", "sluts", "smegma", "smut", "snatch", "son-of-a-bitch", "spac", "spunk", "s_h_i_t", "t1tt1e5", "t1tties", "teets", "teez", "testical", "testicle", "tit", "titfuck", "tits", "titt", "tittie5", "tittiefucker", "titties", "tittyfuck", "tittywank", "titwank", "tosser", "turd", "tw4t", "twat", "twathead", "twatty", "twunt", "twunter", "v14gra", "v1gra", "vagina", "viagra", "vulva", "w00se", "wang", "wank", "wanker", "wanky", "whoar", "whore", "xrated", "Arschgeige", "Trantüte", "Spargeltarzan", "Lustmolch", "Flachwichser", "Pissnelke", "Fickfehler", "Tratschtante", "Stinkstiefel", "Hosenscheisser", "Schlappschwanz", "Hackfresse", "Allmannshure", "Andächtler", "Arschgucker", "Arschkröte", "Arschloch", "Bartputzer", "Dickscheißer", "Donnermaul", "Scheiss", "Scheisse", "Fick", "F1ck", "fick", "f-i-c-k", "Fickdich", "Fickdick", "Huren", "Hurensohn", "Sclampe", "Schlampen", "Schlampenficker", "Misgeburt", "Missgeburt", "Wichser", "Wicser", "Wixer", ]

#empty list for swear words
swear_location = []

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for swear words"))

@client.event
async def on_message(message):
    if message.content.lower() == '$leaderboard':
        if adminLeaderboard == "TRUE" and not message.author.guild_permissions.administrator:
            return
        else:
            with open("leaderboard.json",'r') as file:
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

                await message.channel.send(embed=embedvar)
                file.close()
        
    #end if user is the bot
    if message.author == client.user:
        return

    #end if user is admin
    if adminExempt == "TRUE":
        if message.author.guild_permissions.administrator:
            return

    #split message into parts of a list, removing spaces 
    x = re.split("\s", message.content.lower())

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

        embed2=discord.Embed(title="Filtered Message", description="Author: <@"+str(message.author.id)+">", color=0x00FFAE)
        embed2.add_field(name="Message:", value=(" ".join(x)))
        embed2.set_thumbnail(url=message.author.avatar_url)
        embed2.set_footer(text="you all swear too much")

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

        with open("leaderboard.json",'r+') as file:
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
    else:
        return

client.run(TOKEN)
