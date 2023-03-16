from bs4 import BeautifulSoup
import re
from random import randint

class Android:
    def __init__(self, device, container, vnc_port):
        self.__device = device
        self.__container = container
        self.__vnc_port = vnc_port

    def get_vnc_link(self):
        # print vnc url
        return f'http://localhost:{self.__vnc_port}/'

    def get_xml(self):
        # grab page xml
        out = randint(10000, 99999)
        self.__device.shell('uiautomator dump /sdcard/%s.xml' % out)
        self.__device.pull('/sdcard/%s.xml' % out, 'xml/%s.xml' % out)
        
        # extract element from page xml
        with open('xml/%s.xml' % out) as f:
            return f.read()

    def get_xml_file(self):
        # grab page xml
        out = randint(10000, 99999)
        self.__device.shell('uiautomator dump /sdcard/%s.xml' % out)
        self.__device.pull('/sdcard/%s.xml' % out, 'xml/%s.xml' % out)
        
        # extract element from page xml
        return 'xml/%s.xml' % out
    
    def get_xml_vid(self, run, reason):
        # grab page xml
        out = randint(10000, 99999)
        self.__device.shell('uiautomator dump /sdcard/%s.xml' % out)
        self.__device.pull('/sdcard/%s.xml' % out, 'xml/%s/%s/%s.xml' % (run,reason,out))
        
        # extract element from page xml
        with open('xml/%s/%s/%s.xml' % (run,reason,out)) as f:
            return f.read()
        
    def find_element(self, attrs, xml=None):
        xml = self.get_xml() if xml is None else xml
        soup = BeautifulSoup(xml, 'xml')
        return soup.find('node', attrs=attrs)

    def find_elements(self, attrs, xml=None):
        xml = self.get_xml() if xml is None else xml
        soup = BeautifulSoup(xml, 'xml')
        return soup.find_all('node', attrs=attrs)

    def get_coordinates(self, node):
        # grab bounding box of node
        bounds = node['bounds']
        tokens = re.sub(r'[\[\]]', ',', bounds).split(',')
        return (int(tokens[1]) + int(tokens[4])) / 2, (int(tokens[2]) + int(tokens[5])) / 2
        
    def tap(self, coords):
        # tap a certain coordinate
        self.__device.shell('input tap %d %d' % coords)

    def longtap(self):
        #long tap a certain coordinate
        self.__device.shell('input touchscreen swipe 500 500 500 500 2000')

    def swipe(self, start, end):
        self.__device.shell('input swipe %s %s %s %s' % (start[0], start[1], end[0], end[1]))

    def type_text(self, text):
        # tap in text
        if type(text) == str:
            text = text.replace(' ', '%s')
            self.__device.shell('input text %s' % text)
        elif type(text) == int:
            self.__device.shell('input keyevent %s' % text)

    def install_apk(self, path_to_apk):
        self.__device.install(path_to_apk)

    def is_installed(self, package_name):
        return self.__device.is_installed(package_name)

    def launch_app(self, package_name):
        self.__device.shell(f'monkey -p {package_name} 1')

    def kill_app(self, package_name):
        self.__device.shell(f'am force-stop {package_name}')

    def set_keyboard(self, package_name):
        self.__device.shell(f'settings put secure default_input_method {package_name}')
        self.__device.shell(f'ime enable {package_name}')
        self.__device.shell(f'ime set {package_name}')

    def destroy(self):
        self.__container.kill()
        self.__container.remove()

    def shutdown(self):
        self.__container.stop()

    def screenshot(self, path):
        result = self.__device.screencap()
        with open(path, "wb") as fp:
            fp.write(result)
