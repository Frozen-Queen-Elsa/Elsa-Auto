import subprocess
import sys
import os
import pkg_resources

# Đường dẫn tới file requirements.txt
requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'requirements.txt')

# Đường dẫn tới file setup.py
setup_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setup.py')

# Hàm kiểm tra các thư viện trong requirements.txt
def check_requirements(requirements_path):
    with open(requirements_path, 'r') as file:
        requirements = file.readlines()
    
    # Lấy danh sách các thư viện đã cài đặt
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    
    # Kiểm tra từng thư viện trong requirements.txt
    missing_requirements = []
    for requirement in requirements:
        requirement = requirement.strip()
        if requirement and requirement not in installed_packages:
            missing_requirements.append(requirement)
    
    return missing_requirements

# Kiểm tra các thư viện trong requirements.txt
missing_requirements = check_requirements(requirements_path)

# Nếu thiếu thư viện nào, chạy file setup.py để cài đặt
if missing_requirements:
    print(f"Missing requirements: {missing_requirements}")
    subprocess.check_call([sys.executable, setup_path])
else:
    print("All requirements are satisfied.")
    
# Chạy file ElsaCuuGioi.py
elsa_cuu_gioi_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ElsaCuuGioi.py')
subprocess.check_call([sys.executable, elsa_cuu_gioi_path])