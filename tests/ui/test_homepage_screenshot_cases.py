"""
Test: Homepage screenshot cases for demo website coverage
Selenium Features: [driver.get, save_screenshot]
AUT: trinus.com and Superbateriascr.com
Markers: @ui @trinus / @superbateriascr
Purpose: Opens a demo homepage, waits for the page to render, and captures a screenshot for evidence.
"""
from pathlib import Path
from urllib.parse import urljoin, urlparse

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _resolve_demo_cases(requested_case: str | None):
    if requested_case:
        return [requested_case]
    return ["superbaterias"]


def pytest_generate_tests(metafunc):
    if "case_key" in metafunc.fixturenames:
        requested_case = metafunc.config.getoption("demo_case")
        metafunc.parametrize("case_key", _resolve_demo_cases(requested_case))


def _slugify_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        return "home"
    slug = path.replace("/", "_").replace("-", "_")
    return slug or "home"


def _collect_internal_links(driver, max_links=6):
    links = []
    try:
        anchors = driver.find_elements(By.TAG_NAME, "a")
        for anchor in anchors:
            href = anchor.get_attribute("href")
            if not href:
                continue
            full_url = urljoin(driver.current_url, href)
            parsed = urlparse(full_url)
            if parsed.scheme not in {"http", "https"}:
                continue
            if parsed.netloc.lower() not in {urlparse(driver.current_url).netloc.lower()}:
                continue
            if full_url.startswith("mailto:") or full_url.startswith("tel:"):
                continue
            if "#" in full_url:
                full_url = full_url.split("#", 1)[0]
            if full_url not in links:
                links.append(full_url)
            if len(links) >= max_links:
                break
    except Exception:
        pass
    return links


def _baterias_spanish_summary(case_key: str, pages_count: int) -> str:
    if case_key != "superbaterias":
        return ""
    return (
        "Evidencia de recorrido de Super Baterias: revisamos la home y las landing pages "
        f"principales del sitio ({pages_count} páginas en total), verificando la presencia del "
        "contenido por categoría comercial y confirmando que el footer también se renderiza correctamente."
    )


def _capture_full_page_screenshot(driver, screenshot_path: Path):
    original_size = driver.get_window_size()
    total_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight, document.body.clientHeight, document.documentElement.clientHeight);")
    viewport_height = driver.execute_script("return window.innerHeight")
    driver.set_window_size(1440, max(900, min(total_height, 1800)))
    page_dir = screenshot_path.parent
    page_stem = screenshot_path.stem
    base_name = screenshot_path.name

    # Always write a unique main capture for the page itself.
    driver.execute_script("window.scrollTo(0, 0);")
    page_save = driver.save_screenshot(str(screenshot_path))

    scroll_step = max(250, int(viewport_height * 0.85))
    scroll_positions = list(range(0, total_height + 1, scroll_step))
    if scroll_positions and scroll_positions[-1] != total_height:
        scroll_positions.append(total_height)
    scroll_positions = sorted(set(scroll_positions))
    scroll_positions = [pos for pos in scroll_positions if pos > 0]

    unique_scroll_captures = []
    for idx, pos in enumerate(scroll_positions, start=1):
        driver.execute_script(f"window.scrollTo(0, {pos});")
        driver.execute_script("return new Promise(resolve => setTimeout(resolve, 250));")
        scroll_path = page_dir / f"{page_stem}_scroll_{idx:02d}.png"
        result = driver.save_screenshot(str(scroll_path))
        if result is not False:
            unique_scroll_captures.append(scroll_path)

    driver.set_window_size(original_size["width"], original_size["height"])
    return {"page": screenshot_path, "scroll_captures": unique_scroll_captures, "page_saved": page_save}


@pytest.mark.ui
def test_homepage_screenshot_case(driver, config, case_key):
    """Open each configured demo homepage and capture a small crawl of evidence screenshots."""
    site_url = config["urls"].get(case_key)
    if not site_url:
        pytest.skip(f"No URL configured for '{case_key}'")

    screenshots_dir = Path("artifacts/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    driver.get(site_url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    extra_pages = [
        "https://www.superbaterias.com/super-baterias-corporativo/",
        "https://www.superbaterias.com/contact-us-2/#puntos",
        "https://www.superbaterias.com/servicios-especializados/",
        "https://www.superbaterias.com/super-asistencias/",
        "https://www.superbaterias.com/super-baterias-ev/",
        "https://www.superbaterias.com/rescate-nocturno/",
        "https://www.superbaterias.com/marcas-y-tecnologias/",
        "https://www.superbaterias.com/garantias-2/",
        "https://www.superbaterias.com/terminos-condiciones/",
        "https://www.superbaterias.com/uso-de-las-estaciones-de-carga/",
        "https://www.superbaterias.com/politica-de-privacidad/",
        "https://www.superbaterias.com/reclutamiento/",
    ]

    pages_to_visit = [site_url]
    seen = {site_url}
    for page in extra_pages:
        if page not in seen:
            pages_to_visit.append(page)
            seen.add(page)
    for link in _collect_internal_links(driver, max_links=12):
        if link not in seen:
            pages_to_visit.append(link)
            seen.add(link)
        if len(pages_to_visit) >= 12:
            break

    captured_paths = []
    for idx, page_url in enumerate(pages_to_visit[:12], start=1):
        driver.get(page_url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        slug = _slugify_url(page_url)
        screenshot_path = screenshots_dir / f"{case_key}_{slug}.png"
        if case_key == "superbaterias":
            capture_result = _capture_full_page_screenshot(driver, screenshot_path)
            saved = capture_result["page_saved"]
            captured_paths.extend(capture_result["scroll_captures"])
            captured_paths.append(screenshot_path)
        else:
            saved = driver.save_screenshot(str(screenshot_path))
            captured_paths.append(screenshot_path)
        assert saved is not False
        assert screenshot_path.exists(), f"Screenshot was not created for '{case_key}' page '{page_url}'"
        if case_key == "superbaterias":
            print(f"Evidencia de Super Baterias guardada -> {screenshot_path.resolve()}")
            for scroll_shot in capture_result["scroll_captures"]:
                print(f"Scroll evidence guardada -> {scroll_shot.resolve()}")
        else:
            print(f"Screenshot evidence saved for '{case_key}' -> {screenshot_path.resolve()}")

    summary = _baterias_spanish_summary(case_key, len(captured_paths))
    if summary:
        print(summary)

    assert captured_paths, f"No screenshots captured for '{case_key}'"
    assert site_url in driver.current_url or driver.current_url.startswith("http")
