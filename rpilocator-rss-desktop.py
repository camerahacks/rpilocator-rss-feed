import feedparser
import time
from plyer import notification
import ssl

# Since the feed is using a self-signed certificate, we need to disable SSL verification
# to prevent the script from throwing an error.
ssl._create_default_https_context = ssl._create_unverified_context

# Feed URL
FEED_URL = 'https://rpilocator.com/feed/'

# User Agent
USER_AGENT = 'xlocator feed alert'

print("Starting rpilocator-rss-desktop.py...")

# Noitfy the user about a new entry
def notifyUser(user_message = 'The stock has been updated!'):
    notification.notify(
        title='Rpilocator Alert',
        message=user_message,
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
else:
    print("No entries in feed.")

# Only wait 30 seconds after initial run.
print("Initial run. Waiting 30 seconds...")
time.sleep(30)

while True:
    print("Checking feed...")
    # Fetch the feed again, and again, and again...
    f = feedparser.parse(FEED_URL, agent=USER_AGENT)

    for entry in f.entries:
        if entry.id not in control:

            # Set the message to the title of the entry
            message = entry.title

            # Duplicate the message to the console
            print(message)

            # Notify the user
            notifyUser(message)

            # Add entry guid to the control variable
            control.append(entry.id)

    # Wait 59 seconds before checking the feed again
    time.sleep(59)