from argparse import ArgumentParser
from random import randint
from time import sleep
import util
from emulator import emulate_new_device, get_connected_devices
from collections import namedtuple
import screens
import os
import pandas as pd

def parse_args():
    args = ArgumentParser()
    args.add_argument('--query', default='cricket')
    return args.parse_args()

def generate_credentials(q):
    credentials = namedtuple('Credentials', ['name', 'email', 'password'])
    return credentials(
        name='%s-%s' % (q, randint(10000, 99999)),
        email=util.generate_email(),
        password=util.generate_password()
    )

def install_apks(device):
    for apk in os.listdir('apks'):
        device.install_apk(os.path.join('apks', apk))

def configure_keyboard(device):
    device.set_keyboard('io.github.visnkmr.nokeyboard/.IMEService')

def restart_app(device):
    device.kill_app('com.ss.android.ugc.trill')
    device.launch_app('com.ss.android.ugc.trill')
    sleep(5)

def signup_controller(device, credentials):
    while True:
        xml = device.get_xml()
        if "Don’t have an account? Sign up" in xml:
            screens.signup_screen(device)
        elif "When’s your birthday?" in xml:
            screens.date_of_birth_screen(device, 'Next')
        elif "When’s your birthdate?" in xml:
            screens.date_of_birth_screen(device, 'Continue')
        elif "Too many attempts. Try again later." in xml:
                restart_app(device)
        elif 'text="Email"' in xml:
            if "Enter a valid email address" in xml:
                restart_app(device)
            else:
                screens.email_screen(device, credentials.email)
        elif "Verify to continue" in xml:
            screens.captcha_screen(device)
        elif "Agree and continue" in xml:
            util.tap_on(device, attrs={'text': 'Agree and continue'})
        elif "Create password" in xml:
            screens.password_screen(device, credentials.password)
        elif "Create nickname" in xml:
            screens.nickname_screen(device)
        elif "Choose your interests" in xml:
            screens.interests_screen(device)
        elif 'access your contacts?' in xml:
            screens.permissions_screen(device)
        elif xml == '' or 'Swipe up' in xml:
            util.play_pause(device)
            util.swipe_up(device)
        elif 'Profile' in xml:
            util.tap_on(device, attrs={'text': 'Profile'})
            if 'Add bio' in xml:
                print("Account created!")
                break
            elif 'Sign up for an account' in xml:
                util.tap_on(device, attrs={'text': 'Sign up'})

def train(device, query):
    # click on search button
    device.tap((1000, 120))

    # enter search query
    device.type_text(18)
    device.type_text(query)

    # click search button
    util.tap_on(device, attrs={'text': 'Search'})

    # click first video
    util.tap_on(device, attrs={'resource-id': 'com.ss.android.ugc.trill:id/bc5'})

    # start training
    training_data = []
    for ind in range(5):
        # watch short for a certain time
        sleep(5)

        # pause video
        util.play_pause(device)

        # click on see more to reveal content
        try:
            util.tap_on(device, {'text': 'See more'})
        except:
            pass

        # send signal
        util.tap_on(device, {'content-desc': 'Like'})
        util.tap_on(device, {'resource-id': 'com.ss.android.ugc.trill:id/c0o'})
        
        # check if ok appears
        try: util.tap_on(device, {'text': 'OK'})
        except: pass

        # grab xml
        text_elems = device.find_elements({'text': r'.+'})

        # build row
        row = {}
        for el in text_elems:
            row[el['resource-id']] = el['text']

        # append to training data
        training_data.append(row)

    return training_data


def test(device, query):
    restart_app(device)

    # start training
    testing_data = []
    for ind in range(5):
        # watch short for a certain time
        sleep(5)

        # pause video
        util.play_pause(device)

        # click on see more to reveal content
        try:
            util.tap_on(device, {'text': 'See more'})
        except:
            pass

        # grab xml
        text_elems = device.find_elements({'text': r'.+'})

        # build row
        row = {}
        for el in text_elems:
            row[el['resource-id']] = el['text']
            # like video if it contains the query needed
            row['liked'] = query in el['text']
            if row['liked']:
                util.tap_on(device, {'content-desc': 'Like'})

        # append to training data
        testing_data.append(row)

    return testing_data


if __name__ == '__main__':
    args = parse_args()
    credentials = generate_credentials(args.query)
    print(credentials)
    
    device = emulate_new_device(credentials.name)
    print("VNC link:", device.get_vnc_link())
    
    install_apks(device)
    configure_keyboard(device)
    restart_app(device)

    signup_controller(device, credentials)

    training_data = train(device, args.query)
    testing_data = test(device, args.query)

    pd.DataFrame(training_data).to_csv(f'training/{credentials.name}.csv', index=False)
    pd.DataFrame(testing_data).to_csv(f'testing/{credentials.name}.csv', index=False)
    
    device.shutdown()