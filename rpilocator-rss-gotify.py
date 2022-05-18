import requests
import feedparser
import time
import json

# Feed URL
FEED_URL = 'https://rpilocator.com/feed/'
# FEED_URL = 'https://hwlocator.com/feed/'

# Gotify settings
GOTIFY_BASE_URL = '<your gotify server url>'
GOTIFY_TOKEN = '<your gotify app token>'
GOTIFY_PRIORITY = 5

# Customize the message title
MESSAGE_TITLE = 'xlocator Stock Alert'

# User Agent
USER_AGENT = 'xlocator feed alert'

# Create the message body
def formatMessage(entry):

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

    return message

# Send the push/message to all devices connected to Gotify
def sendMessage(message):
    
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

# Set control to blank list
control = []

# Fetch the feed
f = feedparser.parse(FEED_URL, agent=USER_AGENT)

# If there are entries in the feed, add entry guid to the control variable
if f.entries:
    for entries in f.entries:
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
