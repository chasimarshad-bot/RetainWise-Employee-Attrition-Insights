"""Local Chromium checks of actual navigation, filters and responsive layouts."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/browser'
OUT.mkdir(parents=True, exist_ok=True)
PAGES = [('', 'RetainWise'), ('patterns', 'Workforce Patterns'), ('hypotheses', 'Hypothesis Lab'),
         ('governance', 'Fairness & Governance'), ('methodology', 'Methodology & Project Plan')]


def ready(page, title):
    page.get_by_role('heading', name=title, exact=True).wait_for(timeout=30000)
    page.get_by_text('RetainWise · Unit 3 capstone', exact=False).wait_for(state='attached', timeout=30000)
    page.wait_for_timeout(300)

if __name__ == '__main__':
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page()
        page.set_default_timeout(15000)
        for width, height in [(1440, 1000), (768, 1024), (390, 844)]:
            page.set_viewport_size({'width': width, 'height': height})
            for route, title in PAGES:
                response = page.goto('http://localhost:8501/' + route)
                ready(page, title)
                assert response.status == 200
                assert page.get_by_test_id('stException').count() == 0
                assert 'The keyword arguments have been deprecated' not in page.inner_text('body')
                overflow = page.evaluate('document.documentElement.scrollWidth > window.innerWidth')
                assert not overflow, (route, width)
                page.get_by_role('heading', name=title, exact=True).scroll_into_view_if_needed()
                page.screenshot(path=str(OUT / f'{route or "overview"}-{width}.png'), full_page=True)
                if route != 'methodology':
                    chart = page.get_by_test_id('stPlotlyChart').first
                    chart.scroll_into_view_if_needed()
                    chart.locator('.main-svg').first.wait_for(timeout=30000)
                    chart.screenshot(path=str(OUT / f'{route or "overview"}-chart-{width}.png'))
                results.append({'page': route or 'overview', 'width': width, 'http': response.status, 'horizontal_page_overflow': overflow})
            print(f'Checked five pages at {width}px', flush=True)
        page.close()
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        page.set_default_timeout(15000)
        page.goto('http://localhost:8501/')
        ready(page, 'RetainWise')
        for route, title in PAGES[1:]:
            page.locator(f'a[href$="/{route}"]').click()
            ready(page, title)
        results.append({'navigation': 'all sidebar links passed'})
        page.goto('http://localhost:8501/patterns')
        ready(page, 'Workforce Patterns')
        combo = page.get_by_role('combobox', name='Workplace characteristic')
        combo.click()
        page.get_by_role('option', name='Job satisfaction', exact=True).click()
        page.wait_for_timeout(700)
        assert page.get_by_test_id('stException').count() == 0
        page.get_by_role('tab', name='Tenure & compensation').click()
        page.get_by_role('combobox', name='Tenure or compensation measure').click()
        page.get_by_role('option', name='Monthly income (source units)', exact=True).click()
        page.wait_for_timeout(700)
        assert page.get_by_test_id('stException').count() == 0
        page.screenshot(path=str(OUT / 'income-desktop.png'), full_page=True)
        chart = page.get_by_test_id('stPlotlyChart').nth(1)
        chart.scroll_into_view_if_needed()
        chart.locator('.main-svg').first.wait_for()
        chart.screenshot(path=str(OUT / 'income-box-desktop.png'))
        page.set_viewport_size({'width': 390, 'height': 844})
        chart.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        chart.screenshot(path=str(OUT / 'income-box-mobile.png'))
        results.append({'explorer': 'satisfaction and monthly income selection passed'})
        browser.close()
    (OUT / 'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(json.dumps(results, indent=2))
