## Task Prioritizer Decision Rules

The `TaskPrioritizer` is a conceptual layer of this project, representing the logic used to prioritize development tasks. When using the "Let Task Prioritizer Decide" feature in the Streamlit UI, the following rules are applied to the backlog of features and tests.

### Priority Scoring
Each task is assigned a score based on the following formula:

`PriorityScore = (ROI * Weight_ROI) + (Complexity * Weight_Complexity) + (LearningValue * Weight_Learning)`

### Factors

1.  **ROI (Return on Investment)**
    - **Scale**: 1-10
    - **Description**: How much value does this task add?
        - **High (8-10)**: Critical path functionality, unblocking other work, high-risk areas.
        - **Medium (4-7)**: Important but not critical features, significant refactors.
        - **Low (1-3)**: Minor UI tweaks, "nice-to-have" features, low-impact bugs.

2.  **Complexity**
    - **Scale**: 1-10
    - **Description**: How difficult is this task to implement?
        - **Low (1-3)**: Simple, well-understood, can be done quickly.
        - **Medium (4-7)**: Requires some research or design, involves multiple components.
        - **High (8-10)**: Complex, requires significant research, high risk of unforeseen issues.

3.  **Learning Value**
    - **Scale**: 1-5
    - **Description**: How much does implementing this task contribute to the growth of the framework or the developer?
        - **High (4-5)**: Involves new technologies, patterns, or a challenging problem.
        - **Medium (2-3)**: Reinforces existing knowledge, minor new concepts.
        - **Low (1)**: Repetitive or trivial task.

### Weighting
The weights determine the strategy for development.

- **Balanced (Default)**:
    - `Weight_ROI`: 0.5
    - `Weight_Complexity`: -0.2 (we prefer less complex tasks, hence negative)
    - `Weight_Learning`: 0.3

- **Feature-Driven**:
    - `Weight_ROI`: 0.7
    - `Weight_Complexity`: -0.1
    - `Weight_Learning`: 0.2

- **Innovation-Driven**:
    - `Weight_ROI`: 0.3
    - `Weight_Complexity`: -0.1
    - `Weight_Learning`: 0.6

The task with the highest `PriorityScore` is selected as the next item to work on. This logic will be implemented in `tools/task_prioritizer.py` and integrated with the Streamlit UI.

### Guardrails
To ensure the integrity and consistency of the project, adhere to the following guardrails:

- Never rename `tools/task_prioritizer.py` or `config/prioritizer_rules.yml`.
- Keep `tools/innercouncil.py` as a shim that re-exports from `tools/task_prioritizer`.
- When you see legacy imports to `tools.innercouncil`, prefer fixing them to `tools.task_prioritizer` gradually.
- Always run: `python -m tools.consistency_check` before committing structural changes.
