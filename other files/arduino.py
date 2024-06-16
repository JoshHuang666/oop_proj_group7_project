import tkinter as tk
from pyfirmata import Arduino, util
import time
import threading

class ArduinoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Arduino LED Control")

        # Connect to Arduino
        # Adjust your Arduino connection port accordingly
        self.board = Arduino('/dev/ttyUSB0')

        self.led_pin = self.board.get_pin('d:13:o')  # d for digital, 13 for pin, o for output

        # Create a GUI scale for setting PWM duty cycle
        self.pwm_duty_scale = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, label="PWM Duty Cycle (%)", command=self.update_pwm)
        self.pwm_duty_scale.pack()

        # Initialize duty cycle
        self.pwm_duty_cycle = 0
        self.pwm_thread = None
        self.pwm_stop_event = threading.Event()

    def update_pwm(self, duty_cycle):
        self.pwm_duty_cycle = int(duty_cycle)
        if self.pwm_thread is not None:
            self.pwm_stop_event.set()
            self.pwm_thread.join()
        self.pwm_stop_event.clear()
        self.pwm_thread = threading.Thread(target=self.pwm_loop)
        self.pwm_thread.start()

    def pwm_loop(self):
        while not self.pwm_stop_event.is_set():
            on_time = (self.pwm_duty_cycle / 100) * 0.1
            off_time = 0.1 - on_time
            self.led_pin.write(1)
            time.sleep(on_time)
            self.led_pin.write(0)
            time.sleep(off_time)

    def close(self):
        if self.pwm_thread is not None:
            self.pwm_stop_event.set()
            self.pwm_thread.join()
        self.board.exit()
        self.master.destroy()

# Create the GUI window
root = tk.Tk()
app = ArduinoGUI(root)

# Ensure the application cleans up properly upon exit
root.protocol("WM_DELETE_WINDOW", app.close)

# Run the application
root.mainloop()

