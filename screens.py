import util
from time import sleep
import requests

def signup_screen(device):
    util.tap_on(device, {'text': "Don’t have an account? Sign up"})
    sleep(1)
    util.tap_on(device, {'text': "Use phone or email"})

def date_of_birth_screen(device, next_prompt):
    print(">>> Please scroll select date of birth.")
    input('>>> Continue?')
    try: util.tap_on(device, {'text': next_prompt})
    except: pass

def email_screen(device, email):
    util.tap_on(device, {'text': "Email"})
    device.type_text(email)
    util.lower_keyboard(device)
    util.tap_on(device, {'text': "Next"})

def captcha_screen(device):
    print(">>> Please solve captcha")
    input('>>> Continue?')

def code_entry_screen(device, email):
    sleep(15)
    r = requests.get(f'https://youtubeaudit.com/tiktokverificationapi/getVerificationCode/{email}')
    code = r.json()['verification_code']
    for c in code:
        device.type_text(c)
    print(code)
    print(">>> Please enter code")
    input('>>> Continue?')

def password_screen(device, password):
    device.type_text(password)
    util.lower_keyboard(device)
    try: util.tap_on(device, {'text': "Next"})
    except: pass

def skip_screen(device):
    util.tap_on(device, {'text': "Skip"})

def confirm_screen(device):
    util.tap_on(device, {'text': "Confirm"})

def permissions_screen(device):
    try: util.tap_on(device, {'text': "Deny"})
    except: pass
    try: util.tap_on(device, {'text': "DENY"})
    except: pass

def login_screen(device, credentials):
    util.tap_on(device, {'text': "Use phone / email / username"})

def email_username_screen(device, email, password):
    util.tap_on(device, {'text': "Email / Username"})
    device.type_text(email)
    util.tap_on(device, {'text': 'Password'})
    device.type_text(password)
    util.tap_on_nth(device, {'text': 'Log in'}, 1)