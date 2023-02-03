# TikTok-Emulator

## Pre-requisites
### Docker
Follow the guide [here](https://docs.docker.com/engine/install/ubuntu/).
### Android Debug Bridge (ADB)
Install using `sudo apt install adb`.
### Libraries
`pip install pure-python-adb docker beautifulsoup4`
## Running the emulator
- Run using `python main.py --query <hashtag>`
- The program will print a VNC link. Open that in your browser to view the screen.
