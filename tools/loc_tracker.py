# tools/loc_tracker.py
"""
Tracks lines of code (LOC) and churn for the MASTER_QA_SUITE project.

This tool provides metrics on code volume and volatility, which are key
indicators of development activity and potential areas of instability.

Functions:
- count_loc(directory): Counts the total lines of code in a given directory.
- track_churn(repo_path, since_date): Tracks code churn (added/deleted lines)
  since a specific date.
- main(): Main function to run the tracker and print a report.
"""
import argparse
import os
import subprocess
from datetime import datetime, timedelta

# --- Configuration ---
# Directories/files to include in LOC count
INCLUDED_EXTENSIONS = ['.py', '.yml', '.md', '.robot']
# Directories to exclude from LOC count
EXCLUDED_DIRS = ['.git', '.vscode', '__pycache__', 'docs', 'reports', 'allure-report', 'allure-results', 'downloads']

def count_loc(directory):
    """
    Recursively counts the lines of code in a directory, filtering by
    included extensions and excluding specified directories.

    Args:
        directory (str): The path to the directory to analyze.

    Returns:
        int: The total count of lines of code.
    """
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        for file in files:
            if any(file.endswith(ext) for ext in INCLUDED_EXTENSIONS):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        total_lines += len(f.readlines())
                except Exception as e:
                    print(f"Could not read file {filepath}: {e}")
    return total_lines

def track_churn(repo_path, since_date=None):
    """
    Tracks code churn (lines added, lines deleted) in a Git repository.

    Args:
        repo_path (str): The path to the Git repository.
        since_date (str, optional): The start date in 'YYYY-MM-DD' format.
                                    Defaults to 30 days ago.

    Returns:
        tuple: A tuple containing (lines_added, lines_deleted).
    """
    if since_date is None:
        # Default to the last 30 days
        since_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    try:
        # Use git log to get the number of added and deleted lines
        cmd = [
            'git', 'log', '--since', since_date, '--numstat',
            '--pretty=format:', '--', '*.py', '*.yml', '*.md', '*.robot'
        ]
        
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, check=True)
        
        lines_added = 0
        lines_deleted = 0
        
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t')
                if len(parts) == 3:
                    # numstat format is: added_lines <tab> deleted_lines <tab> filename
                    added, deleted, _ = parts
                    if added.isdigit():
                        lines_added += int(added)
                    if deleted.isdigit():
                        lines_deleted += int(deleted)
                        
        return lines_added, lines_deleted
        
    except subprocess.CalledProcessError as e:
        print(f"Error running git log: {e}")
        print(f"Stderr: {e.stderr}")
        return 0, 0
    except FileNotFoundError:
        print("Git command not found. Is Git installed and in your PATH?")
        return 0, 0

def main():
    """
    Main function to run the LOC and churn tracker and print a report.
    """
    parser = argparse.ArgumentParser(description="Code and Churn Tracker for MASTER_QA_SUITE")
    parser.add_argument(
        "--since",
        type=str,
        help="Start date for churn analysis (YYYY-MM-DD). Defaults to 30 days ago."
    )
    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    print("--- MASTER QA SUITE: Code Metrics ---")
    
    # 1. Current Lines of Code
    print("\nCalculating current Lines of Code (LOC)...")
    total_loc = count_loc(project_root)
    print(f"✅ Total Lines of Code: {total_loc}")
    
    # 2. Code Churn
    print(f"\nAnalyzing code churn since {args.since or '30 days ago'}...")
    added, deleted = track_churn(project_root, args.since)
    total_churn = added + deleted
    print(f"✅ Lines Added: {added}")
    print(f"✅ Lines Deleted: {deleted}")
    print(f"✅ Total Churn: {total_churn}")
    
    print("\n--- Analysis Complete ---")

if __name__ == "__main__":
    main()
