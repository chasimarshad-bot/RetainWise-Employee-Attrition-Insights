"""Verify committed data contracts and executed notebooks before packaging."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import nbformat
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from retainwise.data import RAW, DATA, PROCESSED, prepare, load_data, validate_source
from retainwise.analysis import hypothesis_evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--review-date', required=True, help='Review date in Europe/London, YYYY-MM-DD')
    args = parser.parse_args()
    metadata = json.loads((PROCESSED / 'metadata_v1.json').read_text(encoding='utf-8'))
    raw = pd.read_csv(RAW)
    data = load_data()
    checks = {
        'source_validation': validate_source(raw),
        'source_hash_matches': hashlib.sha256(RAW.read_bytes()).hexdigest() == metadata['source_sha256'],
        'processed_hash_matches': hashlib.sha256(DATA.read_bytes()).hexdigest() == metadata['processed_sha256'],
        'preparation_matches_versioned_data': prepare(raw).equals(data),
        'dictionary_complete': not pd.read_csv(PROCESSED / 'data_dictionary_v1.csv').description.isna().any(),
        'hypothesis_evidence_matches': hypothesis_evidence(data) == json.loads((PROCESSED / 'hypothesis_evidence_v1.json').read_text(encoding='utf-8')),
        'notebooks': [],
    }
    for path in sorted((ROOT / 'jupyter_notebooks').glob('*.ipynb')):
        notebook = nbformat.read(path, as_version=4)
        code = [cell for cell in notebook.cells if cell.cell_type == 'code']
        errors = [out for cell in code for out in cell.get('outputs', []) if out.get('output_type') == 'error']
        executed = all(cell.execution_count is not None for cell in code)
        checks['notebooks'].append({'file': path.name, 'code_cells': len(code), 'all_executed': executed, 'error_outputs': len(errors)})
        if not executed or errors:
            raise SystemExit(f'Notebook execution evidence failed: {path.name}')
    for name, value in checks.items():
        if isinstance(value, (bool, type(pd.Series([True]).all()))) and not value:
            raise SystemExit(f'Verification failed: {name}')
    report = {'review_date': args.review_date, 'python': sys.version.split()[0],
              'reviewed_base_revision': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'source_files_lf_sha256': {name: hashlib.sha256((ROOT / name).read_bytes().replace(b'\r\n', b'\n')).hexdigest()
                  for name in ['app.py', 'retainwise/ui.py', 'retainwise/data.py', 'retainwise/analysis.py', 'retainwise/charts.py', 'requirements.txt', 'Dockerfile']},
              'checks': checks, 'result': 'passed'}
    destination = ROOT / 'docs/qa/submission_verification.json'
    destination.write_text(json.dumps(report, indent=2, default=bool), encoding='utf-8')
    print(json.dumps(report, indent=2, default=bool))
