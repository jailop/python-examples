import numpy as np
import matplotlib.pyplot as plt
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock import Clock
import localnet
from pingmanager import PingManager

N = 60
X = list(range(1, N + 1))
Y = [0] * N

class RealTimeLineChart(GridLayout):
    def __init__(self, **kwargs):
        super(RealTimeLineChart, self).__init__(**kwargs)
        self.cols = 2
        self.fig, self.ax = plt.subplots(layout="constrained")
        # plt.style.use('dark_background')
        self.bar_plot = self.ax.bar([], [])
        self.ax.set_xlim(right=0, left=60)
        canvas = FigureCanvasKivyAgg(figure=self.fig)
        canvas.size_hint_x = 1.8
        self.add_widget(canvas)
        button = Button(text='Start')
        button.bind(on_press=self.toggle)
        self.add_widget(button)
        self.start()
        self.pm = None
    def start(self):
        conn = localnet.default_connection()
        self.pm = PingManager(conn['gateway'])
        self.pm.start()
        self.event = Clock.schedule_interval(self.update_plot, 1)
    def stop(self):
        self.event.cancel()
        self.pm.stop()
    def toggle(self, instance):
        if not self.pm:
            self.start()
            instance.text = 'Stop'
        else:
            self.stop()
            self.pm = None
            instance.text = 'Start'
    def update_plot(self, dt):
        if not self.pm or not self.pm.running:
            return 
        Y.append(self.pm.get())
        Y.pop(0)
        self.ax.clear()
        _Y = np.array(Y)
        mean = _Y[np.nonzero(_Y)].mean()
        self.ax.bar(X, Y, width=1.0)
        self.ax.axhline(mean, color="red", label="Mean")
        self.ax.set_ylabel('Response Time (ms)')
        self.ax.set_xlabel('Sequences x 1s')
        self.ax.legend()
        self.ax.grid(visible=True)
        self.children[1].draw()


