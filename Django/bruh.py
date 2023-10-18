import time    #https://docs.python.org/fr/3/library/time.html
from adafruit_servokit import ServoKit    #https://circuitpython.readthedocs.io/projects/servokit/en/latest/
#Constants
nbPCAServo=16 
#Parameters
MIN_IMP  =[500 if (i+1)%4!=0 else 0 for i in range(nbPCAServo)]
MAX_IMP  =[2500 if (i+1)%4!=0 else 0 for i in range(nbPCAServo)]
MIN_ANG  =[0 for i in range(nbPCAServo)]
MAX_ANG  =[180 for i in range(nbPCAServo)]
#Objects
pca = ServoKit(channels=16)

# function init 
def init():
    for i in range(nbPCAServo):
        pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])
# function main 
def main():
    pcaScenario();

# function pcaScenario 
def pcaScenario():
    """Scenario to test servo"""
    for i in range(nbPCAServo):
        for j in range(MIN_ANG[i],MAX_ANG[i],1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.servo[i].angle = j
            time.sleep(0.01)
        for j in range(MAX_ANG[i],MIN_ANG[i],-1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.servo[i].angle = j
            time.sleep(0.01)
        pca.servo[i].angle=None #disable channel
        time.sleep(0.5)
if __name__ == '__main__':
    init()
    main()