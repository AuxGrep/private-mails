import subprocess
import time
#				!!< REQUIREMENTS >!!
# 1. You need telegram bot > use telegram botfather to build free telegramBot
# 2. Copy telegram bot token and save it in your computer, we ll use it at a future
# 3. use any technique to get your bot chat id and save it in your computer
# 4. add your BOT to the channel and wait for inbox email backups from this script.
#                           @Enjoy >> made by Hezron
#				< Twitter AuxGrep > 

def private():

	cmd = "zip -r inbox.zip Inbox"
	subprocess.call('xterm -T Telegram -e ' + cmd ,shell=True)
	bot_id = input("Enter Bot chat_Id: ")
	bot_token = input("Enter bot tokken: ")
	API = "" + bot_token + "/sendDocument?chat_id="
	subprocess.call('curl -F document=@inbox.zip ' + API + bot_id, shell=True)
