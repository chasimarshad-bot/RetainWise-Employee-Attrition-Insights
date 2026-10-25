"""Check browser accessibility and keyboard tasks without claiming certification."""
from pathlib import Path
import argparse
import base64
import hashlib
import io
import json
import tarfile
import urllib.request
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/accessibility'
PAGES = [('', 'RetainWise'), ('patterns', 'Workforce Patterns'), ('hypotheses', 'Hypothesis Lab'),
         ('governance', 'Fairness & Governance'), ('methodology', 'Methodology & Project Plan')]
AXE_VERSION = '4.10.3'


def axe_source():
    """Verify the upstream npm package before loading its browser-only audit code."""
    with urllib.request.urlopen(f'https://registry.npmjs.org/axe-core/{AXE_VERSION}', timeout=30) as response:
        metadata = json.load(response)
    with urllib.request.urlopen(metadata['dist']['tarball'], timeout=30) as response:
        archive = response.read()
    integrity = 'sha512-' + base64.b64encode(hashlib.sha512(archive).digest()).decode()
    if integrity != metadata['dist']['integrity']:
        raise ValueError('Accessibility library integrity check failed')
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as bundle:
        return bundle.extractfile('package/axe.min.js').read().decode()


def ready(page, title):
    page.get_by_role('heading', name=title, exact=True).wait_for(timeout=30000)
    page.get_by_text('RetainWise · Unit 3 capstone', exact=False).wait_for(state='attached', timeout=30000)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://localhost:8501')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    source = axe_source()
    report = {'tool': f'axe-core {AXE_VERSION}', 'pages': [], 'keyboard_tasks': []}
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 1000})
        for route, title in PAGES:
            page.goto(args.url.rstrip('/') + '/' + route)
            ready(page, title)
            if route != 'methodology':
                chart = page.get_by_test_id('stPlotlyChart').first
                chart.scroll_into_view_if_needed()
                chart.locator('.main-svg').first.wait_for(timeout=30000)
            page.add_script_tag(content=source)
            result = page.evaluate('''async () => await axe.run(document, {
                runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa']}
            })''')
            findings = [{key: finding[key] for key in ['id', 'impact', 'description', 'helpUrl', 'nodes']}
                        for finding in result['violations']]
            report['pages'].append({'page': route or 'overview', 'violations': findings,
                                    'passed_rules': len(result['passes']),
                                    'manual_review_rules': [item['id'] for item in result['incomplete']]})
            (OUT / 'results.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
            print(f'{route or "overview"}: {len(findings)} automated findings', flush=True)

        page.goto(args.url.rstrip('/') + '/patterns')
        ready(page, 'Workforce Patterns')
        select = page.get_by_role('combobox', name='Workplace characteristic')
        select.focus()
        page.keyboard.press('Home')
        page.keyboard.press('ArrowDown')
        page.keyboard.press('Enter')
        page.wait_for_timeout(500)
        assert select.input_value() == 'Job satisfaction'
        report['keyboard_tasks'].append({'task': 'Change workplace measure using arrows and Enter', 'result': 'passed'})
        tab = page.get_by_role('tab', name='Workplace & engagement')
        tab.focus()
        page.keyboard.press('ArrowRight')
        assert page.get_by_role('tab', name='Tenure & compensation').get_attribute('aria-selected') == 'true'
        report['keyboard_tasks'].append({'task': 'Move between tabs using the keyboard', 'result': 'passed'})
        link = page.locator('a[href$="/hypotheses"]')
        link.focus()
        page.keyboard.press('Enter')
        ready(page, 'Hypothesis Lab')
        report['keyboard_tasks'].append({'task': 'Navigate to the Lab with Enter', 'result': 'passed'})
        disclosure = page.get_by_test_id('stExpander').last.locator('summary')
        disclosure.focus()
        before = disclosure.locator('xpath=..').get_attribute('open')
        page.keyboard.press('Enter')
        after = disclosure.locator('xpath=..').get_attribute('open')
        assert before != after
        report['keyboard_tasks'].append({'task': 'Open technical evidence using Enter', 'result': 'passed'})
        report['limits'] = 'Automated WCAG-tagged rules and four keyboard tasks; not a screen-reader audit or conformance certification.'
        browser.close()
    (OUT / 'results.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'pages': len(report['pages']), 'violations': sum(len(p['violations']) for p in report['pages']), 'keyboard_tasks': len(report['keyboard_tasks'])}, indent=2))
    if any(page['violations'] for page in report['pages']):
        raise SystemExit(1)
