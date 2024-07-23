from kivy.app import App

class Main(App):
    def build(self):
        return MainBox()


if __name__ == "__main__":
    Main().run()
