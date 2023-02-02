from ppadb.client import Client as AdbClient
from time import sleep

adb_client = AdbClient(host="127.0.0.1", port=5037)


device = adb_client.devices()[0]

for i in range(100):
    try:
        device.shell('input swipe 200 500 200 0')
        sleep(60)
    except:
        input("Continue swiping?")
