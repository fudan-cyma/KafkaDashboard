import json
from flask import Flask, render_template
from flask_socketio import SocketIO
from kafka import  KafkaConsumer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode = 'threading')
thread = None

consumer = KafkaConsumer('result')


def background_thread():
    data_province = {'北京市': 0, '天津市': 0, '河北': 0, '山西': 0, '内蒙古': 0, '辽宁': 0, '吉林': 0, '黑龙江': 0, '上海市': 0, '江苏': 0,
                     '浙江': 0, '安徽': 0, '福建': 0, '江西': 0, '山东': 0, '河南': 0, '湖北': 0, '湖南': 0, '广东': 0, '广西': 0,
                     '海南': 0, '重庆市': 0, '四川': 0, '贵州': 0, '云南': 0, '西藏': 0, '陕西': 0, '甘肃': 0, '青海': 0, '宁夏': 0,
                     '新疆': 0, '香港': 0, '澳门': 0, '台湾': 0}
    data_region = {'North China': 0, 'North East': 0, 'East China': 0, 'Mid South': 0, 'South west': 0,
                   'North west': 0}
    for msg in consumer:

        data_json = msg.value.decode('utf8')
        data_list = json.loads(data_json)
        data_province = dict.fromkeys(data_province, 0)
        data_region = dict.fromkeys(data_region, 0)

        if len(data_list) == 0:
            continue
        for key, value in data_list:
            data_province[key] = int(value)

        data_region['North China'] = data_province['北京市'] + data_province['天津市'] + data_province['河北'] + data_province['山西'] + data_province['内蒙古']
        data_region['North East'] = data_province['辽宁'] + data_province['吉林'] + data_province['黑龙江']
        data_region['East China'] = data_province['上海市'] + data_province['江苏'] + data_province['浙江'] + data_province['安徽'] + data_province['福建'] + data_province['江西'] + data_province['山东'] + data_province['台湾']
        data_region['Mid South'] = data_province['河南'] + data_province['湖北'] + data_province['湖南'] + data_province['广东'] + data_province['广西'] + data_province['海南'] + data_province['香港'] + data_province['澳门']
        data_region['South west'] = data_province['重庆市'] + data_province['四川'] + data_province['贵州'] + data_province['云南'] + data_province['西藏']
        data_region['North west'] = data_province['陕西'] + data_province['甘肃'] + data_province['青海'] + data_province['宁夏'] + data_province['新疆']

        result = ','.join(str(val) for key, val in data_region.items())
        print(result)
        socketio.emit('test_message', {'data': result})


@socketio.on('test_connect')
def connect(message):
    print(message)
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    socketio.emit('connected', {'data': 'Connected'})


@app.route("/")
def handle_mes():
    return render_template("index_v1.html")


if __name__ == '__main__':
    socketio.run(app, debug = False, host='127.0.0.1')