#!/usr/bin/python3

import asyncio
import RPi.GPIO as GPIO

from carcontrol import Mecanocar

from gamepad import Gamepad


async def main():
    car = Mecanocar()
    gamepad = Gamepad(car)
    tasks = await asyncio.gather(
            gamepad.gamepadInput(),
            car.drive())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("byebye")
