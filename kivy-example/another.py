from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class ColorGridApp(App):
    def build(self):
        # Create a GridLayout with two columns and one row
        grid_layout = GridLayout(cols=2, rows=1, spacing=10, padding=10)

        # Colors for the labels
        label_colors = [(0.2, 0.7, 0.3, 1), (0.8, 0.4, 0.1, 1)]  # Green and Orange

        for i, color in enumerate(label_colors):
            # Create a Label for each cell
            label = Label(
                text=f"Label {i + 1}",
                font_size='20sp',
                halign='center',
                valign='middle',
            )

            # Set the background color using canvas.before
            with label.canvas.before:
                Color(*color)
                Rectangle(pos=label.pos, size=label.size)

            # Add the label to the GridLayout
            grid_layout.add_widget(label)

        return grid_layout

if __name__ == '__main__':
    ColorGridApp().run()
