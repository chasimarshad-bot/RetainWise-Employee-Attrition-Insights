"""Execute each notebook in its own clean kernel; stop on the first error."""
from pathlib import Path
import os
import sys
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
os.environ['JUPYTER_PATH'] = str(Path(sys.prefix) / 'share/jupyter') + os.pathsep + os.environ.get('JUPYTER_PATH', '')

if __name__ == '__main__':
    for path in sorted((ROOT / 'jupyter_notebooks').glob('*.ipynb')):
        notebook = nbformat.read(path, as_version=4)
        client = NotebookClient(notebook, timeout=180, kernel_name='python3', resources={'metadata': {'path': str(ROOT)}})
        client.execute()
        # Execution host paths are not useful assessment evidence and vary by machine.
        for cell in notebook.cells:
            cell.get('metadata', {}).pop('execution', None)
        nbformat.write(notebook, path)
        print(f'Executed {path.name}', flush=True)
