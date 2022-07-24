import func
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=10)
def main():
    target_symbol = ['btcusdt']
    threads = []
    for s in target_symbol:
        threads.append(func.MyThread2(s))
        threads[-1].run()

sched.start()
