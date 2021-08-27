#!/usr/bin/python3

import asyncio

from carcontrol import Mecanocar
from gamepad import Gamepad


async def main():
    car = Mecanocar()
    gamepad = Gamepad(car)
    task_gamepad = asyncio.create_task(gamepad.gamepadInput())
    task_car = asyncio.create_task(car.drive())
    try:
        print("starting car")
        await task_gamepad
        await task_car
    except KeyboardInterrupt:
        print("byebye")

if __name__ == "__main__":
    asyncio.run(main())
