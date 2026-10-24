"""Check project-owned document links, with network failures recorded separately."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import re
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]


def check(url):
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 RetainWise link review'})
        with urllib.request.urlopen(request, timeout=20) as response:
            return {'url': url, 'status': response.status}
    except urllib.error.HTTPError as exc:
        return {'url': url, 'status': exc.code, 'note': 'Access restriction or failure; review manually'}
    except Exception as exc:
        return {'url': url, 'status': None, 'note': type(exc).__name__}


if __name__ == '__main__':
    files = [ROOT / 'README.md', ROOT / 'data/SOURCE.md', *sorted((ROOT / 'docs').glob('*.md'))]
    urls = set()
    missing = []
    for path in files:
        if path.name == 'PRD.md':
            continue
        content = path.read_text(encoding='utf-8-sig')
        urls.update(re.findall(r'https?://[^\s)<>`]+', content))
        for target in re.findall(r'\]\(([^)]+)\)', content):
            if not target.startswith(('https://', 'http://', '#')) and not (path.parent / target.split('#')[0]).exists():
                missing.append({'file': str(path.relative_to(ROOT)), 'target': target})
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(check, sorted(urls)))
    report = {'external': results, 'missing_local_links': missing}
    destination = ROOT / 'docs/link_check.json'
    destination.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    if missing:
        raise SystemExit(1)
