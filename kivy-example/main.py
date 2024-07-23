from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from pingchart import RealTimeLineChart

from test import *

class KeyValue(GridLayout):
    key_attr = StringProperty('')
    value_attr = StringProperty('')

class Default(GridLayout):
    def update(self, props):
        box = self.ids.key_value_props
        for key, value in props.items():
            box.add_widget(KeyValue(key_attr=key, value_attr=value))

class BasicApp(App):
    def build(self):
        d = Default()
        d.update(local_info)
        return d

if __name__ == "__main__":
    Window.size = (480, 800)
    BasicApp().run()
