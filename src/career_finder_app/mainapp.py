from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from career_finder_app.ui.formscreen import FormScreen
from career_finder_app.ui.resultscreen import ResultScreen
from career_finder_app.ui.coverletterscreen import CoverLetterScreen


class MyApp(MDApp):
    def build(self):
        """
        build the main app
        
        :param self: object
        :return: screen manager
        """
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Prevent keyboard from auto-dismissing
        from kivy.core.window import Window
        Window.softinput_mode = "below_target"

        sm = MDScreenManager()
        sm.add_widget(FormScreen(name="form"))
        sm.add_widget(ResultScreen(name="result"))
        sm.add_widget(CoverLetterScreen(name="cover_letter"))
        return sm


if __name__ == "__main__":
    MyApp().run()