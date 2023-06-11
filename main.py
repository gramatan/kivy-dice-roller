from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from random import randint
from datetime import datetime
import logging

logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('my_app.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


class DiceRollerApp(App):
    title = 'Dice Roller'

    def build(self):
        Window.size = (400, 600)
        layout = BoxLayout(orientation='vertical')

        dice_layout_1 = BoxLayout(size_hint=(1, 0.2))
        dice_layout_2 = BoxLayout(size_hint=(1, 0.2))
        dice_layout_3 = BoxLayout(size_hint=(1, 0.2))

        self.log = TextInput(size_hint=(1, 0.4), readonly=True)

        dice_layout_1.add_widget(Button(text="Roll d4", on_press=lambda _: self.roll_dice(4)))
        dice_layout_1.add_widget(Button(text="Roll d6", on_press=lambda _: self.roll_dice(6)))
        dice_layout_1.add_widget(Button(text="Roll d8", on_press=lambda _: self.roll_dice(8)))

        dice_layout_2.add_widget(Button(text="Roll d10", on_press=lambda _: self.roll_dice(10)))
        dice_layout_2.add_widget(Button(text="Roll d12", on_press=lambda _: self.roll_dice(12)))
        dice_layout_2.add_widget(Button(text="Roll d100", on_press=lambda _: self.roll_dice(100)))

        dice_layout_3.add_widget(Button(text="Clear log", on_press=self.show_clear_log_popup))
        dice_layout_3.add_widget(Button(text="Roll d20", on_press=lambda _: self.roll_dice(20)))
        dice_layout_3.add_widget(Button(text="Save log", on_press=self.save_log))

        layout.add_widget(dice_layout_1)
        layout.add_widget(dice_layout_2)
        layout.add_widget(dice_layout_3)
        layout.add_widget(self.log)

        return layout

    def roll_dice(self, sides):
        if sides != " ":
            result = randint(1, int(sides))
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            self.log.text += f"{current_time}: Rolled d{sides}: {result}\n"

    def save_log(self, instance):
        now = datetime.now()
        current_time = now.strftime("%Y%m%d_%H%M%S")
        with open(f"log_{current_time}.txt", 'w') as f:
            f.write(self.log.text)
        popup = Popup(title='Log saved',
                      content=Label(text=f'Log saved as log_{current_time}.txt'),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def show_clear_log_popup(self, instance):
        popup = Popup(title='Confirm Clear',
                      content=Label(text='Are you sure you want to clear the log?'),
                      size_hint=(None, None), size=(400, 200),
                      auto_dismiss=False)
        popup.content.add_widget(Button(text='Cancel', on_press=popup.dismiss))
        popup.content.add_widget(Button(text='Clear', on_press=self.clear_log, on_release=popup.dismiss))
        popup.open()

    def clear_log(self, instance):
        self.log.text = ""


if __name__ == "__main__":
    DiceRollerApp().run()

