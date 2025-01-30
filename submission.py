import os
import zipfile
import fnmatch

EXCLUDE_DIRS = {'Debug', 'Release', 'ipch', '.vs'}
EXCLUDE_PATTERNS = ['*.aps', '*.pdb', '*.obj', '*.ilk', '*.cache', '*.suo', 'submission.py']

ID = "" # put your ID here

def get_user_id():
    email = input("your email(eg：simpsonbart@msu.edu): ").strip()
    return email.split('@')[0]

def find_grading_doc():
    for f in os.listdir():
        if 'grade' in f.lower() and os.path.isfile(f):
            return f
    return None

def create_zip(zip_filename):
    project_root = os.getcwd()
    grading_doc = find_grading_doc()
    sln_files = [f for f in os.listdir() if f.endswith('.sln')]

    # add explicit files(absolute path)
    explicit_files = set()
    for sln in sln_files:
        explicit_files.add(os.path.abspath(sln))
    if grading_doc:
        explicit_files.add(os.path.abspath(grading_doc))

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
        # add project files
        for root, dirs, files in os.walk(project_root):
            # filter out excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                file_path = os.path.join(root, file)

                # filter out excluded files
                if file_path in explicit_files:
                    continue

                if any(fnmatch.fnmatch(file, p) for p in EXCLUDE_PATTERNS):
                    continue

                arcname = os.path.relpath(file_path, project_root)
                zf.write(file_path, arcname)

        # add solution files
        for sln in sln_files:
            zf.write(sln, os.path.basename(sln))
        
        # add grading document
        if grading_doc:
            zf.write(grading_doc, os.path.basename(grading_doc))

def main():
    print("make sure you closed Visual Studio, press enter to continue")
    input()
    
    user_id = get_user_id() if ID == "" else ID
    EXCLUDE_PATTERNS.append(f"{user_id}.zip")
    zip_filename = f"{user_id}.zip"
    
    create_zip(zip_filename)
    
    # check file size
    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    if size_mb > 10:
        print(f"warning: file size ({size_mb:.1f}MB)，please check if any large files included") 

    print(f"successfully created submission: {zip_filename}")

if __name__ == "__main__":
    main()