from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.chip import MDChip
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.clock import Clock

# Import your function
from jobspymodule.searchjobs import get_jobs

# Page 1: Form Screen

class FormScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keywords = []
        self.selected_location = "Select Country"

        layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        # --- Job keyword label ---
        layout.add_widget(
            MDLabel(
                text="Job Keywords",
                font_style="H6",
                size_hint_y=None,
                height="24dp"
            )
        )

        # --- Keyword input ---
        self.title_input = MDTextField(
            hint_text="Type keyword and press Enter",
            multiline=False,
            size_hint_x=1,
            write_tab=False
        )
        self.title_input.bind(on_text_validate=self.add_keyword)
        layout.add_widget(self.title_input)

        # --- Chip box (scrollable) ---
        self.chip_container = MDBoxLayout(
            adaptive_height=True,
            spacing=8,
            padding=(8, 8)
        )

        chip_scroll = MDScrollView(
            size_hint=(1, None),
            height="120dp"
        )
        chip_scroll.add_widget(self.chip_container)
        layout.add_widget(chip_scroll)

        # Location dropdown
        self.location_btn = MDRaisedButton(
            text=self.selected_location,
            on_release=self.open_menu
        )
        layout.add_widget(self.location_btn)

        self.menu = MDDropdownMenu(
            caller=self.location_btn,
            items=[
                {"text": country, "on_release": lambda x=country: self.set_location(x)}
                for country in ["Germany", "Austria", "Switzerland", "USA", "Canada", "UK"]
            ],
            width_mult=4
        )

        # Submit button
        submit_btn = MDRaisedButton(
            text="Submit",
            pos_hint={"center_x": 0.5},
            on_release=self.submit
        )
        layout.add_widget(submit_btn)

        self.add_widget(layout)

    def add_keyword(self, instance):
        keyword = instance.text.strip()
        if not keyword:
            return

        if keyword in self.keywords:
            instance.text = ""
            instance.focus = True
            return

        self.keywords.append(keyword)

        chip = MDChip(
            text=keyword,
            icon="close",
            on_release=lambda x=keyword: self.remove_keyword(x)
        )

        self.chip_container.add_widget(chip)

        # Clear and immediately refocus
        instance.text = ""
        instance.focus = True
        # Also ensure keyboard stays open
        if hasattr(instance, '_keyboard'):
            pass  # Keyboard is already active
        else:
            instance.focus = True


    def remove_keyword(self, keyword):
        self.keywords.remove(keyword)

        self.chip_container.clear_widgets()
        for kw in self.keywords:
            self.chip_container.add_widget(
                MDChip(
                    text=kw,
                    icon="close",
                    on_release=lambda x=kw: self.remove_keyword(x)
                )
            )


    def open_menu(self, instance):
        self.menu.open()

    def set_location(self, location):
        self.selected_location = location
        self.location_btn.text = location
        self.menu.dismiss()

    def submit(self, instance):
        if not self.keywords or self.selected_location == "Select Country":
            return
        
        result_screen = self.manager.get_screen("result")
        result_screen.fetch_and_display(
            self.keywords,
            self.selected_location
        )
        self.manager.current = "result"



# Page 2: Result Screen

class ResultScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.df = None
        self.dialog = None

        self.layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=20
        )

        # Loading label
        self.loading_label = MDLabel(
            text="Loading...",
            halign="center",
            size_hint_y=None,
            height="40dp"
        )
        
        # Scrollview for table
        self.scroll = MDScrollView()
        self.layout.add_widget(self.scroll)

        # Back button
        back_btn = MDFlatButton(
            text="Go Back",
            on_release=self.go_back
        )
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def fetch_and_display(self, keywords, location):
        # Show loading
        self.scroll.clear_widgets()
        self.scroll.add_widget(self.loading_label)
        
        # Fetch data (in real app, do this in a thread)
        try:
            # Call your function
            self.df = get_jobs(location=location, keyword=", ".join(keywords))
            
            if self.df.empty:
                self.show_no_results()
                return
            
            self.display_table()
        except Exception as e:
            self.show_error(str(e))

    def display_table(self):
        self.scroll.clear_widgets()
        
        # Create table container
        table_container = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=10,
            padding=10
        )
        
        # Create rows
        for idx, row in self.df.iterrows():
            row_layout = MDBoxLayout(
                orientation="vertical",
                adaptive_height=True,
                spacing=5,
                padding=10,
                md_bg_color=(0.95, 0.95, 0.95, 1)
            )
            
            # Company
            row_layout.add_widget(
                MDLabel(
                    text=f"[b]Company:[/b] {row.get('company', 'N/A')}",
                    markup=True,
                    size_hint_y=None,
                    height="30dp"
                )
            )
            
            # Location
            row_layout.add_widget(
                MDLabel(
                    text=f"[b]Location:[/b] {row.get('location', 'N/A')}",
                    markup=True,
                    size_hint_y=None,
                    height="30dp"
                )
            )
            
            # Job Title
            row_layout.add_widget(
                MDLabel(
                    text=f"[b]Job Title:[/b] {row.get('jobtitle', 'N/A')}",
                    markup=True,
                    size_hint_y=None,
                    height="30dp"
                )
            )
            
            # Description button
            if 'description' in row and row['description']:
                desc_btn = MDFlatButton(
                    text="View Description",
                    on_release=lambda x, desc=row['description']: self.show_description(desc)
                )
                row_layout.add_widget(desc_btn)
            
            table_container.add_widget(row_layout)
            
            # Add separator
            table_container.add_widget(
                MDLabel(
                    text="",
                    size_hint_y=None,
                    height="10dp"
                )
            )
        
        self.scroll.add_widget(table_container)

    def show_description(self, description):
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title="Job Description",
            text=description,
            size_hint=(0.9, None),
            height="400dp",
            buttons=[
                MDFlatButton(
                    text="Close",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def show_no_results(self):
        self.scroll.clear_widgets()
        self.scroll.add_widget(
            MDLabel(
                text="No jobs found",
                halign="center"
            )
        )

    def show_error(self, error_msg):
        self.scroll.clear_widgets()
        self.scroll.add_widget(
            MDLabel(
                text=f"Error: {error_msg}",
                halign="center"
            )
        )

    def go_back(self, instance):
        self.manager.current = "form"



# App Setup

class MyApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        # Prevent keyboard from auto-dismissing
        from kivy.core.window import Window
        Window.softinput_mode = "below_target"

        sm = MDScreenManager()
        sm.add_widget(FormScreen(name="form"))
        sm.add_widget(ResultScreen(name="result"))
        return sm


if __name__ == "__main__":
    MyApp().run()