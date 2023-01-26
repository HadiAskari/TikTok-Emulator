from time import sleep
from emulator import emulate_new_device, get_connected_devices
import xml.etree.ElementTree as ET
from collections import defaultdict
import pandas as pd

def init_device(device):

    # install tiktok apk
    #device.install_apk('/home/hadi/Desktop/TikTok-Emulator/tiktok.apk')

    # launch tiktok app
    device.launch_app('com.ss.android.ugc.trill')

    # wait for app to load
    sleep(5)

    return device


def login(device, username, password):

    # Click use phone/email button
    elem = device.find_element({'text': 'Use phone / email / username'})
    coords = device.get_coordinates(elem)
    device.tap(coords)

    sleep(3)

    # Click email button
    elem = device.find_element({'text': 'Email / Username'})
    coords = device.get_coordinates(elem)
    device.tap(coords)


    # Type in email and password
    elem = device.find_element({'text': 'Email / Username'})
    coords = device.get_coordinates(elem)
    device.tap(coords)
    device.type_text(username)

    # Type in password
    elem = device.find_element({'text': 'Password'})
    coords = device.get_coordinates(elem)
    device.tap(coords)
    device.type_text(password)


    # Login
    elem = device.find_element({'text': 'Log in', 'resource-id': 'com.ss.android.ugc.trill:id/e1_'})
    coords = device.get_coordinates(elem)
    device.tap(coords)

def swipe_up(device):
    # swipe to next video
    device.swipe((200, 500), (200, 0))

def play_pause(device):
    # pause video
    device.tap((400, 400))

# get physical device
#device = emulate_new_device()
device = get_connected_devices()[0]

# prep tiktok payload
init_device(device)

# click on search button
device.tap((1000, 120))

# # enter search query
device.type_text(18)
device.type_text('cricket')

# # click search button
elem = device.find_element(attrs={'text': 'Search'})
coords = device.get_coordinates(elem)
device.tap(coords)

# click first video
# elem = device.find_element(attrs={'resource-id': 'com.ss.android.ugc.trill:id/x1'})
# coords = device.get_coordinates(elem)
# device.tap(coords)

#problematic tap
# elem = device.find_element(attrs={'text': 'lakhan.singh007'})
# coords = device.get_coordinates(elem)
# print(coords)
sleep(5)
device.tap((250, 750))

Traindata=defaultdict(list)

desc_train=[]
username_train=[]


#Training
# swipe through videos
for i in range(100):
    # watch for 30s
    sleep(30)
    # pause video to grab xml
    # print('here')
    play_pause(device)
    
    # check if see more exists
    elem = device.find_element(attrs={'text': 'See more'})
    if elem is not None:
        coords = device.get_coordinates(elem)
        device.tap(coords)


    # grab description here and reverse-google search
    xml = device.get_xml_file()
    tree=ET.parse(xml)
    
    for elem in tree.iter():
        dic=elem.attrib
        try:
            if dic['resource-id']=="com.ss.android.ugc.trill:id/bc5":
                desc_train.append(dic['text'])
        except:
            continue

        try:
            if dic['resource-id']=="com.ss.android.ugc.trill:id/title":
                username_train.append(dic['text'])
        except:
            continue
    
    # move to next video
    swipe_up(device)

print(desc_train)
print(username_train)

train_dict={'Usernames':username_train, 'Descriptions': desc_train}
df_train=pd.DataFrame.from_dict(train_dict)
df_train.to_csv("Training.csv")


device.kill_app('com.ss.android.ugc.trill')
device.launch_app('com.ss.android.ugc.trill')

#Test

Testdata=defaultdict(list)

desc_test=[]
username_test=[]

for i in range(50):
    sleep(1)
    # pause video to grab xml
    # print('here')
    play_pause(device)
    
    # check if see more exists
    elem = device.find_element(attrs={'text': 'See more'})
    if elem is not None:
        coords = device.get_coordinates(elem)
        device.tap(coords)


    # grab description here and reverse-google search
    xml = device.get_xml_file()
    tree=ET.parse(xml)

    for elem in tree.iter():
        dic=elem.attrib
        try:
            if dic['resource-id']=="com.ss.android.ugc.trill:id/bc5":
                desc_test.append(dic['text'])
        except:
            continue

        try:
            if dic['resource-id']=="com.ss.android.ugc.trill:id/title":
                username_test.append(dic['text'])
        except:
            continue
    
    # move to next video
    swipe_up(device)

test_dict={'Usernames':username_test, 'Descriptions': desc_test}
df_test=pd.DataFrame.from_dict(test_dict)
df_test.to_csv("Testing.csv")