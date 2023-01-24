import requests
import feedparser
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

# String to Boolean
def str2bool(str):
    return str.lower() in ("yes", "true", "t", "1")

# Variable loader
def getvar(variable_name, default):
    var = os.getenv(variable_name)
    filevar = variable_name + '_FILE'
    filevarpath = '/run/secrets/' + filevar
    if filevarpath.exists():
        with open(filevarpath, 'r') as f:
            filevarcontent = f.readline()

    if var and filevarcontent:
        print('An environment variable and a Docker Secret have been set for ' + variable_name + '. The Docker Secret will be ignored.')
    
    if var:
        val = var
    elif filevarcontent:
        val = filevarcontent
    elif default:
        val = default
    else:
        val = ''

    return val

# Notification service
NOTIFICATION_SERVICE = getvar('NOTIFICATION_SERVICE', 'ntfy')

# Feed URL
FEED_URL = getvar('FEED_URL', 'https://rpilocator.com/feed/')

# ntfy settings
NTFY_BASE_URL = getvar('NTFY_BASE_URL', 'https://ntfy.sh')
NTFY_TOPIC = getvar('NTFY_TOPIC')
NTFY_PRIORITY = getvar('NTFY_PRIORITY', 'default')
NTFY_EMOJI = getvar('NTFY_EMOJI', 'white_check_mark')

# Gotify settings
GOTIFY_BASE_URL = getvar('GOTIFY_BASE_URL')
GOTIFY_TOKEN = getvar('GOTIFY_TOKEN')
GOTIFY_PRIORITY = getvar('GOTIFY_PRIORITY', 5)

# After creating your pushbullet account, create an 
# Access Token and enter it here
PUSHBULLET_TOKEN = getvar('PUSHBULLET_TOKEN')

# After creating your Pushover account, register your application
# User Key
PUSHOVER_KEY = getvar('PUSHOVER_KEY')
# Application Key
PUSHOVER_API_KEY = getvar('PUSHOVER_API_KEY')

# Initial notifications
INITIAL_NOTIFICATION = str2bool(getvar('INITIAL_NOTIFICATION', False))
ONLINE_NOTIFICATION = str2bool(getvar('ONLINE_NOTIFICATION', True))

# Customize the message title
MESSAGE_TITLE = getvar('MESSAGE_TITLE', 'Pilocator Stock Alert')

# User Agent
USER_AGENT = getvar('USER_AGENT', 'pilocator feed alert')

# Create the message body
def formatMessage(entry):

    match NOTIFICATION_SERVICE:
        case 'ntfy':
            message = entry.title + '\n\n' + 'Link: ' + entry.link
        
        case 'gotify':
            message = {
                'title': MESSAGE_TITLE,
                'message': entry.title + ': ' + entry.link,
                'priority': GOTIFY_PRIORITY,
                'extras': {
                    'client::notification': {
                        'click': {
                            'url': entry.link
                        }
                    }
                }
            }

            message = json.dumps(message)
        
        case 'pushbullet':
            message = {'type': 'link', 'title': MESSAGE_TITLE, 'body': entry.title, 'url': entry.link}

            message = json.dumps(message)

        case 'pushover':
            messageData = 'token='+PUSHOVER_API_KEY+'&user='+PUSHOVER_KEY+'&title='+MESSAGE_TITLE
            message = messageData+'&message='+entry.title+'&url='+entry.link

    return message


# Send the push/message to all devices connected to ntfy
def sendMessage(message):

    match NOTIFICATION_SERVICE:
        case 'ntfy':
            headers = {
                    'Title': MESSAGE_TITLE,
                    'Priority': NTFY_PRIORITY,
                    'Tags': NTFY_EMOJI
            }
            
            try:
                req = requests.post(url=NTFY_BASE_URL + '/' + NTFY_TOPIC, data=message, headers=headers, timeout=20)
            except requests.exceptions.Timeout:
                print('Request Timeout')
                pass
            except requests.exceptions.TooManyRedirects:
                print('Too many requests')
                pass
            except requests.exceptions.RequestException as e:
                print(e)
                pass
        
        case 'gotify':
            headers = {'Content-Type': 'application/json'}
    
            try:
                req = requests.post(url=GOTIFY_BASE_URL + '/message?token=' + GOTIFY_TOKEN, data=message, headers=headers, timeout=20)
            except requests.exceptions.Timeout:
                print('Request Timeout')
                pass
            except requests.exceptions.TooManyRedirects:
                print('Too many requests')
                pass
            except requests.exceptions.RequestException as e:
                print(e)
                pass
        
        case 'pushbullet':
            headers = {'Access-Token': PUSHBULLET_TOKEN, 'Content-Type': 'application/json'}
    
            try:
                req = requests.post(url='https://api.pushbullet.com/v2/pushes', data=message, headers=headers, timeout=20)
            except requests.exceptions.Timeout:
                print('Request Timeout')
                pass
            except requests.exceptions.TooManyRedirects:
                print('Too many requests')
                pass
            except requests.exceptions.RequestException as e:
                print(e)
                pass

        case 'pushover':
            try:
                req = requests.post(url='https://api.pushover.net/1/messages.json', data=message, timeout=20)
            except requests.exceptions.Timeout:
                print('Request Timeout')
                pass
            except requests.exceptions.TooManyRedirects:
                print('Too many requests')
                pass
            except requests.exceptions.RequestException as e:
                print(e)
                pass


# Set control to blank list
control = []

# Fetch the feed
f = feedparser.parse(FEED_URL, agent=USER_AGENT)

class Message(object):
    pass

# Send online message
if ONLINE_NOTIFICATION == True:
    firstmessage = Message()
    firstmessage.title = 'Hello, I am online'
    firstmessage.link = 'https://github.com/camerahacks/rpilocator-rss-feed'
    message = formatMessage(firstmessage)
    sendMessage(message)
if ONLINE_NOTIFICATION == True:
    firstmessage = 'Hello, I am online'
    sendMessage(firstmessage)

# If there are entries in the feed, add entry guid to the control variable
if f.entries:
    for entries in f.entries:
        if INITIAL_NOTIFICATION == True:
            message = formatMessage(entries)
            sendMessage(message)
        control.append(entries.id)

#Only wait 30 seconds after initial run.
time.sleep(30)

while True:
    # Fetch the feed again, and again, and again...
    f = feedparser.parse(FEED_URL, agent=USER_AGENT)

    # Compare feed entries to control list.
    # If there are new entries, send a message/push
    # and add the new entry to control variable
    for entries in f.entries:
        if entries.id not in control:

            message = formatMessage(entries)

            sendMessage(message)

            # Add entry guid to the control variable
            control.append(entries.id)

    time.sleep(59)
