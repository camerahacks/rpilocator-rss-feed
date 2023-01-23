# rpilocator RSS Feed Notifications

This is the official <a href="https://rpilocator.com" target="_blank">rpilocator.com</a> and <a href="https://hwlocator.com" target="_blank">hwlocator.com</a> RSS feed reader and push notification scripts and Node-RED flows. The RSS feed is checked every minute and the script/flow sends a push notification when a product comes in stock.

Send ntfy, Pushbullet, Pushover or Gotify notifications to your device.

If you appreciate the work I do with rpilocator.com and hwlocatorcom consider buying me a coffee. I spend a lot of time looking for Raspberry Pi computers (and other hardware), tweaking the sites, and communicating with different sellers so you don't have to spend your time doing it.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/J3J6BINRX)

## RSS Notification Setup

### Ntfy
Download <a href="https://ntfy.sh/">ntfy</a> to your device (Android/iOS app, webapplication). Subscribe to any desired topic and insert it to the script:
```python
NTFY_TOPIC = '<your topic here>'
```

If you want to use a private ntfy instance, you can also edit the `NTFY_BASE_URL` (without trailing /).

### Pushbullet

Download Pushbullet to your device (Android/iOS App or Browser extension). After logging in to your Pushbullet account, create an Access Token. This token is used to send a push notification to your devices through the Pushbullet API.

Edit the script and enter your Access Token.

```python
PUSHBULLET_TOKEN = '<your access token here>'
```

### Pushover
Download Pushover to your device (Android/iOS/Desktop). After logging in to your Pushover account, register an application. You will need your user key and the application token/key send a push notification to your devices through the Pushover API.

Edit the script and enter your user key and application token/key.

```python
# User Key
PUSHOVER_KEY = '<your user key here>'

# Application Key
PUSHOVER_API_KEY = '<your application key here>'
```

### Gotify
Create an application in your Gotify server. You will need the token from the server to send a push notification to your devices through the Gotify API.

Edit the script and enter your server base URL and application token.

```python
# Gotify Server Base URL e.g. https://mygotifyserver.com
GOTIFY_BASE_URL = '<your gotify server url>'

# Application Key
GOTIFY_TOKEN = '<your application key here>'
```

### Telegram
Create a bot via telegrams 'BotFather'. You will need the token from this and your own telegram chat id.

Edit the script and enter your bot token and chat_id.

```python
# Telegram settings
TELEGRAM_BOT_TOKEN = '<your telegram bot token>'
TELEGRAM_CHAT_ID = '<your telegram chat id>'
```

## Python Dependencies

The script uses the Feedparser module to parse RSS feed information, so you'll have to install it first.

```python
pip install feedparser
```

It also uses Requests to send the notification to the APIs.

```python
pip install requests
```

For the telegram version you will also need the python telegram bot module.
```python
pip install python-telegram-bot
```

## Usage

### Python Scripts

The easiest way to run the Pyhton scrips continuously is to use ```nohup```

```bash
nohup python3 rpilocator-rss-pushbullet.py &
```

### Node-RED Flow

You can import the JSON file into Node-RED as a new flow or just copy and paste it. Make sure to update the authorization information. For example, the Pushbullet node has a ```Access-Token``` header that needs to be update.

## Filters

If you would like to only get notified if certain product categories come in stock in a certain country (for example), you can use the feed customizer at <a href="https://rpilocator.com/about.cfm" target="_blank">rpilocator.com</a> or <a href="https://hwlocator.com/about.cfm" target="_blank">hwlocator.com</a>.

After customzing the feed, update the ```FEED_URL``` variable.

```python
FEED_URL = 'https://rpilocator.com/feed/?country=US,CA&cat=CM4'

```

The example above will only send notifications if Compute Module 4 comes in stock at a US or Canadian store.

## Terms of use

The script is set to check the RSS feed every minute. Don't be tempted to change this to a faster update interval. Faster updates will be blocked and you
will end up missing a stock alert :)

Feel free to modify the script and use with other RSS feeds. If you do so, please change the User Agent to something else. The User Agent is how web servers
identify which software is accessing their website.
