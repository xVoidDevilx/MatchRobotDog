from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import RPi.GPIO as GPIO

# Create a class for GPIO control
class RPi4(GPIO):
    def __init__(self, pinup, pindown, pinleft, pinright):
        self.uppin = pinup
        self.downpin = pindown
        self.leftpin = pinleft
        self.rightpin = pinright

        # Set GPIO pin numbering mode
        self.setmode(GPIO.BCM)

        # Setup GPIO pins as output
        self.setup(self.uppin, GPIO.OUT)
        self.setup(self.downpin, GPIO.OUT)
        self.setup(self.leftpin, GPIO.OUT)
        self.setup(self.rightpin, GPIO.OUT)

    def set_pin_state(self, pin, state):
        self.output(pin, state)

Rpi = RPi4(21, 19, 13, 26)

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
                Rpi.set_pin_state(Rpi.uppin, GPIO.HIGH)  # Turn on the GPIO pin
            elif key == 's' or key == 'ArrowDown':
                Rpi.set_pin_state(Rpi.downpin, GPIO.HIGH)
            elif key == 'a' or key == 'ArrowLeft':
                Rpi.set_pin_state(Rpi.leftpin, GPIO.HIGH)
            elif key == 'd' or key == 'ArrowRight':
                Rpi.set_pin_state(Rpi.rightpin, GPIO.HIGH)
        elif event == "keyup":
            if key == 'w' or key == 'ArrowUp':
                Rpi.set_pin_state(Rpi.uppin, GPIO.LOW)  # Turn off the GPIO pin
            elif key == 's' or key == 'ArrowDown':
                Rpi.set_pin_state(Rpi.downpin, GPIO.LOW)
            elif key == 'a' or key == 'ArrowLeft':
                Rpi.set_pin_state(Rpi.leftpin, GPIO.LOW)
            elif key == 'd' or key == 'ArrowRight':
                Rpi.set_pin_state(Rpi.rightpin, GPIO.LOW)

        return JsonResponse({'message': 'Key event captured',
                             'key': key,
                             'event': event})

    return JsonResponse({'error': 'Invalid Key'}, status=400)
