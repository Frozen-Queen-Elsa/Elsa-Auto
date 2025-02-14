import subprocess
import sys
import os
import pkg_resources

# Đường dẫn tới file requirements.txt
requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Data', 'requirements.txt')

# Hàm kiểm tra và cài đặt các thư viện trong requirements.txt
def install_requirements(requirements_path):
    with open(requirements_path, 'r') as file:
        requirements = file.readlines()
    
    # Lấy danh sách các thư viện đã cài đặt
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    
    # Lặp qua từng thư viện trong requirements.txt và cài đặt nếu chưa có
    for requirement in requirements:
        requirement = requirement.strip()
        if requirement and requirement not in installed_packages:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', requirement])

# Kiểm tra và cài đặt các thư viện trong requirements.txt
install_requirements(requirements_path)