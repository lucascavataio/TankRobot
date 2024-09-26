def set_motor_speed(pin_ctrl, pin_pwm, direction, speed):
    pin_ctrl.write(direction)
    # Normalize the speed value to the range of 0 to 1
    normalized_speed = speed / 200.0
    pin_pwm.write(normalized_speed)


class Servo:
    def __init__(self, board, pin, default_angle=90, min_angle=1, max_angle=175, sensitivity=4):
        self.board = board
        self.servo = self.board.get_pin('d:{_pin}:s'.format(_pin=pin))
        self.current_angle = 0
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.sensitivity = sensitivity
        self.default_angle = default_angle

    def reset_servo_pos(self):
        self.move_servo(self.default_angle)

    def move_servo(self, angle):
        # Ensure that angle is within the specified range
        angle = max(min(angle, self.max_angle), self.min_angle)

        # Map the angle from the input range to the output range
        mapped_angle = ((angle - self.min_angle) / (self.max_angle - self.min_angle)) * (
                self.max_angle - self.min_angle) + self.min_angle

        # Write the mapped angle to the servo
        self.servo.write(mapped_angle)
        self.current_angle = mapped_angle

    def move_negative(self, speed=None):

        if speed is None:
            speed = self.sensitivity

        target_angle = self.current_angle - speed

        self.move_servo(target_angle)

    def move_positive(self, speed=None):

        if speed is None:
            speed = self.sensitivity

        target_angle = self.current_angle + speed

        self.move_servo(target_angle)


class TankRobot:

    def __init__(self, board):
        self.board = board

        self.default_speed = 200

        # Define the pins
        self.ML_Ctrl = board.get_pin('d:4:o')  # Direction control pin of the left motor
        self.ML_PWM = board.get_pin('d:6:o')   # PWM control pin of the left motor
        self.MR_Ctrl = board.get_pin('d:2:o')  # Direction control pin of the right motor
        self.MR_PWM = board.get_pin('d:5:o')   # PWM control pin of the right motor

        self.servo_x = Servo(board, 10)  # Servo control
        self.servo_y = Servo(board, 9, 110, 50, 140)  # Servo control

    def move_fwd(self, speed=None):
        if speed is None:
            speed = 55

        set_motor_speed(self.ML_Ctrl, self.ML_PWM, 1, speed)  # 1 for HIGH direction
        set_motor_speed(self.MR_Ctrl, self.MR_PWM, 1, speed)

    def move_bwd(self, speed=None):
        if speed is None:
            speed = 200

        set_motor_speed(self.ML_Ctrl, self.ML_PWM, 0, speed)  # 0 for LOW direction
        set_motor_speed(self.MR_Ctrl, self.MR_PWM, 0, speed)

    def move_fwd_right(self, speed=None):
        if speed is None:
            speed = 200

        set_motor_speed(self.ML_Ctrl, self.ML_PWM, 1, 55)
        set_motor_speed(self.MR_Ctrl, self.MR_PWM, 0, speed)

    def move_fwd_left(self, speed=None):
        if speed is None:
            speed = 200

        set_motor_speed(self.ML_Ctrl, self.ML_PWM, 0, speed)
        set_motor_speed(self.MR_Ctrl, self.MR_PWM, 1, 55)

    def turn_right(self, speed=None):
        if speed is None:
            speed = 200

        set_motor_speed(self.ML_Ctrl, self.ML_PWM, 1, 0)
        set_motor_speed(self.MR_Ctrl, self.MR_PWM, 0, speed)

    def turn_left(self, speed=None):
        if speed is None:
            speed = 200

        set_motor_speed(self.ML_Ctrl, self.ML_PWM, 0, speed)
        set_motor_speed(self.MR_Ctrl, self.MR_PWM, 1, 0)

    def stop_motors(self):
        set_motor_speed(self.ML_Ctrl, self.ML_PWM, 0, 0)
        set_motor_speed(self.MR_Ctrl, self.MR_PWM, 0, 0)
