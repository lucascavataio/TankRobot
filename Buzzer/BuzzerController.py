import time
from Utils import MorseConverter


class Buzzer:
    def __init__(self, board, pin):
        self.board = board
        self.buzzer_pin = self.board.get_pin('d:{_pin}:p'.format(_pin=pin))
        self.playingSound = False

    def play_morse(self, text, dot_duration=0.05, dash_duration=0.15):

        if self.playingSound:
            return

        morse_code = MorseConverter.text_to_morse(text)

        print("Playing in morse code:", text, "-", morse_code)

        for symbol in morse_code:
            self.playingSound = True

            if symbol == ".":
                self.buzzer_pin.write(0.5)  # Set the duty cycle (50% for a higher pitch)
                time.sleep(dot_duration)
                self.buzzer_pin.write(0)
                time.sleep(0.1)  # Pause between beeps
            elif symbol == "-":
                self.buzzer_pin.write(0.5)  # Set the duty cycle (50% for a higher pitch)
                time.sleep(dash_duration)
                self.buzzer_pin.write(0)
                time.sleep(0.1)  # Pause between beeps
            elif symbol == " ":
                time.sleep(0.3)  # Pause between words (adjust as needed)

            self.playingSound = False

    def play_morse_thread(self, text, dot_duration=0.05, dash_duration=0.15):
        self.play_morse(text, dot_duration, dash_duration)

