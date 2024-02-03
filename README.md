# MACRO-Explative-Exterminator
A Python-Based Discord Bot that will remove, filter, and re-send their message without any swear words.

To use this bot, enter the Leaderboard folder, and ensure you have a ```V2.py```, ```leaderboard.json```, & ```.env``` file, they should all be in the same directory

Make sure you have discord.py installed, ensure you have entered your token into the .env file, and run the vL2.py

This Version has a leaderboard custom-made for MACRO. To use it, use the ```$Leaderboard``` command.
Once enough users are logged in the ```leaderboard.json``` file you may want to remove the 5 placeholder accounts.
In this same file there is a variable ```adminexempt```, make this true or false if you want admins to be able to swear un-moderated.
 
To access all commands in a server, do ```$commands``` in a valid channel

to start or stop filtering in a channel, to ```$startfilter``` or ```stopfilter```, you can use the ```$status``` command to check if a channel is being filtered

This version uses discord webhooks and a bock backend to imitate the user that said something that needs to be filtered. This requires an authenticated discord bot to move the webhook between channels.
