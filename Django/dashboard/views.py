from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import RPi.GPIO as GPIO
from sense_hat import SenseHat
from .arrows import colors, arrows
"""
GPIO 2 & 3 : Sensehat SDA SCL
GPIO 4: GPCLK0 - Sensehat LED Matrix
GPIO 17: joystick on sensehat
GPIO 22: humidity and temp sensor on sensehat
GPIO 27: Pressure and temp sensor on sensehat
GPIO 5 & 6: Orientation and accelerometer
GPIO 13: Fan on Sensehat
"""

# init a sense hat object for our robot control HMI
global sense
sense = SenseHat()

# For the servos
import time
from adafruit_servokit import ServoKit

#Constants
nbPCAServo=16 

#Parameters
MIN_IMP  =[500 if (i+1)%4!=0 else 0 for i in range(nbPCAServo)]
MAX_IMP  =[2500 if (i+1)%4!=0 else 0 for i in range(nbPCAServo)]
MIN_ANG  =[0 for i in range(nbPCAServo)]
MAX_ANG  =[90 for i in range(nbPCAServo)]

#Objects
pca = ServoKit(channels=16)

# function init 
def init():
    for i in range(nbPCAServo):
        pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])
init()

# function pcaScenario 
def pcaScenario():
    """Scenario to test servo"""
    for i in range(nbPCAServo):
        for j in range(MIN_ANG[i],MAX_ANG[i],1):
            pca.servo[i].angle = j
            time.sleep(0.01)
        pca.servo[i].angle=None #disable channel
        time.sleep(0.5)

def pcaClear():
    for i in range(nbPCAServo):
        pca.servo[i].angle=None #disable channel
        time.sleep(0.5)


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
                pcaScenario()
                #Rpi.gpio_control.set_pin_state(Rpi.gpio_control.uppin, GPIO.HIGH)  # Turn on the GPIO pin
            elif key == 's' or key == 'ArrowDown':
                pixels = [colors['red'] if pixel == 1 else colors['white'] for pixel in arrows['down']]
                sense.set_pixels(pixels)
                #Rpi.gpio_control.set_pin_state(Rpi.gpio_control.downpin, GPIO.HIGH)
            elif key == 'a' or key == 'ArrowLeft':
                pixels = [colors['red'] if pixel == 1 else colors['white'] for pixel in arrows['left']]
                sense.set_pixels(pixels)
                #Rpi.gpio_control.set_pin_state(Rpi.gpio_control.leftpin, GPIO.HIGH)
            elif key == 'd' or key == 'ArrowRight':
                pixels = [colors['red'] if pixel == 1 else colors['white'] for pixel in arrows['right']]
                sense.set_pixels(pixels)
                #Rpi.gpio_control.set_pin_state(Rpi.gpio_control.rightpin, GPIO.HIGH)
        
        #key release event
        elif event == "keyup":
            sense.clear()   #clear the sensehat matrix
            if key == 'w' or key == 'ArrowUp':
                pcaClear()
                #Rpi.gpio_control.set_pin_state(Rpi.gpio_control.uppin, GPIO.LOW)  # Turn off the GPIO pin
            elif key == 's' or key == 'ArrowDown':
                pass
                ##Rpi.gpio_control.set_pin_state(Rpi.gpio_control.downpin, GPIO.LOW)
            elif key == 'a' or key == 'ArrowLeft':
                pass
                #Rpi.gpio_control.set_pin_state(Rpi.gpio_control.leftpin, GPIO.LOW)
            elif key == 'd' or key == 'ArrowRight':
                pass
                #Rpi.gpio_control.set_pin_state(Rpi.gpio_control.rightpin, GPIO.LOW)

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