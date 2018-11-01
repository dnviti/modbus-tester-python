import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pyModbusTCP.client import ModbusClient
import time
import atexit

c = ModbusClient(host="192.168.0.252", port=502, auto_open=True)

# Your Parameters
amp = 1         # 1V        (Amplitude)
f = 50        # 1kHz      (Frequency)
fs = 5000     # 200kHz    (Sample Rate)
T = 1/f
Ts = 1/fs

# Stopwatch Parameters
timeUnit = 2000

# Select if you want to display the sine as a continous wave
#  True = Continous (not able to zoom in x-direction)
#  False = Non-Continous  (able to zoom)
continous = True

x = np.arange(fs)
y = [amp*np.sin(2*np.pi*f * (i/fs)) for i in x]


def curMillis():
    millis = int(round(time.time() * 1000))
    return millis


class Scope(object):
    def __init__(self, ax, maxt=2*T, dt=Ts):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-amp, amp)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if continous:
            if lastt > self.tdata[0] + self.maxt:
                self.ax.set_xlim(lastt-self.maxt, lastt)

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,


def sineEmitter():
    while True:
        # Passo al grafico le info del PLC
        startReadTime = int(round(time.time() * 1000))
        regs = c.read_holding_registers(20, 2)
        endReadTime = int(round(time.time() * 1000))
        elapsedReadTime = endReadTime - startReadTime

        print(str(elapsedReadTime) + ' - ' + str(regs))
        yield y[regs[0]]


fig, ax = plt.subplots()

scope = Scope(ax)

# pass a generator in "sineEmitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, sineEmitter, interval=1,
                              blit=True)

plt.show()
