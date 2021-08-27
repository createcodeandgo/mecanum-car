#!/usr/bin/env python3
'''
    Controll 4 stepper motors
'''

import asyncio
import RPi.GPIO as GPIO
import time


class Mecanocar():
    """
        control stepper motors
        control over motorDirection, which needs to be locked
    """
    def __init__(self):

        """
            initialize motorDirection
            set GPIO pins
        """
        # the sequence every motor has to run through
        self._stepperSeq = [[1, 0, 0, 1],
                            [1, 0, 0, 0],
                            [1, 1, 0, 0],
                            [0, 1, 0, 0],
                            [0, 1, 1, 0],
                            [0, 0, 1, 0],
                            [0, 0, 1, 1],
                            [0, 0, 0, 1]]

        self._maxSteps = len(self._stepperSeq)

        # the GPIO pins for the stepper motor
        self._stepPins = [[22, 27, 18, 17],
                          [23, 24, 25, 4],
                          [13, 12, 6, 5],
                          [20, 26, 16, 19]]

        GPIO.setmode(GPIO.BCM)
        for pin in self._stepPins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

        self._counter = [0, 0, 0, 0]
        # forward: 1
        # stop: 0
        # backward: -1
        self._motorDirection = [1, -1, 1, -1]
        self._waitTime = 0.001
        # lock for the motor direction
        # also used by gamepad
        self.lock = asyncio.Lock()

    def getMotorDirection(self):
        '''
            used by drive()
        '''
        return self._motorDirection

    def setMotorDirection(self, motorDirection):
        '''
            used by gamepad class
        '''
        self._motorDirection = motorDirection

    async def drive(self):
        '''
            send signals to the stepper motors
        '''
        while True:
            async with self.lock:
                motorD = self.getMotorDirection()
            for pin in range(0, 4):
                for motor in range(0, 4):
                    xpin = self._stepPins[motor][pin]

                    if (motorD != 0):
                        steps = self._counter[motor]
                        output = self._stepperSeq[steps][pin]
                        GPIO.output(xpin, output)

            for motor in range(0, 4):
                self._counter[motor] += motorD[motor]
                if (self._counter[motor] >= self._maxSteps):
                    self._counter[motor] = 0
                if (self._counter[motor] < 0):
                    self._counter[motor] = self._maxSteps - 1
            await asyncio.sleep(self._waitTime)

    def cleanup():
        ''' free the GPIO pins '''
        GPIO.cleanup()


if __name__ == "__main__":
    car = Mecanocar()
    try:
        futures = [car.drive()]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(futures))
        loop.close()
        print("byebye")
        GPIO.cleanup()
    except KeyboardInterrupt:
        print("byebye")
        GPIO.cleanup()
