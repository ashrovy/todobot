# The first is to make web requests using Python and we'll use it to interact with the Telegram API (similarly to what we were using our web browser for earlier). We'll use the JSON module to parse the JSON responses from Telegram into Python dictionaries so that we can extract the pieces of data that we need.
import json
import requests
import time
import urllib 
# The next two lines are global variables, where we define our Bot's token that we need to authenticate with the Telegram API, and we create the basic URL that we'll be using in all our requests to the API.
from dbhelper import DBHelper
db = DBHelper()

TOKEN ="262920578:AAFz2vQkrm_gFbxTTMLW45QNlA1N8w8n6vE"
URL = "https://api.telegram.org/bot{}/". format(TOKEN)
# The get_url function simply downloads the content from a URL and gives us a string. We add the .decode("utf8") part for extra compatibility as this is necessary for some Python versions on some platforms
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content
# The get_json_from_url function gets the string response as above and parses this into a Python dictionary using json.loads() (loads is short for Load String).
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js
# get_updates calls the same API command that we used in our browser earlier, and retrieves a list of "updates" (messages sent to our Bot).
def get_updates(offset=None):
    # url = URL + "getUpdates"
    url = URL + "getUpdates" # ?Timeout=100
    if offset:
        # Add an optional offset parameter to our getUpdates function. If this is specified, we'll pass it along to the Telegram API to indicate that we don't want to receive any messages with smaller IDs this.
        # url += "?offset={}".format(offset)
        url += "?offset={}".format(offset) #&offset
    js = get_json_from_url(url)
    return js
# Add a function that calculates the highest ID of all the updates we receive from getUpdates.
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)
#  Again we loop through each update and grab the text and the chat components so that we can look at the text of the message we received and respond to the user who sent it.
"""
def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            items = db.get_items()
            if text in items:
                db.delete_item(text)
                items = db.get_items()
            else:
                db.add_item(text)
                items = db.get_items()
            message = "\n".join(items)
            send_message(message, chat)
        except KeyError:
            pass 
"""
def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items= db.get_items(chat) # penambahan (chat)
        if text == "/delete":
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        elif text == "/start":
            send_message("Celamat Datang ToDoList Chatbot Great Community",chat)        
        elif text == "/done":
            db.get_items(chat)
            keyboard = build_keyboard(items)
            send_message("Ini adalah daftar ToDoList Anda Hari ini", chat, keyboard)
        elif text.startswith("/"):
            continue
        elif text in items:
            db.delete_item(text, chat) # penambahan (chat)
            items = db.get_items(chat) # penambahan (chat)
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        else:
            db.add_item(text, chat) # penambahan (chat)
            items = db.get_items(chat) # penambahan (chat)
            message = "\n".join(items)
            send_message(message, chat)
# get_last_chat_id_and_text provides a simple but inelegant way to get the chat ID and the message text of the most recent message sent to our Bot.
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)
# This function constructs the list of items, turning each item into a list to indicate that it should be an entire row of the keyboard. We then build a dictionary which contains the keyboard as a value to the "keyboard" key and specifies that this keyboard should disappear once the user has made one choice (unlike with a normal keyboard where you might have to press many keys to construct a word, for this keyboard the user will only be choosing one item at a time)
def build_keyboard(items):
    keyboard =[[item] for item in items]
    reply_markup = {"keyboard":keyboard,"one_time_keyboard": True}
    return json.dumps(reply_markup)
# send_message takes the text of the message we want to send (text) and the chat ID of the chat where we want to send the message (chat_id). 
def send_message(text, chat_id, reply_markup=None): # reply_markup --> We also need to teach our send_message() function how to include a custom keyboard when we want it to. Remember that the reply_markup argument that we pass along to Telegram isn't only the keyboard, but instead, an object that includes the keyboard along with other values, such as"one_time_keyboard": True. Because we built the entire object in our build_keyboard() and encoded it as JSON
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def main():
    # last_textchat = (None,None)
    db.setup()
    last_update_id = None
    while True:
        # text, chat = get_last_chat_id_and_text(get_updates())
        updates = get_updates(last_update_id)
        # if(text,chat) != last_textchat:
        if len(updates["result"]) > 0: 
            # send_message(text, chat)
            last_update_id = get_last_update_id(updates) + 1
            # We now also need to remember the most recent message that we replied to (we save this in the last_textchat variable) so that we don't keep on sending the echoes every second to messages that we've already processed. 
            # last_textchat = (text,chat) 
            # echo_all(updates)
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
"""
text, chat = get_last_chat_id_and_text(get_updates())
send_message(text, chat)
"""
