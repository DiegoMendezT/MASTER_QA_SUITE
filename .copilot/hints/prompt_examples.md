## Generating a New Test Suite

**Prompt:**
"Create a new test suite for the login page. It should include tests for a successful login, a login with an invalid password, and a login with an empty username. The tests should be marked as `smoke` and `regression`. The user story is 'As a user, I want to be able to log in to the application so that I can access my account.'"

**Expected Output:**
A new file `tests/test_login_flow.py` with:
- A file-level docstring describing the user story.
- Three test functions, one for each scenario.
- Each test function has a BDD-style docstring.
- Appropriate `@pytest.mark.smoke` and `@pytest.mark.regression` markers.
- Correct use of the `LoginPage` page object and fixtures.

---

## Refactoring a Page Object

**Prompt:**
"The locators on the `HomePage` are using IDs, but the front-end team is switching to `data-testid` attributes. Refactor the `HomePage` page object in `pages/home_page.py` to use the new `data-testid` locators. The new attributes are `data-testid='home-title'` and `data-testid='user-profile-button'`."

**Expected Output:**
The `pages/home_page.py` file is updated:
- The locator tuples are changed from `(By.ID, ...)` to `(By.CSS_SELECTOR, '[data-testid="..."]')`.
- The rest of the class structure remains unchanged.

---

## Adding a Control to the Streamlit UI

**Prompt:**
"Add a new control to the Streamlit UI in `ui/controls.py`. It should be a multi-select box that allows the user to select which environment to run the tests against (e.g., 'staging', 'production'). The selected environment should be passed as an environment variable `TARGET_ENV` to the pytest command."

**Expected Output:**
The `ui/controls.py` file is updated:
- A new `st.multiselect` widget is added.
- The selected value is captured.
- The `subprocess.run` command is updated to include `env={'TARGET_ENV': selected_env, **os.environ}`.
