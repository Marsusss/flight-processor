import time
from modules.arduino import Arduino


def main():
    try:
        arduino = Arduino('/dev/ttyUSB0', 9600)
        print("Arduino initialized.")
        while True:
            if arduino.is_data_available():
                for i in range(10):  # Retry up to 10 times
                    try:
                        read_arduino = arduino.read_line()
                        if read_arduino is not None:
                            print(read_arduino)
                            break  # If reading was successful, break out of the retry loop
                    except Exception as e:
                        if i < 9:  # Don't sleep after the last attempt
                            time.sleep(0.1)
                        else:
                            error_message = "Failed to read from Arduino after 10 attempts."
                            arduino.write(error_message)
                            raise Exception(error_message) from e

    except Exception as e:
        print(f"Error: {e}")
        exit(1)  # End the program

main()


def calculate_state(accelerometer_data, gyroscope_data, magnetometer_data, accelerometer_uncertainty, gyroscope_uncertainty, magnetometer_uncertainty): # The amount of data in here will depend on how wast the pi is compared to the ARduino sensors.
    # Calculate orientation, speed, position, and uncertainty
    pass


def analyse_image(image):
    # Use nn to analyse image and output image_representation
    pass


def calculate_instructions(orientation, speed, position, uncertainty, image_representation):
    # Use nn to calculate motor instructions for the Arduino based on current state and image data.Output is 4 integers representing motor settings
    pass


def send_instructions(instructions):
    # Send instructions to the Arduino, output is binary data representing motor settings
    pass


def get_image():
    # Get image from camera
    pass