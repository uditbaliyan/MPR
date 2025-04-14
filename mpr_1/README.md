
# Flask App

This Flask app provides routes for pose analysis and recommendations, using templates for HTML rendering and a modular structure for organization.

## Project Structure

```
├── config.py                  # Configuration settings
├── __init__.py                # App initialization
├── models/                    # Models for data handling
├── routes/                    # Route definitions
├── templates/                 # HTML templates
└── utils/                     # Utility functions for camera and pose detection
```

## Getting Started

### Prerequisites

- Python 3.11 or later
- Virtual environment (recommended)
- Flask and other libraries in `requirements.txt`

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/uditbaliyan/MPR.git
   cd MPR
   ```

2. **Set up a virtual environment and install dependencies:**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure `config.py` as needed.**

### Running the Application

To start the Flask application, run the following command:

```bash
python run.py

```

Visit `http://127.0.0.1:5000` to access the app.

## Usage

- **Homepage**: Overview and links to features (`index.html`)
- **Pose Analysis**: Analyze poses via video input (`pose_analysis.html`)
- **Recommendations**: View generated recommendations (`recommendations.html`)


## License

MIT License


This version focuses on setup, structure, and usage without additional explanation. Let me know if you'd like any further refinements!
