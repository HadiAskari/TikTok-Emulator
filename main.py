from argparse import ArgumentParser
import argparse
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
from transformers import pipeline
from tqdm.auto import tqdm
from classifier import classify


PARAMETERS = dict(
    training_phase_n=25,
    training_phase_sleep=30,
    testing_phase_n=200,
    intervention_phase_n=15
)


def parse_args():
    args = ArgumentParser()
    args.add_argument('--q', required=True)
    args.add_argument('--i', help='Intervention Type', required=True)
    return args.parse_args()

def generate_credentials(q):
    credentials = namedtuple('Credentials', ['name', 'email', 'password'])
    return credentials(
        name='%s' % randint(10000, 99999),
        email='barbara_bergren118@youtubeaudit.com',
        password='@7699cef4'
    )

def install_apks(device):
    for apk in os.listdir('apks'):
        if not apk.endswith('.apk'):
            continue
        package_name = apk[:-4]
        if not device.is_installed(package_name):
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
            print("Captcha screen. Waiting for email.")
            screens.captcha_screen(device)
        elif "Enter 6-digit code" in xml:
            print("Code entry screen. Waiting.")
            screens.code_entry_screen(device, credentials.email)
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
            print("Permissions requested. Denying.")
            screens.permissions_screen(device)
        elif xml == "" or "Swipe up" in xml:
            util.swipe_up(device)
            sleep(5)
            util.play_pause(device)
        elif "Profile" in xml and ("Discover" in xml or "Friends" in xml or "Inbox" in xml):
            print("Main app screen. Going to Profile.")
            util.tap_on(device, attrs={'text': "Profile"})
            if "Add bio" in xml or "Add friends" in xml or 'add bio' in xml or "Complete your profile" in xml:
                print("Account signed-in! Quitting.")
                break
            elif "Sign up for an account" in xml:
                print("Signing up for account")
                util.tap_on(device, attrs={'text': 'Sign up'})

def login_controller(device, credentials):
    while True:
        xml = device.get_xml()
        if "Log in to TikTok" in xml and "Use phone / email / username" in xml:
            print("Login screen")
            screens.login_screen(device, credentials)
        elif 'text="Email / Username"' in xml:
            print("Email screen. Entering email.")
            screens.email_username_screen(device, credentials.email, credentials.password)
        elif "Verify to continue" in xml:
            print("Captcha screen. Waiting.")
            screens.captcha_screen(device)
        elif "When’s your birthdate?" in xml:
            print("Birthday screen. Waiting.")
            screens.date_of_birth_screen(device, 'Continue')
        elif "Choose your interests" in xml:
            print("Interests screen. Skipping.")
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
        elif "Swipe up for more" in xml:
            util.swipe_up(device)
        elif "Profile" in xml and ("Discover" in xml or "Friends" in xml or "Inbox" in xml):
            print("Main app screen. Going to Profile.")
            util.tap_on(device, attrs={'text': "Profile"})
            if "add bio" in xml or "Add bio" in xml or "Add friends" in xml or "Set up profile" in xml:
                print("Account signed-in! Quitting.")
                break

# def training_phase_1(device, query):
#     # start training
#     restart_app(device)
#     training_data_phase1 = []

#     # click on search button
#     device.tap((1000, 120))
#     # device.tap((450, 50))
#     sleep(1)

#     # enter search query
#     device.type_text(18)
#     device.type_text(query)

#     # click search button
#     util.tap_on(device, attrs={'text': 'Search'})
#     sleep(1)

#     # click first video
#     util.tap_on(device, attrs={'resource-id': 'com.ss.android.ugc.trill:id/bc5'})

#     for ind in tqdm(range(5)):
#         # watch short for a certain time
#         sleep(20)

#         # pause video
#         util.play_pause(device)

#         # get xml
#         xml = device.get_xml()

#         # send signal
#         util.like_bookmark_subscribe(device, xml)

#         # click on see more to reveal content
#         try: util.tap_on(device, {'text': 'See more'}, xml)
#         except: pass

#         # grab xml
#         text_elems = device.find_elements({'text': re.compile('.+')}, xml)

#         # build row
#         row = {}
#         for el in text_elems:
#             row[el['resource-id']] = el['text']
        
#         # press on hide to hide content
#         try: util.tap_on(device, {'text': 'Hide'})
#         except: pass

#         # append to training data
#         training_data_phase1.append(row)

#         # swipe to next video
#         sleep(1)
#         util.swipe_up(device)

#     return training_data_phase1


def training_phase_2(device, query):
    restart_app(device)

    count = 0
    # start training
    training_phase_2_data = []
    while count <= PARAMETERS["training_phase_n"]:

        # check for any flow disruptions first
        util.check_disruptions(device)

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
            if el['resource-id'] == 'com.ss.android.ugc.trill:id/bc5':
                text = el['text']

                if classify(query, text):
                    print(text)
                    count += 1
                    row['liked'] = True
                    # click on like and watch for longer
                    util.like_bookmark_subscribe(device)
                    util.play_pause(device)
                    sleep(PARAMETERS["training_phase_sleep"])
            
        # append to training data
        training_phase_2_data.append(row)

        # press on hide to hide content
        try: util.tap_on(device, {'text': 'Hide'})
        except: pass

        # swipe to next
        util.swipe_up(device)
    return training_phase_2_data

#Also code "Cool Down Period Later"

def testing(device):
    try:
        restart_app(device)
        testing_phase1_data = []
        for ind in range(PARAMETERS["testing_phase_n"]):
            # check for any flow disruptions first
            util.check_disruptions(device)
            
            # watch short for a certain time
            sleep(1)

            # pause video
            util.play_pause(device)

            # click on see more to reveal content
            try: util.tap_on(device, {'text': 'See more'})
            except: pass

            # grab xml
            text_elems = device.find_elements({'text': re.compile('.+')})

            # grab text elements
            row = {}
            for el in text_elems:
                row[el['resource-id']] = el['text']

            # append to training data
            testing_phase1_data.append(row)

            # press on hide to hide content
            try: util.tap_on(device, {'text': 'Hide'})
            except: pass

            util.swipe_up(device)
    except Exception as e:
        if e == "'NoneType' object is not subscriptable":
            restart_app(device)

    return testing_phase1_data

def Intervention(device,query, intervention):
    try:
        if intervention=="Not_Interested":
            pass 
        
        restart_app(device)
        intervention_data = []
        count = 0
        
        while count <= PARAMETERS["intervention_phase_n"]:
            # check for any flow disruptions first
            util.check_disruptions(device)
            
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
                if el['resource-id']=='com.ss.android.ugc.trill:id/bc5':
                    text = el['text']

                    if classify(query, text):
                        count += 1
                        row['Intervened'] = True
                        row['Intervention'] = intervention

                        #longtap
                        device.longtap()

                        # click on Not intereseted
                        util.tap_on(device, {'text': 'Not interested'})
                        sleep(1)
                        
            # append to training data
            intervention_data.append(row)

            # press on hide to hide content
            try: util.tap_on(device, {'text': 'Hide'})
            except: pass

            # swipe to next
            util.swipe_up(device)
    except Exception as e:
        if e == "'NoneType' object is not subscriptable":
            restart_app(device)

    return intervention_data


if __name__ == '__main__':
    args = parse_args()
    
    print("Generating credentials...")
    # credentials = generate_credentials(args.q)
    credentials = generate_credentials(None)
    #credentials.name=credentials.name + "big_run"
    # print(credentials.name)
    # with open(f'credentials/{credentials.name}', 'w') as f:
        # json.dump(credentials, f)
        # f.write('\n')
    
    print("Launching emulator...")
    # device = emulate_new_device(credentials.name)
    device = get_connected_devices()[0]
    # print("VNC link:", device.get_vnc_link())


    try:
        print("Installing APKs...")
        install_apks(device)

        print("Configuring keyboard...")
        configure_keyboard(device)
        
        # print("Starting TikTok...")
        # restart_app(device)
        
        # try:
        # print("Signing up...")
        # signup_controller(device, credentials)

        # with open('accounts.txt', 'a') as f:
        #     f.write('\n%s,%s' % (credentials.email, credentials.password))

        # print("Logging in")
        # login_controller(device, credentials)

        # print("Training Phase 1...", util.timestamp())
        # training_data_phase1 = training_phase_1(device, args.q)

        print("Training Phase 2...", util.timestamp())
        training_phase_2_data = training_phase_2(device, args.q)
        
        print("Testing Phase 1...", util.timestamp())
        testing_phase_1_data = testing(device)

        print("Saving...", util.timestamp())
        # pd.DataFrame(training_data_phase1).to_csv(f'training_phase_1/{credentials.name}_big.csv', index=False)
        pd.DataFrame(training_phase_2_data).to_csv(f'training_phase_2/{args.q}_{credentials.name}.csv', index=False)
        pd.DataFrame(testing_phase_1_data).to_csv(f'testing_phase_1/{args.q}_{credentials.name}.csv', index=False)
        
        print("Intervention...", util.timestamp())
        intervention_data = Intervention(device,args.q, args.i)
        
        print("Testing Phase 2... ", util.timestamp())
        testing_phase_2_data = testing(device)

        print("Saving...")
        pd.DataFrame(intervention_data).to_csv(f'intervention/{args.q}_{credentials.name}.csv', index=False)
        pd.DataFrame(testing_phase_2_data).to_csv(f'testing_phase_2/{args.q}_{credentials.name}.csv', index=False)

        device.kill_app('com.ss.android.ugc.trill')
        device.type_text(26)

    except Exception as e:
        device.screenshot(f'screenshots/{credentials.name}.png')
        # device.destroy()

    # finally:
        # pass
        # device.destroy()
    # except Exception as e:
    #     print(e)
    #     device.screenshot(f'screenshots/{credentials.name}.png')
        # device.destroy()
