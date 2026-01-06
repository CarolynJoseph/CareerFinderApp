from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from threading import Thread
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard




class CoverLetterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.job_data = None

        # Main layout
        main_layout = MDBoxLayout(orientation="vertical", padding=20, spacing=15)

        # Job info header
        self.job_info_label = MDLabel(
            text="Job Information", size_hint_y=None, height="40dp", font_style="H6"
        )
        main_layout.add_widget(self.job_info_label)

        # Two-column layout for input and output
        content_layout = MDBoxLayout(
            orientation="horizontal", spacing=20, size_hint_y=0.8
        )

        # Left side - Input section
        left_section = MDBoxLayout(orientation="vertical", spacing=10, size_hint_x=0.45)

        left_section.add_widget(
            MDLabel(
                text="Your Information & Notes:",
                size_hint_y=None,
                height="30dp",
                font_style="Subtitle1",
            )
        )
        
        input_container = MDBoxLayout(
            orientation="vertical",
            md_bg_color=(1, 1, 1, 1),  # White background 
            padding=20,
            radius=[5, 5, 5, 5],
        )

        input_scroll = MDScrollView(do_scroll_x=False)

        # self.input_field = MDTextField(
        #     multiline=True,
        #     hint_text="Start typing your background, skills, and experience...",
        #     mode="fill",
        #     size_hint_y=None,
        #     font_size="14sp",
        #     fill_color=(1, 1, 1, 0),  
        #     line_color_normal=(1, 1, 1, 0), 
        #     line_color_focus=(1, 1, 1, 0),  
        #     hint_text_color=(0.5, 0.5, 0.5, 1), 
        # )

        self.input_field = MDTextField(
            multiline=True,
            hint_text="Start typing your background, skills, and experience...",
            size_hint_y=None,
            font_size="14sp",
            mode="rectangle",  # Rectangle mode looks cleaner
            line_color_normal=(0.9, 0.9, 0.9, 1),  # Very light gray
            line_color_focus=(0.9, 0.9, 0.9, 1)  # Keep it light when focused
        )
        
        self.input_field.bind(minimum_height=self.input_field.setter("height"))

        self.input_field.height = dp(400)

        input_scroll.add_widget(self.input_field)
        input_container.add_widget(input_scroll)
        left_section.add_widget(input_container)

        content_layout.add_widget(left_section)

        # Center - Generate button
        center_section = MDBoxLayout(
            orientation="vertical", size_hint_x=0.1, padding=(0, 100, 0, 0)
        )

        self.generate_btn = MDRaisedButton(
            text="Generate",
            size_hint=(1, None),
            height="48dp",
            on_release=self.generate_cover_letter,
        )
        center_section.add_widget(self.generate_btn)

        content_layout.add_widget(center_section)

        # Right side - Output section
        right_section = MDBoxLayout(
            orientation="vertical", spacing=10, size_hint_x=0.45
        )

        right_section.add_widget(
            MDLabel(
                text="Generated Cover Letter:",
                size_hint_y=None,
                height="30dp",
                font_style="Subtitle1",
            )
        )

        # Output text field (scrollable, READ-ONLY)
        output_scroll = MDScrollView()
        self.output_field = MDLabel(
            text="", size_hint_y=None, markup=False, padding=(10, 10)
        )
        self.output_field.bind(
            texture_size=lambda instance, value: setattr(instance, "height", value[1])
        )
        output_scroll.add_widget(self.output_field)
        right_section.add_widget(output_scroll)
        content_layout.add_widget(right_section)

        main_layout.add_widget(content_layout)

        # Bottom buttons
        button_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height="50dp",
            padding=(0, 10, 0, 0),
        )

        back_btn = MDFlatButton(text="Back to Job listings", on_release=self.go_back)
        button_layout.add_widget(back_btn)

        button_layout.add_widget(MDLabel())

        submit_btn = MDRaisedButton(
            text="Copy to Clipboard", on_release=self.copy_to_clipboard
        )
        button_layout.add_widget(submit_btn)

        main_layout.add_widget(button_layout)

        self.add_widget(main_layout)

    def set_job_data(self, job_data):
        """
        set job data for application screen

        :param self: object
        :param job_data: job data dictionary
        """

        self.job_data = job_data

        # Update job info display
        company = job_data.get("company", "N/A")
        title = job_data.get("title", "N/A")
        location = job_data.get("location", "N/A")

        self.job_info_label.text = f"Applying to: {title} at {company} ({location})"

        # Clear previous content
        self.input_field.text = ""
        self.output_field.text = ""  # Blank initially

    def generate_cover_letter(self, instance):
        """
        generate cover letter based on job data and user input
        
        :param self: object
        :param instance: widget instance
        """
        if not self.input_field.text.strip():
            self.output_field.text = "Please enter your information first."
            return

        # Disable button during generation
        self.generate_btn.disabled = True
        self.generate_btn.text = "Generating..."
        self.output_field.text = "Generating your cover letter..."

        # Run in thread to avoid blocking UI
        thread = Thread(target=self._generate_in_background)
        thread.start()

    def copy_to_clipboard(self, instance):
        """
        copy to clipboard
        
        :param self: object
        :param instance: widget instance
        """
        if not self.output_field.text:
            return

        Clipboard.copy(self.output_field.text)

        # Could show a snackbar or dialog here
        print("Cover letter copied to clipboard!")

    def _generate_in_background(self):
        """
        background thread to generate cover letter

        :param self: object
        """
        try:
            cover_letter = self._call_ai_function(
                job_title=self.job_data.get("jobtitle", ""),
                company=self.job_data.get("company", ""),
                job_description=self.job_data.get("description", ""),
                user_info=self.input_field.text,
            )

            Clock.schedule_once(lambda dt: self._update_output(cover_letter), 0)

        except Exception as e:

            Clock.schedule_once(
                lambda dt: self._update_output(
                    f"Error generating cover letter: {str(e)}"
                ),
                0,
            )

    def _call_ai_function(self, job_title, company, job_description, user_info):
        """
        placeholder AI function call
        
        :param self: object
        :param job_title: title string
        :param company: company string
        :param job_description: Description string
        :param user_info: user input string
        :return: generated cover letter string
        """
        # todo: implement actual AI calls
        # Placeholder implementation
        return f"""Dear Hiring Manager at {company},

        I am writing to express my strong interest in the {job_title} position.

        {user_info}

        I  and look forward to discussing how my skills align with your needs.

        Sincerely,
        [Your Name]"""

    def _update_output(self, text):
        """
        update output field with generated text
        
        :param self: object
        :param text: generated cover letter string
        """
        self.output_field.text = text
        self.generate_btn.disabled = False
        self.generate_btn.text = "Generate"

    def go_back(self, instance):
        """
        navigate back to results screen
        
        :param self: object
        :param instance: widget instance
        """
        self.manager.current = "result"
