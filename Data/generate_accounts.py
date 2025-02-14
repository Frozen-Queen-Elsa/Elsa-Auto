import json
import os

# Đường dẫn tới file setting.json
current_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(current_dir, '../data/setting.json')

# Đọc nội dung file setting.json
with open(filepath, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Đọc số lượng tài khoản cần tạo từ file setting.json hoặc thiết lập mặc định
so_account = data.get('SốAccount', 1)

# Kiểm tra và tạo mảng accounts nếu chưa tồn tại
if "Accounts" not in data:
    data["Accounts"] = []

# Định nghĩa cấu trúc mẫu cho một tài khoản
account_template = {
    "IdIngame": 0,
    "TênTàiKhoản": "",
    "IdLogin": "",
    "Password": "",
    "ThầnMa": {
        "ThầnMa": False,
        "GiờThầnMa": "4,8",
        "GặpKẻThù": 0,
        "_description": "GặpKẻThù=0 : Để yên, 1: Đấm nó, 2:Chạy là thượng sách"
    },
    "CửuGiới": {
        "CửuGiới": True,
        "KhuVực": 0,
        "MaxTàiPhú": 5000,
        "TàiPhúOut": 5000,
        "NhặtVàng": True,
        "GặpShipper": 0,
        "_description": "GặpShipper=0 : Để yên, 1: Đấm nó, 2:Chạy là thượng sách",
        "ĐiMaxTàiPhú": False,
        "GócChạy": 1,
        "__description": "1 = gocTrenTrai ; 2 = gocTrenPhai; 3 = duoiTrai; 4 phai"
    },
    "TôngMônChiến": {
        "TôngMônChiến": True,
        "GặpKẻThù": 0,
        "DiChuyển": False,
        "KhuVựcHoạtĐộng": 0,
        "_description": "KhuVựcHoạtĐộng=0 : Ở bên ngoài, 1: Khu Tím, 2:Khu Lục,3: Rìa ngoài và Tím,4:Rìa Tím và Lục"
    },
    "ĐọcTruyện": {
        "ĐọcTruyện": True,
        "LinkTruyện": "https://cmangax.com/album/vo-luyen-dinh-phong-189/ref/29713"
    },
    "ThánhChiến":{
        "ThánhChiến": False,
        "RandomPhe":True,
        "SớVàngBet":1
    },
    "HằngNgày": {
        "HằngNgày":False,
        "CốngHiếnTôngMôn": False,
        "ThầnLongMộ": False,
        "TầmBảo": False
    },
    "Event":{
        "Event":False,
        "SinhTửChiến": False,
        "QuánQuânChiến": False,
    }
    
}

# Hàm kiểm tra và cập nhật cấu trúc của từng tài khoản
def update_account_structure(account, template):
    for key, value in template.items():
        if key not in account:
            account[key] = value
        elif isinstance(value, dict):
            if not isinstance(account[key], dict):
                account[key] = value
            else:
                update_account_structure(account[key], value)
    return account

# Kiểm tra và sửa cấu trúc của từng tài khoản trong mảng Accounts
for i, account in enumerate(data["Accounts"]):
    data["Accounts"][i] = update_account_structure(account, account_template)

# Tạo hoặc xóa tài khoản để phù hợp với số lượng SốAccount
current_account_count = len(data["Accounts"])

if current_account_count < so_account:
    for i in range(current_account_count, so_account):
        account = account_template.copy()
        account["IdIngame"] = 100000 + i  # Tạo IdIngame duy nhất cho mỗi tài khoản
        account["TênTàiKhoản"] = f"Tên nhân vật {i+1}"
        account["IdLogin"] = f"user{i+1}"
        account["Password"] = f"password{i+1}"
        
        # Tạo dictionary mới với AccountNumber ở đầu
        account_with_number = {"AccountNumber": i + 1}
        account_with_number.update(account)
        
        data["Accounts"].append(account_with_number)
elif current_account_count > so_account:
    data["Accounts"] = data["Accounts"][:so_account]

# Hàm ghi JSON với dòng trắng giữa các tài khoản
def write_json_with_blank_lines(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        json_str = json.dumps(data, ensure_ascii=False, indent=4)
        json_str = json_str.replace('},\n        {', '},\n\n        {')
        file.write(json_str)

# Ghi lại nội dung mới vào file setting.json với dòng trắng giữa các tài khoản
write_json_with_blank_lines(filepath, data)

print(f"Đã cập nhật {so_account} tài khoản trong mảng accounts.")