import yaml
import os

class InnerCouncil:
    """
    The InnerCouncil provides decision-making logic for prioritizing development tasks.
    It reads a backlog of tasks and scores them based on predefined rules.
    """

    def __init__(self, backlog_file='config/backlog.yml', rules_file='.copilot/hints/innercouncil_rules.md'):
        self.backlog = self._load_yaml(backlog_file)
        self.rules = self._parse_rules(rules_file)

    def _load_yaml(self, file_path):
        """Loads a YAML file."""
        if not os.path.exists(file_path):
            print(f"Warning: Backlog file not found at {file_path}. Creating a default backlog.")
            default_backlog = {
                'tasks': [
                    {'name': 'Implement live test logs in Streamlit UI', 'roi': 8, 'complexity': 6, 'learning': 4},
                    {'name': 'Add Playwright for parallel headless execution', 'roi': 9, 'complexity': 8, 'learning': 5},
                    {'name': 'Create a new test suite for user profile page', 'roi': 6, 'complexity': 3, 'learning': 2},
                ]
            }
            with open(file_path, 'w') as f:
                yaml.dump(default_backlog, f)
            return default_backlog
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)

    def _parse_rules(self, file_path):
        """A simple parser for the rules markdown file to extract weights."""
        # This is a simplistic parser. A more robust solution might be needed for complex rules.
        rules = {
            'Weight_ROI': 0.5,
            'Weight_Complexity': -0.2,
            'Weight_Learning': 0.3
        }
        # In a real scenario, we would parse the markdown file to get these values.
        return rules

    def decide_next_task(self):
        """
        Scores all tasks in the backlog and returns the one with the highest score.
        """
        if not self.backlog or 'tasks' not in self.backlog:
            return {"error": "No tasks found in backlog."}, 0

        highest_score = -1
        best_task = None

        for task in self.backlog['tasks']:
            score = (
                task.get('roi', 0) * self.rules['Weight_ROI'] +
                task.get('complexity', 0) * self.rules['Weight_Complexity'] +
                task.get('learning', 0) * self.rules['Weight_Learning']
            )
            if score > highest_score:
                highest_score = score
                best_task = task

        return best_task, highest_score

if __name__ == '__main__':
    council = InnerCouncil()
    next_task, score = council.decide_next_task()
    if 'error' in next_task:
        print(next_task['error'])
    else:
        print("InnerCouncil has decided. The next priority task is:")
        print(f"  Task: {next_task['name']}")
        print(f"  Score: {score:.2f}")
        print(f"  (ROI: {next_task['roi']}, Complexity: {next_task['complexity']}, Learning: {next_task['learning']})")
