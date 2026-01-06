import getpass
import platform
from datetime import datetime
from pathlib import Path

def write_test_summary(metadata: dict, results: dict, run_dir: Path):
    """
    Write an ALM Octane/Jira-style summary block to result_summary.txt in the run directory.
    metadata: dict of test metadata fields (name, component, etc.)
    results: dict with keys 'visited', 'start_time', 'duration', 'error_message', etc.
    run_dir: Path to the run directory
    """
    total_pages = len(results.get('visited', []))
    passed = sum(1 for v in results.get('visited', []) if v.get('status', '').startswith('Passed'))
    failed = sum(1 for v in results.get('visited', []) if v.get('status', '').startswith('Failed'))
    error_message = results.get('error_message') or next((v.get('status') for v in results.get('visited', []) if v.get('status','').startswith('Failed')), None)
    error_type = "None" if not error_message else "Test Failure"
    error_details = error_message if error_message else "None"
    start_time = results.get('start_time')
    duration_str = results.get('duration')
    # QA-style template
    bug_found = failed > 0 or error_message
    summary_lines = [
        "# QA Test Case Report\n",
        "## Details",
        "| Field         | Value |",
        "|---------------|-------|",
        f"| Test Name     | {metadata.get('test_name', 'N/A')} |",
        f"| Component     | {metadata.get('component', 'N/A')} |",
        f"| Duration      | {duration_str} |",
        f"| Start Time    | {start_time} |",
        "",
        "## Additional Info",
        "| Field         | Value |",
        "|---------------|-------|",
        f"| Test Level    | {metadata.get('test_level', 'N/A')} |",
        f"| Test Type     | {metadata.get('test_type', 'N/A')} |",
        f"| Build         | {metadata.get('build', 'N/A')} |",
        f"| Release       | {metadata.get('release', 'N/A')} |",
        f"| Milestone     | {metadata.get('milestone', 'N/A')} |",
        f"| Environment   | {metadata.get('environment', 'N/A')} |",
        f"| Pipeline Run  | {metadata.get('pipeline_run', 'N/A')} |",
        f"| Run By        | {metadata.get('run_by', getpass.getuser())} |",
        "",
        "## Purpose",
        f"- {metadata.get('purpose', '')}",
        "",
        "## Expected Results",
        "- Every main navigation and submenu page is visited and loaded successfully.",
        "- The test scrolls through each page, ensuring the footer and all dynamic content are captured.",
        "- Unique screenshots are taken for every scroll position, with no duplicates.",
        "- The evidence block contains a detailed record for each page, including name, URL, status, and screenshot path.",
        "- The summary reports the total number of pages visited, passed, and failed, with zero failures expected for a healthy site.",
        "",
        "## Actual Results",
        f"- This run visited {total_pages} pages: {passed} passed, {failed} failed.",
    ]
    if bug_found:
        summary_lines += [
            "",
            "## Bug Report",
            f"- **Error Message:** {error_message if error_message else 'N/A'}",
            f"- **Error Type:** {error_type}",
            f"- **Error Details:** {error_details}",
            "- **Status:** FAILED (Bug found, see error info above)",
        ]
    else:
        summary_lines += [
            "- Actual results match expected results. No bugs found.",
            "- **Status:** PASSED"
        ]
    summary_lines += [
        "",
        metadata.get('additional_info', '')
    ]
    # Add margin by wrapping in a Markdown blockquote
    summary_text = '\n'.join(summary_lines)
    summary_text = '>\n' + summary_text.replace('\n', '\n> ')
    (Path(run_dir) / 'result_summary.txt').write_text(summary_text, encoding='utf-8')
