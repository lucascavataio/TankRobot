import json
import os
import pygame

pygame.init()
clock = pygame.time.Clock()


class PS4Controller:

    def __init__(self):

        # Initialize controller
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
        for joystick in self.joysticks:
            joystick.init()

        # Load PS4 button keys from JSON file
        with open(os.path.join("ps4_keys.json"), 'r+') as file:
            self.button_keys = json.load(file)

        # Create dictionary to store analog key values
        self.analog_keys = {0: 0, 1: 0, 2: 0, 3: 0, 4: -1, 5: -1}

        self.triggered_circle = False
        self.triggered_r1 = False
        self.triggered_l1 = False
        self.triggered_triangle = False
        self.triggered_x = False

        self.triggered_touchpad = False

        self.left = False
        self.right = False
        self.forward = False
        self.backward = False
        self.idle = True

    def initialize_joysticks(self):
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
        for joystick in self.joysticks:
            joystick.init()

    def handle_input(self):
        """
        Handle input from the PS4 controller.
        """

        # Get all events from the pygame event queue
        for event in pygame.event.get():

            if not self.left and not self.right and not self.backward and not self.forward:
                self.idle = True
            else:
                self.idle = False

            # Handle button presses
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == self.button_keys['left_arrow']:
                    self.left = True
                if event.button == self.button_keys['right_arrow']:
                    self.right = True
                if event.button == self.button_keys['down_arrow']:
                    self.backward = True
                if event.button == self.button_keys['up_arrow']:
                    self.forward = True

                # Actions
                if event.button == self.button_keys['circle']:
                    self.triggered_circle = True
                if event.button == self.button_keys['touchpad']:
                    self.triggered_touchpad = True
                if event.button == self.button_keys['R1']:
                    self.triggered_r1 = True
                if event.button == self.button_keys['L1']:
                    self.triggered_l1 = True
                if event.button == self.button_keys['triangle']:
                    self.triggered_triangle = True
                if event.button == self.button_keys['x']:
                    self.triggered_x = True

            # Handle button releases
            if event.type == pygame.JOYBUTTONUP:
                if event.button == self.button_keys['left_arrow']:
                    self.left = False
                if event.button == self.button_keys['right_arrow']:
                    self.right = False
                if event.button == self.button_keys['down_arrow']:
                    self.backward = False
                if event.button == self.button_keys['up_arrow']:
                    self.forward = False

                # Actions
                if event.button == self.button_keys['circle']:
                    self.triggered_circle = False
                if event.button == self.button_keys['touchpad']:
                    self.triggered_touchpad = False
                if event.button == self.button_keys['R1']:
                    self.triggered_r1 = False
                if event.button == self.button_keys['L1']:
                    self.triggered_l1 = False
                if event.button == self.button_keys['triangle']:
                    self.triggered_triangle = False
                if event.button == self.button_keys['x']:
                    self.triggered_x = False

            # Handle analog stick movements
            if event.type == pygame.JOYAXISMOTION:

                self.analog_keys[event.axis] = event.value

                # Horizontal analog stick
                if abs(self.analog_keys[0]) > .4:
                    if self.analog_keys[0] < -.7:
                        self.left = True
                    else:
                        self.left = False
                    if self.analog_keys[0] > .7:
                        self.right = True
                    else:
                        self.right = False

                # Vertical analog stick
                if abs(self.analog_keys[1]) > .4:
                    if self.analog_keys[1] < -.7:
                        self.forward = True
                    else:
                        self.forward = False
                    if self.analog_keys[1] > .7:
                        self.backward = True
                    else:
                        self.backward = False
