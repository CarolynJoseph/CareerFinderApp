
# CareerFinderApp

CareerFinderApp is an AI-powered application designed to help users discover suitable career paths and generate tailored cover letters based on their skills and preferences. The app integrates with Hugging Face models to provide intelligent job recommendations and personalized content.

## Features
- AI-driven job recommendations (todo)
- Cover letter generation using advanced language models
- User-friendly interface for inputting skills and preferences
- Modular codebase for easy extension and maintenance

## Project Structure
```
CareerFinderApp/
├── src/
│   └── career_finder_app/
│       ├── mainapp.py          # Main application entry point
│       ├── aiintegration/
│       │   └── huggingfaceinference.py  # Hugging Face API integration
│       ├── jobspymodule/      # Job-related modules
│       └── ui/                # User interface modules
│           ├── coverletterscreen.py
│           ├── formscreen.py
│           └── resultscreen.py
├── pyproject.toml              # Project dependencies and configuration
├── README.md                   # Project documentation
└── LICENSE                     # License information
```

## Installation
1. Clone the repository:
	```bash
	git clone <repository-url>
	cd CareerFinderApp
	```
2. Install dependencies:
    ```
	use pyproject.toml with poetry
	```

## Usage
Run the main application:
```bash
python src/career_finder_app/mainapp.py
```

## Configuration
- Create a .env file and add your huggingface token as follows
export HF_TOKEN="your_token_here"

## License
This project is licensed under the terms of the LICENSE file in this repository.
