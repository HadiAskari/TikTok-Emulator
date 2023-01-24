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

def audit(device):
    # swipe over video
    for i in range(100):
        xml = device.get_xml()
        
        # play/pause video
        device.tap((200, 200))


#device = emulate_new_device()
device = get_connected_devices()[0]
init_device(device)
login(device, 'auditshorts1@gmail.com', 'ytshortstiktok123!')


#def main():
#    print("VNC link:", device.get_vnc_link())
#    try:
#    finally:
#        device.shutdown()

#if __name__ == '__main__':
#    main()
