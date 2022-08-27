import pyperclip
import requests
import re
import os
import random
import string
import time
import subprocess
import sys
import pkg_resources

purple = '\x1b[38;5;165m'
blue = '\x1b[38;5;33m'
red = '\x1b[38;5;196m'
green = '\x1b[38;5;118m'
grey = '\x1b[38;5;0m'
pink = '\x1b[38;5;199m' #

required = {'pyperclip==1.8.0', 'requests==2.21.0'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

API = 'https://www.1secmail.com/api/v1/'
domainList = ['1secmail.com', '1secmail.net', '1secmail.org']
domain = random.choice(domainList)

def banner():
    print(f'''{grey}
	                               ,▄▄▄▄▄╓,
                   ,,▄▄▄▄▓█████████████████████▓▓▄▄▄▄,,
                 ▀▀████████████████████████████████████████▓▄▄▄▄▄▄▄,
                ▄▄██████████████████████████████████████████████▌▄╓▄∩
             ▄██▀▀████████████████████████████████████████████████▄,     '
            `   ▄█████████{green}▓{grey}████{green}▓▓▓▓▓▓▓▓▓{grey}███████{green}▓{grey}██████▄▄L,
              ▄██████████{green}▓{grey}███{green}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{grey}████{green}▓{grey}███████▀
             └▀╙ ▓██████{green}▓{grey}██{green}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{grey}███{green}▓▓▓{grey}████▀╙`
                ,███████{green}▓{grey}██{green}▓▓▓▓▓▓{grey}████{green}▓▓▓▓▓▓▓▓▓{grey}██{green}▓{grey}███
                ▓██████████{green}▓▓▓▓▓▓{grey}█████{green}▓▓▓▓▓▓▓▓{grey}██{green}▓{grey}█████m
                ████████{green}▓{grey}████{green}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{grey}████████████████████,
               J█████████{green}▓{grey}████{green}▓▓▓▓▓▓▓▓▓▓▓▓▓▓{grey}███{green}▓{grey}██████▀╙
               ╟█████████████{green}▓▓▓▓▓▓▓▓▓▓▓▓▓{grey}████{green}▓{grey}████████████████▀
             {green} ▄▓▓{grey}████████████{green}▓▓▓{grey}█████████████████████████████████▀{green}╨
             Φ▌▓▓▓{grey}███████████████████████████████████████{green}▓▓▓▓▌Å"`
              ⌐'╫▓▓▓▓▓▓▓▓▓▓▓▓▓{grey}███████████████████████{green}▓▓▓▓▓▓▓Ñ`
              `  "▌░╟╫╨╢║╣▀▓▓▓▀▀▀▓▓▓▓▓▓▓▓▓▓▓▓▓▓▌▀▀▀▀╣ÖÅ`╠░║▓:
             `    ▌ "╫. j  ▓▓▒" ``╟╫M` ```└```     ╙⌂║. "Ñ▓▌ PRIVATE MAILS - AuxGrep
                 ▐M `╨H ¿ "▓▓╫    ╣Ñ      j         ╣╬   ║▓      2022
                 ╬   :Ñ"  ╫▓╣Ü    ╣░      j         ╙▌   ╣▌
                 ''')

def generateUserName():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    return username

def extract():
    getUserName = re.search(r'login=(.*)&',newMail).group(1)
    getDomain = re.search(r'domain=(.*)', newMail).group(1)
    return [getUserName, getDomain]


def print_statusline(msg: str):
    last_msg_length = len(print_statusline.last_msg) if hasattr(print_statusline, 'last_msg') else 0
    print(' ' * last_msg_length, end='\r')
    print(msg, end='\r')
    sys.stdout.flush()
    print_statusline.last_msg = msg

def deleteMail():
    url = 'https://www.1secmail.com/mailbox'
    data = {
        'action': 'deleteMailbox',
        'login': f'{extract()[0]}',
        'domain': f'{extract()[1]}'
    }

    print_statusline("Generating your email address - " + mail + '\n')
    req = requests.post(url, data=data)

def checkMails():
    reqLink = f'{API}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
    req = requests.get(reqLink).json()
    length = len(req)
    if length == 0:
        print_statusline("Inbox is Empty!! let's wait for emails.")
    else:
        idList = []
        for i in req:
            for k,v in i.items():
                if k == 'id':
                    mailId = v
                    idList.append(mailId)

        x = 'mails' if length > 1 else 'mail'
        print_statusline(f"You received {length} {x}. (Enjoy!!!!.)")

        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'All Mails')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        for i in idList:
            msgRead = f'{API}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={i}'
            req = requests.get(msgRead).json()
            for k,v in req.items():
                if k == 'from':
                    sender = v
                if k == 'subject':
                    subject = v
                if k == 'date':
                    date = v
                if k == 'textBody':
                    content = v

            mail_file_path = os.path.join(final_directory, f'{i}.txt')

            with open(mail_file_path,'w') as file:
                file.write("Sender: " + sender + '\n' + "To: " + mail + '\n' + "Subject: " + subject + '\n' + "Date: " + date + '\n' + "Content: " + content + '\n')

banner()
userInput1 = input("Do you wish to use to a custom domain name (Y/N): ").capitalize()

try:

    if userInput1 == 'Y':
        userInput2 = input("\nEnter the name that you wish to use as your domain name(eg.hezronkihiyo): ")
        newMail = f"{API}?login={userInput2}&domain={domain}"
        reqMail = requests.get(newMail)
        mail = f"{extract()[0]}@{extract()[1]}"
        pyperclip.copy(mail)
        print("\nYour private email is " + mail + " (Email address copied to clipboard.)" +"\n")
        print(f"########################## | Inbox of {mail}| ##########################\n")
        while True:
            checkMails()
            time.sleep(5)

    if userInput1 == 'N':
        newMail = f"{API}?login={generateUserName()}&domain={domain}"
        reqMail = requests.get(newMail)
        mail = f"{extract()[0]}@{extract()[1]}"
        pyperclip.copy(mail)
        print("\nYour private email is " + mail + " (Email address copied to clipboard.)" + "\n")
        print(f"########################## | Inbox of {mail} | ##########################\n")
        while True:
            checkMails()
            time.sleep(2)

except(KeyboardInterrupt):
    deleteMail()
    print("\nProgramme Interrupted")
    os.system('cls' if os.name == 'nt' else 'clear')








