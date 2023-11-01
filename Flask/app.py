from flask import Flask, render_template, request, jsonify
from arrows import colors, arrows
import os

app = Flask(__name__, static_folder='templates')

@app.route('/')
def dashboard():
    return render_template('dashboard.html', user_name='xVoidDevilx')


@app.route('/key_event', methods=['POST'])
def capture_key_event():
    key = request.form.get('key')
    event = request.form.get('event')
    print(key, event)

    # Handle the key event here, similar to your existing code
    if event == "keydown":
        if key == 'w' or key == 'ArrowUp':
            print(f"{colors['red']}\n {arrows['up']}")
        elif key == 's' or key == 'ArrowDown':
            print(f"{colors['black']}\n {arrows['down']}")
        elif key == 'a' or key == 'ArrowLeft':
            print(f"{colors['white']}\n {arrows['left']}")
        elif key == 'd' or key == 'ArrowRight':
            print(f"{colors['red']}\n {arrows['right']}")
    elif event == "keyup":
        if key == 'w' or key == 'ArrowUp':
            print(f"{colors['white']}\n {arrows['down']}")
        elif key == 's' or key == 'ArrowDown':
            print(f"{colors['black']}\n {arrows['down']}")
        elif key == 'a' or key == 'ArrowLeft':
            print(f"{colors['white']}\n {arrows['down']}")
        elif key == 'd' or key == 'ArrowRight':
            print(f"{colors['black']}\n {arrows['down']}")

    return jsonify({'message': 'Key event captured', 'key': key, 'event': event})

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    # temperature = sense.get_temperature()
    # humidity = sense.get_humidity()
    # pressure = sense.get_pressure()
    temperature = 25.0
    humidity = 60.25
    pressure = 118
    
    accelerometer = {'x': 0.1,
                 'y': 0.2,
                 'z': 0.3}
    gyroscope = {'x': 555.1,
                 'y': 600.2,
                 'z': 310.3}
    magnetometer = {'x': 666.1,
                 'y': 210.2,
                 'z': 690.3}
    # accelerometer = sense.get_accelerometer_raw()
    # gyroscope = sense.get_gyroscope_raw()
    # magnetometer = sense.get_compass_raw()
    
    # Create a dictionary to store sensor data
    sensor_data = {
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'accelerometer': accelerometer,
        'gyroscope': gyroscope,
        'magnetometer': magnetometer,
    }
    
    return jsonify(sensor_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
