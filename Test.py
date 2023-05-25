import socketio
sio = socketio.Client()

@sio.event(namespace = '/chat')
def connect():

    print('connection established')

@sio.event
def my_message(sid, data):
    sio.emit('connection', data, namespace='/chat', skip_sid=sid)

@sio.event
def my_message(sid, data):
    sio.on('hello', data, namespace='/chat', skip_sid=sid)
    print(sid)
    print(data)

@sio.on('hello', namespace='/chat')
def on_message(arg1):
    print('I received a message!')
    print(arg1)

# @sio.on('switch', namespace='/chat')
# def on_message(arg1, arg2, arg3):
#     print('THIS IS SWITCH')
#     print("arg1 = ", arg1)
#     print("arg2 = ", arg2)
#     print("arg3 = ", arg3)


@sio.on('button', namespace='/chat')
def on_message(arg1, arg2):
    print('THIS IS BUTTON')
    print("arg1 = ", arg1)
    print("arg2 = ", arg2)

def my_custom():
    print("I send smth")
sio.connect('http://localhost:9999', namespaces=['/chat'])

# from Client import*
#
# command = ''
# arg1 = 0
# arg2 = False
# arg3 = 0
# command, arg1, arg2, arg3 = switch_event()
#
# print(command, arg1, arg2, arg3)

# import serial
#
# connected = False
#
# ser = serial.Serial("/dev/ttyUSB0", 9600)
#
# while not connected:
#     serin = ser.read()
#     connected = True
#     print("Arduino connected")
#
# ser.write("1")
#
# while ser.read() == '1':
#     ser.read()
#     print("Arduino connected")
# ser.close()