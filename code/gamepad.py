#!/usr/bin/env python3
'''
    Gamepad input is saved if the pressed button changes.
    Input is written to the car object.
'''

import asyncio
from evdev import InputDevice

class Gamepad():
    '''
        read gamepad input and write it to car object
    '''
    def __init__(self, car=None):
        self.gamepad = InputDevice('/dev/input/event0')
        #self.up = 46
        #self.down = 32
        #self.left = 18
        #self.right = 33
        #self.SL = 37
        #self.SR = 50
        #self.select = 49
        #self.start = 24
        #self.x = 35
        #self.y = 23
        #self.a = 34
        #self.b = 36
        self.lastEvent = 33
        self.car = car
        # get print output for testing purposes
        self.button = {46: "up",
                       32: "down",
                       18: "left",
                       33: "right",
                       23: "y",
                       34: "a",
                       35: "x",
                       36: "b",
                       37: "SL",
                       50: "SR",
                       24: "start",
                       49: "select"}
        # get motor direction from input event
        self.motor = {46: [1, 1, 1, 1],
                      32: [-1, -1, -1, -1],
                      18: [-1, 1, -1, 1],
                      33: [1, -1, 1, -1],
                      23: [0, 1, 0, 1],
                      34: [0, -1, 0, -1],
                      35: [1, 0, 1, 0],
                      36: [-1, 0, -1, 0],
                      37: [-1, -1, 1, 1],
                      50: [1, 1, -1, -1],
                      24: [0, 0, 0, 0]}

    async def gamepadInput(self):
        '''
            read gamepad input and write it to car object
        '''
        async for event in self.gamepad.async_read_loop():
            if event.value == 1:
                if self.lastEvent != event.code and event.code in list(self.motor):
                    if self.car is not None:
                        async with self.car.lock:
                            self.car.setMotorDirection(self.motor[event.code])
                        print("motorD set")
                    print(self.button[event.code])
                    self.lastEvent = event.code


async def main():
    print("press keys")
    while True:
        await asyncio.sleep(0)

if __name__ == "__main__":
    gamepad_controll = Gamepad()
    try:
        futures = [gamepad_controll.gamepadInput(), main()]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(futures))
        loop.close()
        print("byebye")
    except KeyboardInterrupt:
        print("byebye")
