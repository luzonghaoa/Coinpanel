import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from Pipeline import data_base_connect as dc
import threading
from flask import Flask, request, render_template
import time
from datetime import datetime
import uuid


def send_notification():
    pass

def get_price(symbol):
    connection = dc.connect()
    cursor = connection.cursor()
    query = """
    select close_price from (
    select
        *,
        row_number() over(partition by symbol order by close_time desc) as rn
    from 
    """ + symbol + """
    ) t
            where t.rn = 1
    """
    cursor.execute(query)
    cursor.fetchall()
    res_price = cursor.fetchall()[0][0]
    cursor.close()
    connection.close()
    return res_price


def check_price(symbol, target_price):
    sleep_time = 5
    while True:
        try:
            result = get_price(symbol)
        except Exception:
            status = False
            pass
        if result > target_price:
            send_notification()
        time.sleep(int(sleep_time))

app = Flask("Price Monitor")

@app.route('/mon', methods=['POST'])
def mon():
    data = request.get_json()
    symbol = data['symbol']
    threading.Thread(target=check_price()).start()

app.run(host='0.0.0.0', debug=False, port=10086)
