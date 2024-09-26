import pyfirmata
import time
import matplotlib.pyplot as plt
import numpy as np
import sys


# Set up the Arduino board connection
board = pyfirmata.Arduino('COM3')  # Replace with your Arduino's port

# Start an iterator thread to avoid buffer overflow
it = pyfirmata.util.Iterator(board)
it.start()

# Define the pins
trig_pin = board.get_pin('d:12:o')  # Trigger pin
echo_pin = board.get_pin('d:13:i')  # Echo pin
servo_pin = board.get_pin('d:10:s')  # Servo pin (PWM)

last_duration = 100
last_distance = 100

def measure_distance():
    # Send a 10us pulse to the trigger pin
    trig_pin.write(0)
    time.sleep(0.000002)
    trig_pin.write(1)
    time.sleep(0.00001)
    trig_pin.write(0)

    # Wait for the echo pin to go HIGH, with timeout
    timeout = time.time() + 0.01  # 10ms timeout
    while echo_pin.read() == 0:
        if time.time() > timeout:
            print("Timeout waiting for HIGH")
            return None  # Return None on timeout
        pass
    start_time = time.time()

    # Wait for the echo pin to go LOW, with timeout
    timeout = time.time() + 0.01  # 10ms timeout
    while echo_pin.read() == 1:
        if time.time() > timeout:
            print("Timeout waiting for LOW")
            return None  # Return None on timeout
        pass
    end_time = time.time()

    # Calculate the duration of the pulse
    duration = end_time - start_time

    # Calculate the distance based on the duration
    distance = (duration * 34300) / 2  # Speed of sound is 34300 cm/s

    # Debugging prints to see what is happening
    global last_duration
    global last_distance

    if duration != last_duration:
        print("Duration:", duration)
        last_duration = duration

    if distance != last_distance:
        print("Distance:", distance)
        last_distance = distance

    return distance



plt.ion()  # Enable interactive mode
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.set_ylim(0, 40)  # Assuming the range is up to 40 cm
ax.set_theta_zero_location('N')
line, = ax.plot([], [], 'r-')
points, = ax.plot([], [], 'ro')

def update_plot(angle, distance):
    theta = np.radians(angle)
    r = distance
    line.set_data([0, theta], [0, r])
    points.set_data([theta], [r])
    plt.draw()
    plt.pause(0.05)  # Increase pause slightly
    plt.gcf().canvas.flush_events()  # Force update

# Main loop to control the servo and read distance
try:
    while True:
        for angle in range(10, 171, 1):  # Move forward
            servo_pin.write(angle)
            time.sleep(0.03)
            distance = measure_distance()
            if distance is not None:
                update_plot(angle, distance)

        for angle in range(170, 9, -1):  # Move backward
            servo_pin.write(angle)
            time.sleep(0.04)
            distance = measure_distance()
            if distance is not None:
                update_plot(angle, distance)

except KeyboardInterrupt:
    print("Exiting...")
    board.exit()
    plt.ioff()
    plt.show()  # Display the final plot before exiting