import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[2] / "ui_streamlit" / "pages" / "1_Test_Runner_-_Online_Demos.py"
SPEC = importlib.util.spec_from_file_location("online_demo_runner", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

HOMECASE_PATH = Path(__file__).resolve().parent / "test_homepage_screenshot_cases.py"
HOMECASE_SPEC = importlib.util.spec_from_file_location("homepage_screenshot_cases", HOMECASE_PATH)
HOMEPAGE_CASES = importlib.util.module_from_spec(HOMECASE_SPEC)
HOMECASE_SPEC.loader.exec_module(HOMEPAGE_CASES)


def test_filter_current_evidence_ignores_stale_files(tmp_path):
    current = tmp_path / "superbaterias_home.png"
    stale = tmp_path / "superbaterias_footer.png"
    trinus = tmp_path / "trinus_home.png"

    current.write_bytes(b"new")
    stale.write_bytes(b"old")
    trinus.write_bytes(b"other")

    now = current.stat().st_mtime
    stale.touch()
    stale_stat = stale.stat()
    old_ts = stale_stat.st_mtime - 200
    import os
    os.utime(stale, (old_ts, old_ts))

    files = [str(current), str(stale), str(trinus)]
    filtered = MODULE.filter_current_evidence(files, run_start_time=now, selected_markers=["superbaterias"])

    assert str(current) in filtered
    assert str(stale) not in filtered
    assert str(trinus) not in filtered


def test_filter_current_evidence_keeps_only_selected_marker_scope(tmp_path):
    baterias = tmp_path / "superbaterias_home.png"
    ui = tmp_path / "ui_test_homepage_passed.png"
    trinus = tmp_path / "trinus_home.png"
    ui_baterias_mislabel = tmp_path / "ui_test_homepage_screenshot_case_superbaterias_passed.png"

    for item in [baterias, ui, trinus, ui_baterias_mislabel]:
        item.write_bytes(b"x")

    filtered = MODULE.filter_current_evidence(
        [str(baterias), str(ui), str(trinus), str(ui_baterias_mislabel)],
        run_start_time=None,
        selected_markers=["superbaterias"],
    )

    assert str(baterias) in filtered
    assert str(ui) not in filtered
    assert str(trinus) not in filtered
    assert str(ui_baterias_mislabel) not in filtered


def test_should_show_baterias_summary_only_for_baterias_selection():
    assert MODULE.should_show_baterias_summary(["superbaterias"]) is True
    assert MODULE.should_show_baterias_summary(["superbaterias", "ui"]) is True
    assert MODULE.should_show_baterias_summary(["bateriascostaricacr"]) is True
    assert MODULE.should_show_baterias_summary(["ui"]) is False
    assert MODULE.should_show_baterias_summary(["trinus"]) is False
    assert MODULE.should_show_baterias_summary(["all"]) is False


def test_capture_full_page_screenshot_creates_unique_scroll_shots(tmp_path):
    class FakeDriver:
        def __init__(self):
            self.scroll_positions = []
            self._after_page_capture = False

        def get_window_size(self):
            return {"width": 1440, "height": 900}

        def execute_script(self, script):
            if "Math.max" in script:
                return 3600
            if "innerHeight" in script:
                return 900
            if "window.scrollTo" in script:
                payload = script.replace("window.scrollTo(", "").replace(");", "").strip()
                parts = [part.strip() for part in payload.split(",")]
                if len(parts) >= 2:
                    try:
                        parsed = int(parts[1])
                        if self._after_page_capture and parsed > 0:
                            self.scroll_positions.append(parsed)
                    except ValueError:
                        pass
                return None
            return None

        def set_window_size(self, width, height):
            return None

        def save_screenshot(self, path):
            # First screenshot is the main page capture; scroll captures follow after this flag flips.
            if path.endswith(".png") and "_scroll_" not in str(path):
                self._after_page_capture = True
            Path(path).write_bytes(b"x")
            return True

    driver = FakeDriver()
    screenshot_base = tmp_path / "superbaterias_home.png"
    created = HOMEPAGE_CASES._capture_full_page_screenshot(driver, screenshot_base)

    scroll_shots = sorted(tmp_path.glob("superbaterias_home*_scroll_*.png"))
    assert 0 not in driver.scroll_positions
    assert len(created["scroll_captures"]) >= 2
    assert len(scroll_shots) >= 3


def test_default_demo_markers_prioritize_baterias_ui_api():
    available = ["all", "api", "superbaterias", "trinus", "ui"]
    assert MODULE.default_demo_markers(available) == ["superbaterias", "ui", "api"]


def test_homepage_default_case_scope_runs_baterias_only_without_explicit_demo_case():
    requested = None
    default_cases = HOMEPAGE_CASES._resolve_demo_cases(requested)
    assert default_cases == ["superbaterias"]

    explicit_cases = HOMEPAGE_CASES._resolve_demo_cases("trinus")
    assert explicit_cases == ["trinus"]


def test_collect_run_screenshots_finds_nested_active_evidence(tmp_path):
    active_run_dir = tmp_path / "20240101T000000Z"
    stale_run_dir = tmp_path / "20230101T000000Z"
    active_run_dir.mkdir()
    stale_run_dir.mkdir()

    active = active_run_dir / "superbaterias_home.png"
    stale = stale_run_dir / "superbaterias_old.png"
    active.write_bytes(b"new")
    stale.write_bytes(b"old")

    active_ts = active.stat().st_mtime
    old_ts = active_ts - 600
    import os
    os.utime(stale, (old_ts, old_ts))

    files = MODULE.collect_run_screenshots(
        str(tmp_path),
        run_start_time=active_ts,
        selected_markers=["superbaterias"],
    )

    assert str(active) in files
    assert str(stale) not in files
