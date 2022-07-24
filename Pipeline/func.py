import threading
import time
import websocket
import json
import pickle
import os
from data_base_connect import connect
from os import listdir
from os.path import isfile, isdir



class MyThread (threading.Thread):
    def __init__(self, symbol, interval):
        threading.Thread.__init__(self)
        self.symbol = symbol
        self.interval = interval
    def run(self):
        print ("Starting " + self.symbol)
        get_data(self.symbol, self.interval)
        print ("Exiting " + self.symbol)

class MyThread2 (threading.Thread):
    def __init__(self, symbol):
        threading.Thread.__init__(self)
        self.symbol = symbol
    def run(self):
        print ("Starting " + self.symbol)
        save_data(self.symbol)
        print ("Exiting " + self.symbol)

def get_data(symbol, interval):

    def on_message(ws, message):
        print(message)
        json_message = json.loads(message)
        s_time = json_message['E']
        sb = json_message['k']['s']
        data_root_path = f'Pipeline/data/{sb}'
        if not os.path.exists(data_root_path):
            os.mkdir(data_root_path)
        filename = data_root_path + f'/{s_time}' + '.pickles'
        print(filename)
        with open(filename, 'ab') as outf:
            pickle.dump(json_message, outf, pickle.HIGHEST_PROTOCOL)

    def on_close(ws, close_status_code, close_msg):
        print("### closed ###")

    socket = f'wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}'
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
    ws.run_forever()

def save_data(symbol):
    connection = connect()
    cursor = connection.cursor()
    print("Start save data into DB")
    # SAVE DATA INTO DB
    root_path = './data/' + symbol
    tmp = []
    files = [root_path + '/' + f for f in listdir(root_path) if isfile(root_path + '/' + f)]
    for f in files:
        with (open(f, "rb")) as openfile:
            try:
                tmp.append(pickle.load(openfile))
            except EOFError:
                print("Error")
    values = []
    for t in tmp:
        t = [t['s'], t['k']['t'], t['k']['T'], t['k']['i'], t['k']['h'],
             t['k']['l'], t['k']['c']]
        values.append(t)
    args_str = ','.join(cursor.mogrify("(%s, %s, %s, %s, %s, %s, %s)", x).decode("utf-8") for x in values)

    cursor.execute("INSERT INTO " + symbol + "VALUES " + args_str)
    cursor.close()
    connection.close()

