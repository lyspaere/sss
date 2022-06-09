import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
from loguru import logger


class Video:
    """This is a boilerplate class for creating new demos/games for the SSS platform. It needs to include definitions for the following functions: init, run, stop.
    The init function needs to at least have the things shown below. Frame rate is in frames per second and demo time is in seconds. Demo time should be None if it is a game.
    The run function yields a generator. This generator will be called a specified frame rate, this controls what is being pushed to the screen.
    The stop function is called when the demo/game is being exited by the upper SSS software. It should reset the state for the game"""

    # User input is passed through input_queue
    # Game output is passed through output_queue
    # Screen updates are done through the screen object
    def __init__(self, input_queue, output_queue, screen):
        # Provide the framerate in frames/seconds and the amount of time of the demo in seconds
        self.frame_rate = 25
        self.demo_time = 300  # None for a game

        self.input_queue = input_queue
        self.output_queue = output_queue
        self.screen = screen

        # init demo/game specific variables here
        self.target = "Never_Gonna_Give_You_Up.avi.csv"
        self.pause = False
        self.previous_frame = np.full((2353), 0)

    def is_pause(self, input_queue):
        for input in input_queue:  # allows the user to pause the video
            if input == "LEFT_P":
                self.pause = True
            if input == "RIGHT_P":
                self.pause = False
            if input == "UP_P":
                self.pause = True
                return False
        return self.pause

    def run(self):
        # Create generator here
        while True:
            with open(
                "./demos/video/resorces/pre-processed/" + self.target, "r"
            ) as input_file:
                y = 0
                for index, input_line in enumerate(input_file):
                    while self.is_pause(self.get_input_buff()):
                        yield

                    input_data = input_line.strip("\n").split(",")
                    y = 0
                    for x_index, pixel in enumerate(input_data):
                        if pixel == "":
                            y += 1
                            continue
                        x = x_index % (self.screen.x_width + 1)

                        if not self.previous_frame[int(x_index)] == int(pixel):
                            self.screen.draw_pixel(x, y, int(pixel))
                            self.previous_frame[x_index] = pixel
                    self.screen.push()
                    yield

    def stop(self):
        # Reset the state of the demo if needed, else leave blank
        pass

    def get_input_buff(self):
        # Get all input off the queue
        return list(self.input_queue.queue)