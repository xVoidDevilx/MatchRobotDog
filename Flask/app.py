# Import main libraries
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Response
from arrows import colors, arrows
import os
import cv2

# Test for RPI library connections
try:
    from sense_hat import SenseHat
    from adafruit_servokit import ServoKit
    RPIConnected = True
except Exception as e:
    print(e)
    print('Install the missing packages for the RPI')
    print('Proceeding in static mode (No Sensor / RPIO response)')
    RPIConnected = False

login_file = 'login.env'    # change this if the .env name changes
admin_info = dict()

# Open the login information on server launch
try:
    with open(login_file) as file:
        for line in file:
            key, value = line.strip().split('=')
            admin_info[key] = value
# An admin control must exist
except FileNotFoundError:
    print(f"Error locating admin file '{login_file}'... aborting.")
    exit()
username = admin_info.get('username')
hashpass = admin_info.get('password')

# Setup the Flask app
app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # Secret key for session management
# Setup the webcam
try:
    camera = cv2.VideoCapture(0)    #open the default webcam
except Exception as e:
    camera = None
    print(f"{e} camera missing. Proceeding with no feed.")

def generate_frames():
    while camera is not None:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# response handler to return a video feed to the clients
@app.route('/video_feed')
def video_feed():
    if camera is None:
        return "Video Feed unavailable"
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Home url handler
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Dashboard url handler
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if session.get('logged_in'):
        return render_template('dashboard.html', user_name=session.get('username'))
    else:
        return render_template('dashboard.html', user_name='Guest')

# Admin Login URL handler
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    
    entered_username = request.form.get('username')
    entered_password = request.form.get('password')

    if entered_username == username and entered_password == hashpass:
        session['logged_in'] = True
        session['username'] = username
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


# logout route handler
@app.route('/logout', methods = ['GET'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('home'))

# Key Logging event handler
@app.route('/key_event', methods=['POST'])
def capture_key_event():

    if not session.get('logged_in'):
        return jsonify({'message': 'Unauthorized. Please log in to transmit key'})

    key = request.form.get('key')
    event = request.form.get('event')
    print(key, event)

    # Handle the key event here, similar to your existing code
    if event == "keydown":
        if key == 'ArrowUp':
            print(f"{colors['red']}\n {arrows['up']}")
        elif key == 'ArrowDown':
            print(f"{colors['black']}\n {arrows['down']}")
        elif key == 'ArrowLeft':
            print(f"{colors['white']}\n {arrows['left']}")
        elif key == 'ArrowRight':
            print(f"{colors['red']}\n {arrows['right']}")
    
    elif event == "keyup":
        if key == 'ArrowUp':
            print(f"{colors['white']}\n {arrows['down']}")
        elif key == 'ArrowDown':
            print(f"{colors['black']}\n {arrows['down']}")
        elif key == 'ArrowLeft':
            print(f"{colors['white']}\n {arrows['down']}")
        elif key == 'ArrowRight':
            print(f"{colors['black']}\n {arrows['down']}")
    
    return jsonify({'message': 'Key event captured', 'key': key, 'event': event})

# Grab sensor data url handle
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

# run if the main process
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    try:
        app.run(host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("Server stopped by keyboard. Exiting...")