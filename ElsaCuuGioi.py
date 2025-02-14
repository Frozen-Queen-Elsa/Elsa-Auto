import os
import threading
import time
import asyncio
import nest_asyncio  # Import nest_asyncio ở đây, không bên trong hàm
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidSessionIdException

from HamPhuTro.GhiLog import ghi_log, LogStyle
from HamPhuTro.Exception import handle_exception as xu_ly_ngoai_le
from Auto.DocTruyen import vao_trang_truyen
from Auto.DangNhap import dang_nhap   # Import hàm đăng nhập từ DangNhap.py
from Auto.Token import lay_chapter_token, lay_token
from Auto.CuuGioi import vao_trang_cuu_gioi, listen_for_events  # Import hàm vào trang cứu giới từ CuuGioi2.py

from Data.DataMoiTaiKhoan import lay_url_web, lay_thong_tin_tai_khoan
from Data.DataMoiTaiKhoan import lay_so_account

# Áp dụng nest_asyncio toàn cục
nest_asyncio.apply()

# Sử dụng hàm lay_url_web để lấy URL của trang web
dia_chi_web = lay_url_web()

# Đường dẫn tới Chrome và chromedriver.exe
duong_dan_chrome = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
duong_dan_chromedriver = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver.exe')


def mo_trinh_duyet(account_number):
    try:
        # Lấy thông tin của tài khoản từ cấu hình đã được load bởi hàm trong DataMoiTaiKhoan
        URLweb = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        id_nhan_vat = tai_khoan.get("IdIngame")
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        cuu_gioi = tai_khoan.get("CửuGiới", {})
        khu_vuc = cuu_gioi.get("KhuVực")
        max_tai_phu = cuu_gioi.get("MaxTàiPhú", 9000)
        tai_phu_out = cuu_gioi.get("TàiPhúOut", 9000)
        nhat_vang = cuu_gioi.get("NhặtVàng", False)
        if nhat_vang:
            max_tai_phu = 0
        gap_shipper = cuu_gioi.get("GặpShipper", 1)
        di_max_tai_phu = "yes" if cuu_gioi.get("ĐiMaxTàiPhú", False) else "NO"
        goc_chay = cuu_gioi.get("GócChạy", 1)
        ghi_log(ten_tai_khoan, "Khởi tạo trình duyệt ", level='info')

        # Khởi tạo webdriver
        chrome_options = Options()
        chrome_options.binary_location = duong_dan_chrome

        #chrome_options.add_argument("--start-maximized") # Mở cửa sổ trình duyệt với kích thước lớn nhất
        #chrome_options.add_argument("--window-size=100,500")  # Chỉnh kích thước cửa sổ lúc vừa mở
        #chrome_options.add_argument("--force-device-scale-factor=0.5")
        # chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        #chrome_options.add_argument('--headless')  # Thêm tùy chọn headless
        chrome_options.add_argument('--disable-gpu')  # Tắt GPU (cần thiết cho một số hệ thống)

        # Khởi tạo webdriver
        dich_vu = Service(executable_path=duong_dan_chromedriver)
        trinh_duyet = webdriver.Chrome(service=dich_vu, options=chrome_options)

        # Thực hiện đăng nhập, sau đó chuyển tới trang truyện
        dang_nhap(trinh_duyet, account_number)
        # Gọi các hàm lấy token với đúng đối số account_number
  


        # Vào trang Cửu Giới:
        asyncio.run(vao_trang_cuu_gioi(trinh_duyet, account_number))

        # Vòng lặp kiểm tra trình duyệt vẫn mở
        while True:
            try:
                _ = trinh_duyet.title
            except Exception as e:
                if isinstance(e, InvalidSessionIdException) or "invalid session id" in str(e).lower():
                    break
                else:
                    xu_ly_ngoai_le(e)
                    break
            time.sleep(60)
    except Exception as loi:
        xu_ly_ngoai_le(loi)


def bat_dau_chay():
    so_account = lay_so_account()
    danh_sach_account = list(range(1, so_account + 1))
    danh_sach_luong = []

    for account_number in danh_sach_account:
        luong = threading.Thread(target=mo_trinh_duyet, args=(account_number,))
        danh_sach_luong.append(luong)
        luong.start()

    for luong in danh_sach_luong:
        luong.join()

    print("Tất cả các luồng đã kết thúc, ứng dụng sẽ dừng lại.")


if __name__ == "__main__":
    bat_dau_chay()