#not used in the amin system of the bot, just for adding  users or swears, mostly just a development proof-of-concept

import json

id = input("what is the id?\n")

#data for what sub-section the swear data is in
location = 0

with open("leaderboard.json",'r+') as file:
    data = json.load(file)
        #search for pre-existing Id
    for i in data["leaderboard"]:
        location += 1
        if i['id_number'] == id:
            print(i)
            #ask for amount of new swears
            print("ID found, editing leaderboard level")
            swears = input("how many more swears?\n")

            #print existing swears
            print(int(i["swear_count"]))

            #add pre-existing and new amount of swears, and print
            total_swears = (int(i["swear_count"]))+(int(swears))
            print(total_swears)

            #set the swear amount on the leaderboard to the amount calculated
            data['leaderboard'][location-1]['swear_count'] = str(total_swears)
            
            #go to correct spot, resend data to json file, and cut off excess data
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            break

    else:
        #ask for amount of new swears
        print("ID not found, creating new instance on leaderboard")
        swears = input("how many swears?\n")

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
