from time import sleep
from emulator import emulate_new_device

def init_device():
    # emulate a new device
    device = emulate_new_device()

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


def audit(device):
    # swipe over video
    for i in range(100):
        xml = device.get_xml()
        
        # play/pause video
        device.tap((200, 200))

        # swipe to next video
        device.swipe((200, 500), (200, 0))



def main():
    device = init_device()
    print("VNC link:", device.get_vnc_link())
    try:
        login(device, 'auditshorts1@gmail.com', 'ytshortstiktok123!')
        audit(device)
    finally:
        device.shutdown()

if __name__ == '__main__':
    main()