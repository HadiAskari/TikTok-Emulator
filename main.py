from time import sleep
from emulator import emulate_new_device, get_connected_devices

def init_device(device):

    # install tiktok apk
    device.install_apk('/home/mharoon/Downloads/TikTok_27.1.3_Apkpure.apk')

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
    device.tap((300, 300))

# get physical device
device = get_connected_devices()[0]

# prep tiktok payload
init_device(device)

# pause video
play_pause(device)

# click on search button
elem = device.find_element(attrs={'resource-id': 'com.ss.android.ugc.trill:id/g1p'})
elem = elem.find_all(attrs={'class': 'android.widget.ImageView'})[-1]
coords = device.get_coordinates(elem)
device.tap(coords)

# enter search query
device.type_text(18)
device.type_text('abortion')

# click search button
elem = device.find_element(attrs={'text': 'Search'})
coords = device.get_coordinates(elem)
device.tap(coords)

# click first video
elem = device.find_element(attrs={'resource-id': 'com.ss.android.ugc.trill:id/x1'})
coords = device.get_coordinates(elem)
device.tap(coords)

# swipe through videos
for i in range(10):
    # watch for 30s
    sleep(30)
    # pause video to grab xml
    play_pause(device)
    xml = device.get_xml()
    # do something here
    swipe_up(device)