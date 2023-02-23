import names
from random import choice, randint
from uuid import uuid4
import re

def generate_email():
    domains = ['youtubeaudit.com']
    email = '%s_%s%s@%s' % (names.get_first_name(), names.get_last_name(), randint(1, 999), choice(domains))
    return email.lower()

def generate_password():
    return ('@%s' % uuid4()).split('-')[0]

def swipe_up(device):
    # swipe to next video
    device.swipe((200, 1000), (200, 300))

def play_pause(device):
    # pause video
    device.tap((400, 400))

def tap_on(device, attrs):
    elem = device.find_element(attrs=attrs)
    coords = device.get_coordinates(elem)
    device.tap(coords)

def tap_on_nth(device, attrs, n):
    elem = device.find_elements(attrs=attrs)[n]
    coords = device.get_coordinates(elem)
    device.tap(coords)


def lower_keyboard(device):
    device.type_text(111)

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                    "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def preprocess(text):
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
    text = text.lower()
    return text  
