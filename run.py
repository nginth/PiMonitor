from time import sleep
from psutil import cpu_percent
from monitor.monitor import Monitor
from monitor.exiter import Exiter


def cpu_utilization():
    cpu_percent_strs = [str(percent) for percent in cpu_percent(percpu=True)]
    return ','.join(cpu_percent_strs)

if __name__ == '__main__':
    monitor = Monitor()

    monitor.connect()

    exiter = Exiter()
    while not exiter.should_exit:
        monitor.publish(cpu_utilization())
        sleep(5)

    monitor.disconnect()
