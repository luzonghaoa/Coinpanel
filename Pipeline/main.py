import func

def main():
    target_symbol = ['btcusdt']
    default_interval = '1m'
    threads = []
    for s in target_symbol:
        threads.append(func.MyThread(s, default_interval))
        threads[-1].run()

if __name__ == '__main__':
    main()
