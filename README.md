# ElsaAuto Project

Dự án ElsaAuto tự động hóa các tác vụ chính bao gồm:  
- Cài đặt chương trình  
- Tạo tài khoản tự động qua file cấu hình  
- Chạy chế độ Cửu Giới  
- Đọc truyện

## 1. Cài đặt Python và Thư viện

1. **Cài đặt Python:**  
   Tải và cài đặt Python 3 từ [python.org](https://www.python.org/downloads/).

2. **Cài đặt các thư viện phụ thuộc:**  
   Mở terminal và chạy:
   ```sh
   python -m pip install -r Data/requirements.txt

2. Chạy Chương Trình Cài Đặt
Chạy file ElsaAuto.py để cài đặt và kiểm tra các thiết lập:
python ElsaAuto.py


3. Cấu Hình Tài Khoản
Mở file setting.json và chỉnh sửa key "SốAccount" theo số lượng tài khoản cần tạo.
Sau đó, chạy file generate_accounts.py để tự động tạo cấu trúc tài khoản:
python Data/generate_accounts.py
Nếu cần, mở lại file setting.json để điều chỉnh các thông số khác của tài khoản.

4. Chạy Các Chức Năng Chính
Chế độ Cửu Giới:
Khởi chạy chế độ Cửu Giới qua file ElsaCuuGioi.py:
python ElsaCuuGioi.py
Đọc Truyện:
Khởi chạy chế độ Đọc Truyện qua file ElsaDocTruyen.py:
python ElsaDocTruyen.py

5. Ghi Log và Kiểm Tra Lỗi
Các log được lưu trong thư mục Logs.
Kiểm tra log để xem thông tin chi tiết hoặc lỗi phát sinh trong quá trình chạy chương trình.
