import os
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        if 'venv' in root or '__pycache__' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            ziph.write(file_path, os.path.relpath(file_path, '.'))

with zipfile.ZipFile('backend.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir('backend', zipf)
print("Finished zipping backend!")
