from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.chip import MDChip
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView


class FormScreen(MDScreen):
    def __init__(self, **kwargs):
        """
        initialize form screen and layout of the screen

        :param self: object
        :param kwargs: additional arguments
        """
        super().__init__(**kwargs)

        self.selected_location = "Select Country"
        self.keywords = []

        layout = MDBoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        layout.add_widget(
            MDLabel(
                text="Job Keywords",
                font_style="H6",
                size_hint_y=None,
                height="24dp"
            )
        )

        # Keyword input
        self.title_input = MDTextField(
            hint_text="Type keyword and press Enter",
            multiline=False,
            write_tab=False
        )
        self.title_input.bind(on_text_validate=self.add_keyword)
        layout.add_widget(self.title_input)

        # Chip container
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
            pos_hint={"center_x": 0.5},
            on_release=self.open_menu
        )
        layout.add_widget(self.location_btn)

        self.menu = MDDropdownMenu(
            caller=self.location_btn,
            items=[
                {
                    "text": country,
                    "on_release": lambda x=country: self.set_location(x)
                }
                for country in ["Germany", "Austria", "Switzerland", "USA", "Canada", "UK"]
            ],
            width_mult=4
        )

        #find_jobs button 
        find_jobs_btn = MDRaisedButton(
            text="Find Jobs",
            pos_hint={"center_x": 0.5},
            on_release=self.find_jobs
        )
        layout.add_widget(find_jobs_btn)

        self.add_widget(layout)



    def add_keyword(self, instance):
        """
        add a keyword from the input field
        
        :param self: object
        :param instance: widget instance
        """
        keyword = instance.text.strip()

        if not keyword or keyword in self.keywords:
            instance.text = ""
            instance.focus = True
            return

        self.keywords.append(keyword)
        self._rebuild_chips()

        instance.text = ""
        instance.focus = True

    def remove_keyword(self, keyword):
        """
        remove a keyword from the list

        :param self: object
        :param keyword: keyword string to remove
        """
        if keyword in self.keywords:
            self.keywords.remove(keyword)
            self._rebuild_chips()

    def _rebuild_chips(self):
        """
        rebuild the keyword chips

        :param self: object
        """
        self.chip_container.clear_widgets()

        for kw in self.keywords:
            # each chip
            chip_layout = MDBoxLayout(
                orientation="horizontal",
                size_hint=(None, None),
                height="32dp",
                padding=("8dp", "4dp", "4dp", "4dp"),
                spacing=4,
                md_bg_color=(0.7, 0.7, 0.7, 0.3)
            )
            chip_layout.adaptive_width = True
            chip_layout.radius = [16, 16, 16, 16]  

            # --- Keyword label ---
            label = MDLabel(
                text=kw,
                size_hint=(None, None),
                height="32dp",
                valign="center",
                padding=("8dp", "4dp", "4dp", "4dp")
            )
            label.adaptive_width = True

            # Close button
            close_btn = MDIconButton(
                icon="close",
                size_hint=(None, None),
                size=("10dp", "10dp"),
                pos_hint={"center_y": 0.5},
                on_release=lambda x, k=kw: self.remove_keyword(k)
            )

            chip_layout.add_widget(label)
            chip_layout.add_widget(close_btn)
            
            self.chip_container.add_widget(chip_layout)


    def open_menu(self, instance):
        """
        open location dropdown menu

        :param self: object
        :param instance: widget instance
        """
        self.menu.open()

    def set_location(self, location):
        """
        set selected location from dropdown

        :param self: object
        :param location: location string
        """
        self.selected_location = location
        self.location_btn.text = location
        self.menu.dismiss()


    def find_jobs(self, instance):
        """
        find jobs based on the form and navigate to result screen

        :param self: object
        :param instance: widget instance
        """
        if not self.keywords or self.selected_location == "Select Country":
            return

        result_screen = self.manager.get_screen("result")
        result_screen.fetch_and_display(
            self.keywords,
            self.selected_location
        )
        self.manager.current = "result"
