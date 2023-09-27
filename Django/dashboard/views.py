from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import RPi.GPIO as GPIO

# Create a class for GPIO control
class GPIOControl:
    def __init__(self, pinup, pindown, pinleft, pinright):
        self.uppin = pinup
        self.downpin = pindown
        self.leftpin = pinleft
        self.rightpin = pinright

        # Set GPIO pin numbering mode
        GPIO.setmode(GPIO.BCM)

        # Setup GPIO pins as output
        GPIO.setup(self.uppin, GPIO.OUT)
        GPIO.setup(self.downpin, GPIO.OUT)
        GPIO.setup(self.leftpin, GPIO.OUT)
        GPIO.setup(self.rightpin, GPIO.OUT)

    def set_pin_state(self, pin, state):
        GPIO.output(pin, state)

class RPi4:
    def __init__(self, pinup, pindown, pinleft, pinright):
        self.gpio_control = GPIOControl(pinup, pindown, pinleft, pinright)

# Initialize RPi4 instance
Rpi = RPi4(19, 20, 21, 16)

# Request handlers
def captureKeyEvent(request):
    if request.method == 'GET':
        return render(request, 'hello.html', {'name': 'Silas'})
    if request.method == 'POST':
        key = request.POST.get('key')
        event = request.POST.get('event')
        print(key, event)

        # Check the key and control the GPIO pin accordingly for both keydown and keyup events
        if event == "keydown":
            if key == 'w' or key == 'ArrowUp':
                Rpi.gpio_control.set_pin_state(Rpi.gpio_control.uppin, GPIO.HIGH)  # Turn on the GPIO pin
            elif key == 's' or key == 'ArrowDown':
                Rpi.gpio_control.set_pin_state(Rpi.gpio_control.downpin, GPIO.HIGH)
            elif key == 'a' or key == 'ArrowLeft':
                Rpi.gpio_control.set_pin_state(Rpi.gpio_control.leftpin, GPIO.HIGH)
            elif key == 'd' or key == 'ArrowRight':
                Rpi.gpio_control.set_pin_state(Rpi.gpio_control.rightpin, GPIO.HIGH)
        elif event == "keyup":
            if key == 'w' or key == 'ArrowUp':
                Rpi.gpio_control.set_pin_state(Rpi.gpio_control.uppin, GPIO.LOW)  # Turn off the GPIO pin
            elif key == 's' or key == 'ArrowDown':
                Rpi.gpio_control.set_pin_state(Rpi.gpio_control.downpin, GPIO.LOW)
            elif key == 'a' or key == 'ArrowLeft':
                Rpi.gpio_control.set_pin_state(Rpi.gpio_control.leftpin, GPIO.LOW)
            elif key == 'd' or key == 'ArrowRight':
                Rpi.gpio_control.set_pin_state(Rpi.gpio_control.rightpin, GPIO.LOW)

        return JsonResponse({'message': 'Key event captured',
                             'key': key,
                             'event': event})

    return JsonResponse({'error': 'Invalid Key'}, status=400)