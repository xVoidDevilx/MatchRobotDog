import time
from adafruit_servokit import ServoKit
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .arrows import colors, arrows
import board
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
pca.frequency = 50
import adafruit_motor.servo
servo = adafruit_motor.servo.Servo(servo_channel)


"""
GPIO 2 & 3 : Sensehat SDA SCL
GPIO 4: GPCLK0 - Sensehat LED Matrix
GPIO 17: joystick on sensehat
GPIO 22: humidity and temp sensor on sensehat
GPIO 27: Pressure and temp sensor on sensehat
GPIO 5 & 6: Orientation and accelerometer
GPIO 13: Fan on Sensehat
"""

# Initialize the PCA9685 and create a servo kit object
kit = ServoKit(channels=16)

# Set the PWM frequency to 50 Hz
kit.servo[0].set_pulse_width_range(500, 2500)  # Servo 0
kit.servo[1].set_pulse_width_range(500, 2500)  # Servo 1


# init a sense hat object for our robot control HMI
global sense
sense = SenseHat()

# Request handlers
def captureKeyEvent(request):
    
    if request.method == 'GET':
        # Check if it's an AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Handle the AJAX request for sensor data
            temperature = sense.get_temperature()
            humidity = sense.get_humidity()
            pressure = sense.get_pressure()
            accelerometer = sense.get_accelerometer_raw()
            gyroscope = sense.get_gyroscope_raw()
            magnetometer = sense.get_compass_raw()
            
            # Create a dictionary to store sensor data
            sensor_data = {
                'temperature': temperature,
                'humidity': humidity,
                'pressure': pressure,
                'accelerometer': accelerometer,
                'gyroscope': gyroscope,
                'magnetometer': magnetometer,
            }
            
            return JsonResponse(sensor_data)
        else:
            # Render the initial HTML page
            return render(request, 'hello.html', {'name': 'Silas'})
    
    if request.method == 'POST':
        key = request.POST.get('key')
        event = request.POST.get('event')
        print(key, event)

        # Check the key and control the GPIO pin accordingly for both keydown and keyup events
        if event == "keydown":
            if key == 'w' or key == 'ArrowUp':
                pixels = [colors['red'] if pixel == 1 else colors['white'] for pixel in arrows['up']]
                sense.set_pixels(pixels)
                kit.servo[0].angle = 90
                kit.servo[1].angle = 0
            elif key == 's' or key == 'ArrowDown':
                pixels = [colors['red'] if pixel == 1 else colors['white'] for pixel in arrows['down']]
                sense.set_pixels(pixels)
            elif key == 'a' or key == 'ArrowLeft':
                pixels = [colors['red'] if pixel == 1 else colors['white'] for pixel in arrows['left']]
                sense.set_pixels(pixels)
            elif key == 'd' or key == 'ArrowRight':
                pixels = [colors['red'] if pixel == 1 else colors['white'] for pixel in arrows['right']]
                sense.set_pixels(pixels)
        
        #key release event
        elif event == "keyup":
            sense.clear()   #clear the sensehat matrix
            if key == 'w' or key == 'ArrowUp':
                kit.servo[0].angle = 0
                kit.servo[1].angle = 90
            elif key == 's' or key == 'ArrowDown':
                pass
            elif key == 'a' or key == 'ArrowLeft':
                pass
            elif key == 'd' or key == 'ArrowRight':
                pass

        return JsonResponse({'message': 'Key event captured',
                             'key': key,
                             'event': event})

    return JsonResponse({'error': 'Invalid Key'}, status=400)

def get_sensor_data(request):
    
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()
    
    accelerometer = sense.get_accelerometer_raw()
    gyroscope = sense.get_gyroscope_raw()
    magnetometer = sense.get_compass_raw()
    
    
    # Create a dictionary to store all sensor data
    sensor_data = {
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'accelerometer': accelerometer,
        'gyroscope': gyroscope,
        'magnetometer': magnetometer,
    }
    
    return JsonResponse(sensor_data)