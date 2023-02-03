import names
from random import choice, randint
from uuid import uuid4

def generate_email():
    domains = ['hotmail.com', 'gmail.com', 'yahoo.com', 'live.com']
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

def lower_keyboard(device):
    device.type_text(111)