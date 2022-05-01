import RPi.GPIO as GPIO
import time

class Servomotor:
    """
    Class to work with servomotor by RPi.GPIO

    Attributes
    ----------
    direction : int
        choose direction of rolling
    mode : int
        mode of rolling
    velocity : int
        count of steps per minute

    """

    def __init__(self, direction: int, mode: int, velocity: int):
        self.direction = direction
        self.mode = mode
        self.velocity = velocity  # steps per minute

        self.sleep_time_for_signal = 0.1
        self.pin_3_YEL = 3  # step
        self.pin_14_BLUE = 14  # (ENA)
        self.pin_4_GREY = 4  # direction (DIR)
        self.pin_17_MS1 = 17  # №6
        self.pin_18_MS2 = 18  # mode


    def initialize_pins(self):
        """
        Initilizes Raspberry pins
        """

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_3_YEL, GPIO.OUT, initial=1)  # step
        GPIO.setup(self.pin_14_BLUE, GPIO.OUT, initial=1)  # (ENA)
        GPIO.setup(self.pin_4_GREY, GPIO.OUT, initial=1)  # (DIR)
        GPIO.setup(self.pin_17_MS1, GPIO.OUT, initial=0)
        GPIO.setup(self.pin_18_MS2, GPIO.OUT, initial=0)

        if self.mode == 1:
            GPIO.output(self.pin_17_MS1, 0)
            GPIO.output(self.pin_18_MS2, 0)
        elif self.mode == 2:
            GPIO.output(self.pin_17_MS1, 1)
            GPIO.output(self.pin_18_MS2, 0)
        elif self.mode == 4:
            GPIO.output(self.pin_17_MS1, 0)
            GPIO.output(self.pin_18_MS2, 1)
        else:
            GPIO.output(self.pin_17_MS1, 1)
            GPIO.output(self.pin_18_MS2, 1)

        GPIO.output(self.pin_4_GREY, self.direction)
        GPIO.output(self.pin_14_BLUE, 0)

    def next_step(self):
        """
        Does one step of servomotor
        """
        GPIO.output(self.pin_3_YEL, 1)
        time.sleep(0.1)
        GPIO.output(self.pin_3_YEL, 0)
        time.sleep(0.1)
