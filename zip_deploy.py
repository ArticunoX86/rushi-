import os
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'alembic_versions']]
        for file in files:
            if not file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                ziph.write(file_path, arcname=os.path.relpath(file_path, start='.'))

if __name__ == '__main__':
    with zipfile.ZipFile('deploy.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir('backend', zipf)
        zipdir('frontend/dist', zipf)
    print("Created deploy.zip successfully!")
