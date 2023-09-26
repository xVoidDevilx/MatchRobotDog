const rpio = require('rpio');

// Set the GPIO pin 17 (physical pin 11) to OUTPUT mode
rpio.open(17, rpio.OUTPUT);

// Function to blink the LED
function blinkLED() {
  rpio.write(17, rpio.HIGH); // Turn the LED on
  setTimeout(() => {
    rpio.write(17, rpio.LOW); // Turn the LED off after 1 second
  }, 1000);
}

// Blink the LED every second
setInterval(blinkLED, 2000);

// Stop blinking after 10 seconds
setTimeout(() => {
  rpio.close(17); // Release the GPIO pin
  process.exit(); // Exit the program
}, 10000);
