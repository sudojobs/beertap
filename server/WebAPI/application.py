from flask_socketio import SocketIO
from flask import Flask, render_template
from random import random
from time import sleep
from threading import Thread, Event


__author__ = 'Siddharth Jain'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG'] = True

# turn the flask app into a socketio app
socketio = SocketIO(app)

# random number Generator Thread
thread = Thread()
thread_stop_event = Event()


class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        print("Making random numbers")
        while not thread_stop_event.isSet():
            number = round(random() * 10, 3)
            print(number)
            socketio.emit('newnumber', {'number': number}, namespace='/test')
            sleep(self.delay)

    def run(self):
        self.randomNumberGenerator()


@app.route('/')
def index():
    return render_template('table01.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    print('Client connected')

    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
