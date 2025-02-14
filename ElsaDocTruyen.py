import os
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from HamPhuTro.GhiLog import ghi_log, LogStyle
from HamPhuTro.Exception import handle_exception as xu_ly_ngoai_le
from Auto.DocTruyen import vao_trang_truyen
from Auto.DangNhap import dang_nhap   # Import hàm đăng nhập từ DangNhap.py

# Import các hàm từ DataMoiTaiKhoan để lấy cấu hình thay vì đọc trực tiếp file setting.json
from Data.DataMoiTaiKhoan import lay_url_web, lay_thong_tin_tai_khoan
from Data.DataMoiTaiKhoan import lay_so_account

# Sử dụng hàm lay_url_web để lấy URL của trang web
dia_chi_web = lay_url_web()

# Đường dẫn tới Brave và chromedriver.exe
duong_dan_brave = r"C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
duong_dan_chromedriver = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.exe')

def chay_trinh_duyet(account_number):
    try:
        # Lấy thông tin của tài khoản từ cấu hình đã được load bởi hàm trong DataMoiTaiKhoan
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Không xác định")
        ghi_log(ten_tai_khoan, "Khởi tạo trình duyệt Brave", level='info')
        
        # Thiết lập chrome options
        chrome_options = Options()
        chrome_options.binary_location = duong_dan_brave
        #chrome_options.add_argument("--start-maximized") # Mở cửa sổ trình duyệt với kích thước lớn nhất
        chrome_options.add_argument("--window-size=100,500")  # Chỉnh kích thước cửa sổ lúc vừa mở
        # Thêm option zoom trình duyệt với kích thước tùy chỉnh (ví dụ: 50% zoom)
        chrome_options.add_argument("--force-device-scale-factor=0.5")
        
        # Thêm option ẩn tất cả hình ảnh trên web
        # chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        
        #chrome_options.add_argument('--headless')  # Thêm tùy chọn headless
        chrome_options.add_argument('--disable-gpu')  # Tắt GPU (cần thiết cho một số hệ thống)
        
        
        
        # Tối ưu hệ thống
        chrome_options.add_argument("--disable-extensions") # Tắt các extension
        chrome_options.add_argument("--disable-infobars") # Tắt thanh thông tin
        chrome_options.add_argument("--disable-notifications") # Tắt thông báo

        
        
        
        # Khởi tạo webdriver
        dich_vu = Service(executable_path=duong_dan_chromedriver)
        trinh_duyet = webdriver.Chrome(service=dich_vu, options=chrome_options)
        
        # Thực hiện đăng nhập, sau đó chuyển tới trang truyện
        dang_nhap(trinh_duyet,account_number)        
        # Sau khi khởi tạo webdriver, có thể zoom nội dung trang web (zoom phần nội dung trang web)
        trinh_duyet.execute_script("document.body.style.zoom='50%'")
        vao_trang_truyen(trinh_duyet,account_number)

        
        # Giữ trình duyệt mở vô thời hạn
        while True:
            time.sleep(60)
    except Exception as loi:
        xu_ly_ngoai_le(loi)

def bat_dau_chay():
    # Lấy danh sách AccountNumber từ biến SốAccount trong file setting.json
    so_account = lay_so_account()
    danh_sach_account = list(range(1, so_account + 1))
    danh_sach_luong = []
    for account_number in danh_sach_account:
        luong = threading.Thread(target=chay_trinh_duyet, args=(account_number,))
        luong.daemon = True
        luong.start()
        danh_sach_luong.append(luong)
        ghi_log(str(account_number), "Luồng đã khởi chạy", level='info')
    
    for luong in danh_sach_luong:
        luong.join()

if __name__ == "__main__":
    try:
        bat_dau_chay()
    except Exception as loi:
        xu_ly_ngoai_le(loi)