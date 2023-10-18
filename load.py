import time
import random
from sense_hat import SenseHat

# Initialize Sense HAT
sense = SenseHat()

# Define some colors
red = (255, 0, 0)
green = (0, 255,0)
blue = (0, 0, 255)

# Function to fill the LED matrix with random colors
def fill_random_color():
    for i in range(8):
        for j in range(8):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            sense.set_pixel(i, j, r, g, b)

# Function to simulate a CPU-intensive task
def cpu_intensive_task():
    for _ in range(1000000):
        _ = 2 ** 2

try:
    while True:
        # Fill the LED matrix with a random color pattern
        fill_random_color()

        # Read sensor data
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()
        gyro = sense.get_gyroscope()
        accel = sense.get_accelerometer()
        mag = sense.get_compass()
        
        # Display sensor data on the LED matrix
        message = f"Temp: {temperature:.1f}C  Humid: {humidity:.1f}%  Pressure: {pressure:.2f}hPa"
        sense.show_message(message, text_colour=blue)

        # Print sensor data to the console
        print("Sensor Data:")
        print(f"Temperature: {temperature:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
        print(f"Pressure: {pressure:.2f}hPa")
        print(f"Gyroscope Data: Pitch={gyro['pitch']:.2f} Roll={gyro['roll']:.2f} Yaw={gyro['yaw']:.2f}")
        print(f"Accelerometer Data: Pitch={accel['pitch']:.2f} Roll={accel['roll']:.2f} Yaw={accel['yaw']:.2f}")
        print(f"Magnetometer Data: {mag:.2f}")

        # Simulate a CPU-intensive task
        cpu_intensive_task()

except KeyboardInterrupt:
    sense.clear()  # Clear the LED matrix on program exit
