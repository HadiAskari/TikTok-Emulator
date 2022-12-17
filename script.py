# Get Android 12 Image
# docker run --privileged -d -p 6080:6080 -p 5554:5554 -p 5555:5555 -e DEVICE="Samsung Galaxy S6" -e DATAPARTITION="2000m" budtmo/docker-android-x86-12.0
# adb kill-server

from ppadb.client import Client as AdbClient
from bs4 import BeautifulSoup
from random import randint
import re
from time import sleep

def find_element(attrs):
    # grab page xml
    out = randint(10000, 99999)
    device.shell('uiautomator dump /sdcard/%s.xml' % out)
    device.pull('/sdcard/%s.xml' % out, 'xml/%s.xml' % out)
    
    # extract element from page xml
    with open('xml/%s.xml' % out) as f:
        soup = BeautifulSoup(f.read(), 'xml')
        return soup.find('node', attrs=attrs)


def get_coordinates(node):
    bounds = node['bounds']
    tokens = re.sub(r'[\[\]]', ',', bounds).split(',')
    return (int(tokens[1]) + int(tokens[4])) / 2, (int(tokens[2]) + int(tokens[5])) / 2
    
def tap(coords):
    device.shell('input tap %d %d' % coords)

# get device from adb
client = AdbClient(host="127.0.0.1", port=5037)
device = client.devices()[0]

# setup and launch tiktok apk
device.install('/home/mharoon/Downloads/TikTok_27.1.3_Apkpure.apk')
device.shell('monkey -p com.ss.android.ugc.trill 1')

# wait for app to load
sleep(5)

# Get bound element
login_btn = find_element({'text': re.compile('Use phone.*')})
coords = get_coordinates(login_btn)
tap(coords)
