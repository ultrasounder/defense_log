import os
from streamlit.testing.v1 import AppTest

def test_app_title_is_correct():
    """
    User opens the app and checks if the title matches the branding.
    """
    # 1. Robustly find app.py relative to this test file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(current_dir, "../app.py")

    # 2. THE FIX: Use the 'app_path' variable, NOT the string "app.py"
    at = AppTest.from_file(app_path).run()
    
    # 3. Assert
    assert at.title[0].value == "🛡️ DefenseLog: Supply Chain Risk Agent"

