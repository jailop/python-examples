import numpy as np
import matplotlib.pyplot as plt

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.matplotlib import FigureCanvasKivyAgg

from test import *

class BarChart(BoxLayout):
    def __init__(self, **kwargs):
        super(BarChart, self).__init__(**kwargs)
        fig, ax = plt.subplots()
        x = np.arange(60)
        y = np.random.rand(60)
        ax.bar(x, y)
        ax.set_title("Ping")
        ax.set_xlabel("Sequence")
        ax.set_ylabel("Response time")
        canvas = FigureCanvasKivyAgg(figure=fig)
        self.add_widget(canvas)

class InfoItem(GridLayout):
    def __init__(self, key, value, **kwargs):
        super(InfoItem, self).__init__(**kwargs)
        self.cols = 2
        keyLabel = Label(text=key)
        valueInput = TextInput(text=value, readonly=True, multiline=False)
        self.add_widget(keyLabel)
        self.add_widget(valueInput)

class NetworkInfo(ScrollView):
    def __init__(self, attrs, **kwargs):
        super(NetworkInfo, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        header = Label(text="Basic Information")
        layout.add_widget(header)
        for key, value in attrs.items():
            layout.add_widget(InfoItem(key, value))
        layout.add_widget(BarChart(size_hint=(1, 3)))
        self.add_widget(layout)

class ButtonRow(GridLayout):
    def __init__(self, **kwargs):
        super(ButtonRow, self).__init__(**kwargs)
        self.cols = 3
        btnAdvInfo = Button(text="Adv Info")
        btnTesting = Button(text="Testing")
        btnMore = Button(text="More...")
        self.add_widget(btnAdvInfo)
        self.add_widget(btnTesting)
        self.add_widget(btnMore)

class NetworkPanel(GridLayout):
    def __init__(self, **kwargs):
        super(NetworkPanel, self).__init__(**kwargs)
        self.rows = 2
        self.add_widget(NetworkInfo(local_info, size_hint=(1, 0.9)))
        self.add_widget(ButtonRow(size_hint=(1, 0.1)))

class NetworkInfoApp(App):
    def build(self):
        # Create a screen with desired size
        screen = Screen(name="Network Info")
        screen.size = (480, 800)
        screen.add_widget(NetworkPanel())  # Add box layout to screen
        # Create a screen manager (optional for future use)
        sm = ScreenManager()
        sm.add_widget(screen)
        return sm

if __name__ == '__main__':
    NetworkInfoApp().run()
