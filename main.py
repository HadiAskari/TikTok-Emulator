from argparse import ArgumentParser
from random import randint
from time import sleep
import util
from emulator import emulate_new_device, get_connected_devices
from collections import namedtuple
import screens
import os
import pandas as pd
import json
import re

def parse_args():
    args = ArgumentParser()
    args.add_argument('--query', required=True)
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
        if apk.endswith('.apk'):
            device.install_apk(os.path.join('apks', apk))

def configure_keyboard(device):
    device.set_keyboard('io.github.visnkmr.nokeyboard/.IMEService')

def restart_app(device):
    device.kill_app('com.ss.android.ugc.trill')
    device.launch_app('com.ss.android.ugc.trill')
    sleep(10)

def signup_controller(device, credentials):
    while True:
        xml = device.get_xml()
        if "Don’t have an account? Sign up" in xml:
            print("Signup screen. Proceeding.")
            screens.signup_screen(device)
        elif "When’s your birthday?" in xml:
            print("Birthday screen. Waiting.")
            screens.date_of_birth_screen(device, 'Next')
        elif "When’s your birthdate?" in xml:
            print("Birthday screen. Waiting.")
            screens.date_of_birth_screen(device, 'Continue')
        elif "Too many attempts. Try again later." in xml:
            print("Too many attempts. Rebooting.")
            restart_app(device)
        elif 'text="Email"' in xml:
            print("Email screen. Entering email.")
            if "Enter a valid email address" in xml:
                restart_app(device)
            else:
                screens.email_screen(device, credentials.email)
        elif "Verify to continue" in xml:
            print("Captcha screen. Waiting.")
            screens.captcha_screen(device)
        elif "Agree and continue" in xml:
            print("Agree prompt. Agreeing.")
            util.tap_on(device, attrs={'text': 'Agree and continue'})
        elif "Create password" in xml:
            print("Password screen. Entering password.")
            screens.password_screen(device, credentials.password)
        elif "Create nickname" in xml:
            print("Nickname screen. Skipping.")
            screens.skip_screen(device)
        elif "Choose your interests" in xml:
            print("Interests screen. Skipping.")
            screens.skip_screen(device)
        elif "Account Privacy" in xml and "Skip" in xml:
            print("Account privacy screen. Skipping.")
            screens.skip_screen(device)
        elif "Enter phone number" in xml and "Skip" in xml:
            print("Phone number screen. Skipping.")
            screens.skip_screen(device)
        elif "What languages" in xml and "Confirm" in xml:
            print("Language prompt. Confirming.")
            screens.confirm_screen(device)
        elif "access your contacts?" in xml:
            print("Permissions requested. Allowing.")
            screens.permissions_screen(device)
        elif xml == "" or "Swipe up" in xml:
            util.swipe_up(device)
            sleep(5)
            util.play_pause(device)
        elif "Profile" in xml:
            print("Main app screen. Going to Profile.")
            util.tap_on(device, attrs={'text': "Profile"})
            if "Add bio" in xml or "Add friends" in xml:
                print("Account signed-in! Quitting.")
                break
            elif "Sign up for an account" in xml:
                print("Signing up for account")
                util.tap_on(device, attrs={'text': 'Sign up'})

def train(device, query):
    restart_app(device)

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
        text_elems = device.find_elements({'text': re.compile('.+')})

        # build row
        row = {}
        for el in text_elems:
            row[el['resource-id']] = el['text']

        # append to training data
        training_data.append(row)

        # swipe to next video
        util.swipe_up(device)

    return training_data


def test(device, query):
    restart_app(device)

    # start training
    testing_data = []
    for ind in range(5):
        # watch short for a certain time
        sleep(1)

        # pause video
        util.play_pause(device)

        # click on see more to reveal content
        try: util.tap_on(device, {'text': 'See more'})
        except: pass

        # grab xml
        text_elems = device.find_elements({'text': re.compile('.+')})

        # build row
        row = {}
        for el in text_elems:
            row[el['resource-id']] = el['text']
            # like video if it contains the query needed
            if query in el['text']:
                row['liked'] = True
                # click on like and watch for longer
                util.tap_on(device, {'content-desc': 'Like'})
                util.tap_on(device, {'resource-id': 'com.ss.android.ugc.trill:id/c0o'})
                sleep(10)

        # append to training data
        testing_data.append(row)

        # swipe to next
        util.swipe_up(device)

    return testing_data


if __name__ == '__main__':
    args = parse_args()
    
    print("Generating credentials...")
    credentials = generate_credentials(args.query)
    with open(f'credentials/{credentials.name}', 'w') as f:
        json.dump(credentials, f)
        f.write('\n')
    print(credentials)
    
    print("Launching emulator...")
    device = emulate_new_device(credentials.name)
    print("VNC link:", device.get_vnc_link())

    print("Installing APKs...")
    install_apks(device)

    print("Configuring keyboard...")
    configure_keyboard(device)
    
    print("Starting TikTok...")
    restart_app(device)

    try:
        print("Signing up...")
        signup_controller(device, credentials)

        print("Training...")
        training_data = train(device, args.query)

        print("Testing...")
        testing_data = test(device, args.query)

        print("Saving...")
        pd.DataFrame(training_data).to_csv(f'training/{credentials.name}.csv', index=False)
        pd.DataFrame(testing_data).to_csv(f'testing/{credentials.name}.csv', index=False)
        
        print("Shutting down...")
        device.shutdown()
    except Exception as e:
        print(e)
        device.screenshot(f'screenshots/{credentials.name}.png')
        device.destroy()
