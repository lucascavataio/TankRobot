import time
from Robots import TankController
import pyfirmata2
import PS4ControllerLogic as ps4
from Buzzer import BuzzerController
import threading
import pygame

controller = ps4.PS4Controller()

# Initialize Arduino board and LED pin
board = pyfirmata2.Arduino('COM3')
defaultLED = board.get_pin('d:13:o')

morseBuzzer = None #BuzzerController.Buzzer(board, 10)

keepRunning = True

# Define the desired frames per second
FPS = 160

robot = TankController.TankRobot(board)

robot.servo_x.reset_servo_pos()
robot.servo_y.reset_servo_pos()

print("Ready")

if morseBuzzer is not None:
    threading.Thread(target=morseBuzzer.play_morse_thread, args=("Hello", 0.05, 0.15)).start()

# Initialize Pygame for keyboard input handling
pygame.init()
pygame.display.set_mode((100, 100))  # Dummy display to enable Pygame event handling

while keepRunning:
    # Handle Pygame events for keyboard input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepRunning = False

    # Get the current state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Handle controller and keyboard input
    controller.handle_input()

    if controller.idle or not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
        robot.stop_motors()
        defaultLED.write(1)
    else:
        defaultLED.write(0)

    if controller.left or keys[pygame.K_a]:
        robot.turn_left()

    if controller.right or keys[pygame.K_d]:
        robot.turn_right()

    if controller.forward or keys[pygame.K_w]:
        robot.move_fwd()

    if controller.backward or keys[pygame.K_s]:
        robot.move_bwd()

    if controller.triggered_touchpad or keys[pygame.K_SPACE]:
        robot.servo_x.reset_servo_pos()

    if controller.triggered_r1 or keys[pygame.K_RIGHT]:
        robot.servo_x.move_negative()

    if controller.triggered_l1 or keys[pygame.K_LEFT]:
        robot.servo_x.move_positive()

    if controller.triggered_triangle or keys[pygame.K_UP]:
        robot.servo_y.move_negative()

    if controller.triggered_x or keys[pygame.K_DOWN]:
        robot.servo_y.move_positive()

    if controller.triggered_circle or keys[pygame.K_c]:
        if morseBuzzer is not None:
            threading.Thread(target=morseBuzzer.play_morse_thread, args=("Air support", 0.05, 0.15)).start()

    # Add a delay to control the loop speed
    time.sleep(1 / FPS)

board.exit()  # Close the Arduino connection when you're done
pygame.quit()  # Quit Pygame when done
