# Raspberry Pi Zero Car with Mecanum Wheels
A prototype for a mecanum wheel car that is controlled by a gamepad. 

![The mecanum car without power source.](photos/mecanum-car.png "mecanum car")

### Hardware:
- Raspberry Pi Zero
- 4tronics PiStep2
- Stepper Motors
- Mecanum Wheels

### Software:
The gamepad class uses evdev to capture the gamepad input. Only if the button pressed is different from the previous button the information is passed on to the car class. The variable motorDirection is used by both classes. A lock is used to keep insure its integrity. The car class controlls the stepper motors.

## 3D Printing

I designed an adapter for the stepper motors, because the ones that came with the wheels where for a D profile. 

![A mecanum wheel with the adapter inside.](photos/adapter.jpg "adapter")

The chassis is also a custom design.

![The bare chassis.](photos/chassis.png "chassis")
