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
sense = SenseHat()

print(f"Arrows: {arrows}\nColors: {colors}")

# Create a class for GPIO control
# class GPIOControl:
#     def __init__(self, pinup, pindown, pinleft, pinright):
#         self.uppin = pinup
#         self.downpin = pindown
#         self.leftpin = pinleft
#         self.rightpin = pinright

#         # Set GPIO pin numbering mode
#         GPIO.setmode(GPIO.BCM)

#         # Setup GPIO pins as output
#         GPIO.setup(self.uppin, GPIO.OUT)
#         GPIO.setup(self.downpin, GPIO.OUT)
#         GPIO.setup(self.leftpin, GPIO.OUT)
#         GPIO.setup(self.rightpin, GPIO.OUT)

#     def set_pin_state(self, pin, state):
#         GPIO.output(pin, state)

# class RPi4:
#     def __init__(self, pinup, pindown, pinleft, pinright):
#         self.gpio_control = GPIOControl(pinup, pindown, pinleft, pinright)

# # Initialize RPi4 instance
# Rpi = RPi4(19, 20, 21, 16)

# Request handlers
def captureKeyEvent(request):
    
    # Check the Accept header to determine the response format
    if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
        # This is a JSON request, return JSON data
        sense = SenseHat()
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
    else:
        # This is an HTML request, render the HTML template
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
                pass
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
    sense = SenseHat()
    
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