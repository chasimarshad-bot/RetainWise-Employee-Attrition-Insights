"""Retrieve the original Kaggle archive without third-party mirrors."""
from pathlib import Path
import hashlib
import io
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'WA_Fn-UseC_-HR-Employee-Attrition.csv'
EXPECTED = 'a5c31e38bd7fafc9bc333884eb181b06b41b8e5e488e8f7ccb27199fb3be7659'

if __name__ == '__main__':
    url = 'https://www.kaggle.com/api/v1/datasets/download/pavansubhasht/ibm-hr-analytics-attrition-dataset'
    request = urllib.request.Request(url, headers={'User-Agent': 'RetainWise educational reproducibility/1.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        archive = response.read()
    with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
        content = zipped.read(NAME)
    if hashlib.sha256(content).hexdigest() != EXPECTED:
        raise SystemExit('Source checksum changed. Review source and licence before accepting a new version.')
    destination = ROOT / 'data/raw' / NAME
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    print(f'Acquired and verified {NAME}')
