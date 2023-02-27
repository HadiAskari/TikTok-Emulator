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

def parse_args():
    args = ArgumentParser()
    args.add_argument('--q', required=True)
    args.add_argument('--i', help='Intervention Type', required=True)
    return args.parse_args()

def generate_credentials(q):
    credentials = namedtuple('Credentials', ['name', 'email', 'password'])
    return credentials(
        name='%s-%s' % (q, randint(10000, 99999)),
        email='alex_ruiz3011@youtubeaudit.com',
        password='@5bfec47e'
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
    sleep(30)

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
            if "add bio" in xml or "Add bio" in xml or "Add friends" in xml or "Set up profile" in xml:
                print("Account signed-in! Quitting.")
                break

def training_phase_1(device, query):
    try:
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
        training_data_phase1 = []
        for ind in range(50):
            # watch short for a certain time
            sleep(30)

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
            training_data_phase1.append(row)
            
            # press on hide to hide content
            try: util.tap_on(device, {'text': 'Hide'})
            except: pass

            # swipe to next video
            util.swipe_up(device)
    except Exception as e:
        if e == "'NoneType' object is not subscriptable":
            restart_app(device)

    return training_data_phase1


def training_phase_2(device, query):
    try:
        restart_app(device)

        count=0
        # start training
        training_phase_2_data = []
        while count<=25:
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
            options=[query,"Undefined"]
            hypothesis_template = "The topic of this TikTok is {}."

            for el in text_elems:
                row[el['resource-id']] = el['text']
                # like video if it contains the query needed
                if el['resource-id']=='com.ss.android.ugc.trill:id/bc5':
                    try:
                        text = util.remove_emojis(el['text'])
                    except:
                        text="Unrecognized"
                    text = util.preprocess(text)
                    if text== "":
                        text="Empty"

                    res=classifier(sequences=text, candidate_labels= options, hypothesis_template=hypothesis_template)

                    if res['scores'][0] > 0.90:
                        count+=1
                        print(res['scores'][0])
                        row['liked'] = True
                        # click on like and watch for longer
                        util.tap_on(device, {'content-desc': 'Like'})
                        util.tap_on(device, {'resource-id': 'com.ss.android.ugc.trill:id/c0o'})
                        util.play_pause(device)
                        sleep(90)
                
            # append to training data
            training_phase_2_data.append(row)

            # press on hide to hide content
            try: util.tap_on(device, {'text': 'Hide'})
            except: pass

            # swipe to next
            util.swipe_up(device)
    except Exception as e:
        if e == "'NoneType' object is not subscriptable":
            restart_app(device)

    return training_phase_2_data

#Also code "Cool Down Period Later"

def testing(device):
    try:
        restart_app(device)
        testing_phase1_data = []
        for ind in range(1000):
            # watch short for a certain time
            sleep(1)

            # pause video
            util.play_pause(device)

            # click on see more to reveal content
            try: util.tap_on(device, {'text': 'See more'})
            except: pass

            # grab xml
            text_elems = device.find_elements({'text': re.compile('.+')})

            row = {}

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
        count=0
        while count <= 25:
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
            options=[query,"Undefined"]
            hypothesis_template = "The topic of this TikTok is {}."

            for el in text_elems:
                row[el['resource-id']] = el['text']
                # like video if it contains the query needed
                if el['resource-id']=='com.ss.android.ugc.trill:id/bc5':
                    try:
                        text = util.remove_emojis(el['text'])
                    except:
                        text="Unrecognized"
                    text = util.preprocess(text)
                    if text== "":
                        text="Empty"

                    res=classifier(sequences=text, candidate_labels= options, hypothesis_template=hypothesis_template)

                    if res['scores'][0] > 0.90:
                        count+=1
                        row['Intervened'] = True
                        row['Intervention']= intervention

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
    
    classifier = pipeline("zero-shot-classification",model="facebook/bart-large-mnli")
    
    print("Generating credentials...")
    credentials = generate_credentials(args.q)
    #credentials.name=credentials.name + "big_run"
    print(credentials.name)
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
        # print("Signing up...")
        # signup_controller(device, credentials)

        print("Logging in")
        login_controller(device, credentials)

        print("Training Phase 1...")
        training_data_phase1 = training_phase_1(device, args.q)

        print("Training Phase 2...")
        training_phase_2_data = training_phase_2(device, args.q)
        
        print("Testing Phase 1...")
        testing_phase_1_data = testing(device)

        print("Saving phase 1...")
        pd.DataFrame(training_data_phase1).to_csv(f'training_phase_1/{credentials.name}_big.csv', index=False)
        pd.DataFrame(training_phase_2_data).to_csv(f'training_phase_2/{credentials.name}_big.csv', index=False)
        pd.DataFrame(testing_phase_1_data).to_csv(f'testing_phase_1/{credentials.name}_big.csv', index=False)
        
        print("Intervention... ")

        intervention_data=Intervention(device,args.q, args.i)
        
        print("Testing Phase 2... ")
        testing_phase_2_data = testing(device)

        print("Saving phase 2...")
        pd.DataFrame(intervention_data).to_csv(f'intervention/{credentials.name}_big.csv', index=False)
        pd.DataFrame(testing_phase_2_data).to_csv(f'testing_phase_2/{credentials.name}_big.csv', index=False)


        print("Shutting down...")
        device.shutdown()
    except Exception as e:
        print(e)
        device.screenshot(f'screenshots/{credentials.name}.png')
        # device.destroy()
