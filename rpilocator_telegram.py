import telegram, sys
import feedparser
import time
import json

# Feed URL
FEED_URL = 'https://rpilocator.com/feed/'

# Telegram settings
TELEGRAM_BOT_TOKEN = '<your telegram bot token>'
TELEGRAM_CHAT_ID = '<your telegram chat id>'

# Customize the message title
MESSAGE_TITLE = 'xlocator Stock Alert'

# User Agent
USER_AGENT = 'xlocator feed alert'

# Create the message body
def formatMessage(entry):
    message = [
        f"<b><u>{MESSAGE_TITLE}</u></b>",
        f"",
        f"{entry.title}",
        f"",
        f"{entry.link}",
    ]

    message = '\n'.join(message)

    return message

# Telegram Nachricht senden
def sendMessage (message):
    try:
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    except Exception as err:
        print('Unhandled exception while creating telegram bot object: %s' % err, file = sys.stderr)
        return False
    try:
        result_msg = bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='HTML')
        return isinstance(result_msg, telegram.message.Message)
    except Exception as err:
        print('Unhandled exception while sending telegram message: %s' % err, file = sys.stderr)
        return False

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
