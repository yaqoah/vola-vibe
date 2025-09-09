import zipfile
import os

PROJECT_ROOT = r"C:\Users\Balot\OneDrive\Coding-Python\vola-vibe"
OUTPUT_ZIP = r"C:\Users\Balot\Downloads\vola-vibe.zip"

def create_zip(project_root=PROJECT_ROOT, output_zip=OUTPUT_ZIP):
    print("[Cloud / Deployment] Creating package for Google Colab")

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in ["aggregator.py", "config.py"]:
            filepath = os.path.join(project_root, file)
            if os.path.exists(filepath):
                zf.write(filepath, arcname=file)

        models_dir = os.path.join(project_root, "models")
        if os.path.exists(models_dir):
            for root, _, files in os.walk(models_dir):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)

                        arcname = os.path.relpath(file_path, project_root)
                        zf.write(file_path, arcname=arcname)

        req_path = os.path.join(project_root, "requirements.txt")
        if os.path.exists(req_path):
            zf.write(req_path, arcname="requirements.txt")

    print(f"✅ Created {output_zip} ({os.path.getsize(output_zip) / 1e6:.1f} MB)")

if __name__ == "__main__":
    create_zip()
