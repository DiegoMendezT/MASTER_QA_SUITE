Trinus demo (scaffold)
======================

Quick notes to run the Trinus demo locally and CI.

Run locally
-----------

1. Activate or use the project venv Python:

   .venv\Scripts\python.exe -m pip install -r requirements/core-tests.txt -r requirements/ui.txt

2. Start the Streamlit app (in the venv):

   .venv\Scripts\python.exe -m streamlit run ui_streamlit\Master_QA_Suite_-_About.py

3. Run the Selenium smoke test (opens headless Chrome and clicks the demo button):

   .venv\Scripts\python.exe -m pytest tests/selenium -q

Notes
-----
- The test starts Streamlit itself and then drives it via Selenium (chromedriver is auto-installed).
- Keep credentials out of `config/clients/trinus.yaml`; use environment variables or CI secrets.
