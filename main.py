from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import temp
import random
import json
from threading import Thread, Event

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

thread = Thread()
thread_stop_event = Event()


class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print("Making random numbers")
        while not thread_stop_event.isSet():
            number = random.randint(10000,99999)
            print(number)
            socketio.emit('newQrCode', str(number), namespace='/test')
            time.sleep(5)

    def run(self):
        self.randomNumberGenerator()


@app.route('/')
def sessions():
    return (str(json.dumps({"arr":temp.readRace()})))

@app.route('/getRace', methods=['GET']):
	return (str(json.dumps({"arr":temp.readRace()}))) 

@app.route('/getRaceDetail',methods=['POST']):
	race = request.get("data")
	return (str(json.dumps({"arr":temp.readRace()}))) 


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

temp.dropDB()
temp.insert()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
