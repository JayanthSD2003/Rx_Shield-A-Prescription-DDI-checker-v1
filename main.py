import os
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from ui.screens import LoginScreen, RegisterScreen, WelcomeScreen, DashboardScreen, ResultsScreen, HomeScreen

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class RxShieldApp(App):
    def build(self):
        # Load KV file using resource_path
        kv_path = resource_path(os.path.join('ui', 'rx_shield.kv'))
        Builder.load_file(kv_path)
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(ResultsScreen(name='results'))
        
        return sm

if __name__ == '__main__':
    RxShieldApp().run()
