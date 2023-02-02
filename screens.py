import util

def signup_screen(device):
    util.tap_on(device, {'text': "Don’t have an account? Sign up"})
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

def password_screen(device, password):
    device.type_text(password)
    util.lower_keyboard(device)
    util.tap_on(device, {'text': "Next"})

def nickname_screen(device):
    util.tap_on(device, {'text': "Skip"})

def interests_screen(device):
    util.tap_on(device, {'text': "Skip"})

def permissions_screen(device):
    util.tap_on(device, {'text': 'Allow'})