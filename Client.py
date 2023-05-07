import socketio
sio = socketio.Client()
@sio.event(namespace = '/chat')
def connect():
    print('connection established')
@sio.event
def my_connection(sid, data):
    sio.emit('connection', data, namespace='/chat', skip_sid=sid)
@sio.event
def send_test_message(sid, data):
    sio.on('hello', data, namespace='/chat', skip_sid=sid)
    print(sid)
    print(data)


@sio.on('hello', namespace='/chat')
def receive_test_message(arg1):
    print('I received a message!')
    print(arg1)
    return arg1

@sio.on('switch', namespace='/chat')
def switch_event(arg1, arg2, arg3):
    print('THIS IS SWITCH')
    sw = 'THIS IS SWITCH'
    print("arg1 = ", arg1)
    print("arg2 = ", arg2)
    print("arg3 = ", arg3)
    return(sw, arg1, arg2, arg3)


@sio.on('button', namespace='/chat')
def button_event(arg1, arg2):
    print('THIS IS BUTTON')
    but = 'THIS IS BUTTON'
    print(button_event)
    print("arg1 = ", arg1)
    print("arg2 = ", arg2)
    return(but, arg1, arg2)

def my_custom():
    print("I send smth")
sio.connect('http://localhost:9999', namespaces=['/chat'])