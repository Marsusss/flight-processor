import serial
import time


class Arduino:
    def __init__(self, port, baud_rate, retries=10, max_lines=10):
        self.port = port
        self.baud_rate = baud_rate
        self.retries = retries
        self.max_lines = max_lines
        self.current_line = 0
        self.ser = None
        self.initialize_serial()

    def initialize_serial(self):
        for i in range(self.retries):  # Retry up to 10 times
            try:
                self.ser = serial.Serial(self.port, self.baud_rate)
                print("Serial port initialized.")
                break
            except serial.SerialException as e:
                if i < self.retries - 1:  # Raise after the last attempt
                    time.sleep(0.2)
                else:
                    raise Exception(f"Failed to initialize serial port after {self.retries} attempts.") from e

    def is_data_available(self):
        return self.ser.in_waiting > 0

    def read_line(self):
        if self.is_data_available():
            try:
                return self.ser.readline().decode('utf-8').strip()
            except Exception as e:
                raise Exception("Error reading line.") from e
        else:
            return None

    def read_binary_line(self):
        if self.is_data_available():
            try:
                return self.ser.readline()
            except Exception as e:
                raise Exception("Error reading binary line.") from e
        else:
            return None

    def write(self, data):
        try:
            self.ser.write(data.encode())
        except Exception as e:
            raise Exception("Error writing data.") from e

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_line >= self.max_lines:
            self.current_line = 0
            raise StopIteration
        line = self.read_line()
        if line is None:
            self.current_line = 0
            raise StopIteration
        else:
            self.current_line += 1
            return line
