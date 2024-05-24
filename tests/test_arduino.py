import unittest
from unittest.mock import patch, Mock
from modules.arduino import Arduino  # Replace 'your_module' with the actual module name

class TestArduino(unittest.TestCase):
    def setUp(self):
        self.mock_serial = patch('modules.arduino.serial.Serial').start()
        self.port = '/dev/ttyUSB0'  # Replace with your actual port
        self.baud_rate = 9600
        self.arduino = Arduino(self.port, self.baud_rate)

    def tearDown(self):
        patch.stopall()

    def test_init(self):
        # Check that the serial.Serial constructor was called with the correct arguments
        self.mock_serial.assert_called_once_with(self.port, self.baud_rate)

        # Check that the 'initialize_serial' method was called
        self.assertTrue(hasattr(self.arduino, 'ser'))
        self.assertEqual(self.arduino.ser, self.mock_serial.return_value)
        self.assertEqual(self.arduino.retries, 10)
        self.assertEqual(self.arduino.port, self.port)
        self.assertEqual(self.arduino.baud_rate, self.baud_rate)

    def test_iter(self):
        # Mock the readline method of the serial object
        self.arduino.ser.readline.return_value = b'test line\n'
        self.arduino.ser.in_waiting = 1

        # Test iterating over the Arduino object
        lines = list(self.arduino)
        self.assertEqual(lines, ['test line' for _ in range(10)])

        # Test when no data is available
        self.arduino.ser.in_waiting = 0
        with self.assertRaises(StopIteration):
            next(self.arduino)

    def test_is_data_available(self):
        # Mock the in_waiting property of the serial object
        self.arduino.ser.in_waiting = 5
        self.assertTrue(self.arduino.is_data_available())

        # Test when no data is available
        self.arduino.ser.in_waiting = 0
        self.assertFalse(self.arduino.is_data_available())

    def test_read_line(self):
        # Mock the readline method of the serial object
        self.arduino.ser.readline.return_value = b'test line\n'
        self.arduino.ser.in_waiting = 1

        # Test reading a line
        self.assertEqual(self.arduino.read_line(), 'test line')

        # Test when no data is available
        self.arduino.ser.in_waiting = 0
        self.assertIsNone(self.arduino.read_line())

        # Test exception handling
        self.arduino.ser.readline.side_effect = Exception('readline error')
        self.arduino.ser.in_waiting = 1
        with self.assertRaises(Exception) as context:
            self.arduino.read_line()
        self.assertTrue('Error reading line.' in str(context.exception))

    def test_write(self):
        # Test writing data
        self.arduino.write('test data')
        self.arduino.ser.write.assert_called_once_with(b'test data')

        # Test exception handling
        self.arduino.ser.write.side_effect = Exception('write error')
        with self.assertRaises(Exception) as context:
            self.arduino.write('test data')
        self.assertTrue('Error writing data.' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
