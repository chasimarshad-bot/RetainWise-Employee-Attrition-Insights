"""Export only committed project files, with a revision and SHA-256 manifest."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'artifacts/submission'


if __name__ == '__main__':
    dirty = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=normal'], cwd=ROOT, text=True)
    if dirty.strip():
        raise SystemExit('Commit reviewed changes before packaging; ignored build artefacts are excluded automatically.')
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    OUT.mkdir(parents=True, exist_ok=True)
    archive = OUT / f'RetainWise-Unit3-{revision[:7]}.zip'
    subprocess.run(['git', 'archive', '--format=zip', '--prefix=RetainWise-Unit3/', '--output', str(archive), revision], cwd=ROOT, check=True)
    with zipfile.ZipFile(archive) as zipped:
        files = zipped.namelist()
        for name in files:
            if any(part in {'.git', '.venv', 'artifacts', '__pycache__'} for part in Path(name).parts):
                raise ValueError(f'Unexpected build artefact in archive: {name}')
        verification = json.loads(zipped.read('RetainWise-Unit3/docs/qa/submission_verification.json'))
        for name, expected in verification['source_files_lf_sha256'].items():
            digest = hashlib.sha256(zipped.read('RetainWise-Unit3/' + name).replace(b'\r\n', b'\n')).hexdigest()
            if digest != expected:
                raise ValueError(f'Archive no longer matches reviewed source: {name}')
        manifest = {'revision': revision, 'archive': archive.name,
                    'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'files': files}
    manifest_path = OUT / f'RetainWise-Unit3-{revision[:7]}-manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps({'archive': str(archive), 'manifest': str(manifest_path), 'revision': revision, 'sha256': manifest['sha256'], 'entries': len(files)}, indent=2))
