# MACRO-Explative-Exterminator
A Python-Based Discord Bot that will rewove, filter, and re-send their message without any swear words.

To use this bot, enter the Leaderboard folder, and ensure you have a ```V2.py```, ```leaderboard.json```, & ```.env``` file, they should all be in the same directory

Make sure you have discord.py installed, ensure you have entered your token into the .env file, and run the vL2.py

This Version has a leaderboard custom made for MACRO, where it is located in one channel and there is no command
To use it, use the ```$Leaderboard_here``` command (do before swearing in order to initialize)
Once enough users are logged in the ```leaderboard.json``` file you may want to remove the 5 placeholder accounts.
In thase same file, at line #466 there is a variable ```adminexempt```, make this true or false for if you want admins to be able to swear un-moderated.
at line #17 in ```V2.PY``` make sure to write in your file path to find your leaderboard file
 
To acess all commands in a server, do $commands in a valid channel
If you are the bot owner, add your discord ID in the ```V2.py``` file at line #26

to start or stop filtering in a channel, to ```$startfilter``` or ```stopfilter```, you can use the ```$status``` command to check if a channel is being filtered
