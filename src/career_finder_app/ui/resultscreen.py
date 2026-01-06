from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.chip import MDChip
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog

from kivy.metrics import dp
from career_finder_app.jobspymodule import get_jobs


class ResultScreen(MDScreen):
    def __init__(self, **kwargs):
        """
        initialize result screen and layout of the screen

        :param self: object
        :param kwargs: additional arguments
        """
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
        """
        fetch and display job results

        :param self: object
        :param keywords: list of keywords strings
        :param location: location string
        """
        # Show loading
        self.scroll.clear_widgets()
        self.scroll.add_widget(self.loading_label)
        
        # Fetch data (in real app, do this in a thread)
        try:
            # Call your function
            self.df = get_jobs(location=location, keywords=", ".join(keywords))
            
            if self.df.empty:
                self.show_no_results()
                return
            
            self.display_table()

        except Exception as e:
            self.show_error(str(e))

    def display_table(self):
        """
        display job results in scrollview table

        :param self: object
        """
        self.scroll.clear_widgets()
        
        # table container
        table_container = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=10,
            padding=10
        )
        
        # rows
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
                    text=f"[b]Job Title:[/b] {row.get('title', 'N/A')}",
                    markup=True,
                    size_hint_y=None,
                    height="30dp"
                )
            )
            
            # Buttons container
            button_container = MDBoxLayout(
                orientation="horizontal",
                adaptive_height=True,
                spacing=10,
                size_hint_y=None,
                height="40dp"
            )
            
            # Description button
            if 'description' in row and row['description']:
                desc_btn = MDFlatButton(
                    text="View Description",
                    on_release=lambda x, desc=row['description']: self.show_description(desc)
                )
                button_container.add_widget(desc_btn)
            
            # Cover Letter button
            cover_letter_btn = MDRaisedButton(
                text="Generate Cover Letter",
                on_release=lambda x, job_row=row: self.go_to_cover_letter(job_row)
            )
            button_container.add_widget(cover_letter_btn)
            
            row_layout.add_widget(button_container)
            
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

    def go_to_cover_letter(self, job_data):
        """
        navigate to cover letter screen with job data

        :param self: object
        :param job_data: job data dictionary
        """
        cover_letter_screen = self.manager.get_screen("cover_letter")
        cover_letter_screen.set_job_data(job_data)
        self.manager.current = "cover_letter"

    def show_description(self, description):
        """
        show job description dialog
        
        :param self: object
        :param description: description string
        """
        if self.dialog:
            self.dialog.dismiss()
        
        if not description:
            description = "No description available"
        
  
        desc_label = MDLabel(
            text=str(description),
            size_hint_y=None,
            markup=False,
            padding=(10, 10)
        )
        desc_label.text_size = (dp(400), None)
        desc_label.bind(
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
  
        content = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(400),  
            padding=0
        )
        
        scroll = MDScrollView(
            do_scroll_x=False,
            size_hint=(1, 1)
        )
        scroll.add_widget(desc_label)
        content.add_widget(scroll)
        
        close_button = MDFlatButton(
            text="CLOSE",
            on_release=lambda x: self.dialog.dismiss()
        )
        
        self.dialog = MDDialog(
            title="Job Description",
            type="custom",
            content_cls=content,
            buttons=[close_button]
        )
        self.dialog.open()

    def show_no_results(self):
        """
        show no results found message
        
        :param self: object
        """
        self.scroll.clear_widgets()
        self.scroll.add_widget(
            MDLabel(
                text="No jobs found",
                halign="center"
            )
        )

    def show_error(self, error_msg):
        """
        show error message

        :param self: object
        :param error_msg: error message string
        """
        self.scroll.clear_widgets()
        self.scroll.add_widget(
            MDLabel(
                text=f"Error: {error_msg}",
                halign="center"
            )
        )

    def go_back(self, instance):
        """
        Docstring for go_back
        
        :param self: object
        :param instance: widget instance
        """
        self.manager.current = "form"


