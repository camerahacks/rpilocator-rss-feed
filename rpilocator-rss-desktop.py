import feedparser
import time
from plyer import notification

# Feed URL
FEED_URL = 'https://rpilocator.com/feed/'

# User Agent
USER_AGENT = 'xlocator feed alert'

print("Starting rpilocator-rss-desktop.py...")

def notifyUser():
    notification.notify(
        title='Rpilocator Alert',
        message='The stock has been updated!',
        app_icon=None,
        timeout=10
    )

# Set control to blank list
control = []

# Fetch the feed
f = feedparser.parse(FEED_URL, agent=USER_AGENT)

# If there are entries in the feed, add entry guid to the control variable
if f.entries:
    for entries in f.entries:
        control.append(entries.id)

#Only wait 30 seconds after initial run.
print("Initial run. Waiting 30 seconds...")
time.sleep(30)

while True:
    print("Checking feed...")
    # Fetch the feed again, and again, and again...
    f = feedparser.parse(FEED_URL, agent=USER_AGENT)

    # Compare feed entries to control list.
    # If there are new entries, send a message/push
    # and add the new entry to control variable
    for entry in f.entries:
        if entry.id not in control:
            notifyUser()

            # Add entry guid to the control variable
            control.append(entry.id)

    time.sleep(59)