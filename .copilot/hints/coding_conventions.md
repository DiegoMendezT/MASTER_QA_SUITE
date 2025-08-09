## Coding Conventions

### Naming
- **Files**: `snake_case.py` (e.g., `test_login_flow.py`, `home_page.py`).
- **Classes**: `PascalCase` (e.g., `LoginPage`, `TestSmokeSuite`).
- **Functions/Methods**: `snake_case()` (e.g., `def login_with_credentials():`).
- **Variables**: `snake_case` (e.g., `user_name`, `login_button`).
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `BASE_URL`, `DEFAULT_TIMEOUT`).
- **Pytest Markers**: `lowercase` (e.g., `@pytest.mark.smoke`).

### Docstrings
- Use Google-style docstrings for all public modules, classes, and functions.
- Include a one-line summary, followed by a more detailed description, `Args:`, and `Returns:`.
- **Test Files**: The docstring of a test file should describe the user story or feature being tested.
- **Test Functions**: The docstring of a test function should describe the specific scenario it covers in a BDD-style (`Given-When-Then`).

### Commits
- Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.
- **Format**: `<type>(<scope>): <subject>`
- **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`.
- **Scope**: The part of the codebase affected (e.g., `ui`, `tests`, `ci`, `docs`).
- **Example**: `feat(ui): add preset selector to streamlit runner`

## Test Design Philosophy

- **AAA Pattern**: Structure tests using Arrange, Act, Assert.
- **DRY (Don't Repeat Yourself)**: Use fixtures for setup/teardown and helper functions for common actions.
- **Single Responsibility**: Each test should verify one specific piece of functionality.
- **Independence**: Tests must be able to run in any order and not depend on the state of other tests.
- **Readability**: Write tests that are easy to understand. Use clear variable names and comments where necessary. The test function name and docstring should clearly state the test's purpose.
- **Markers**: Use pytest markers (`@pytest.mark.<name>`) to categorize tests (e.g., `smoke`, `regression`, `ui`, `api`). This allows for flexible test execution.
