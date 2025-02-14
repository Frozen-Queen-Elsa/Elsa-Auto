from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import asyncio

from HamPhuTro.GhiLog import ghi_log, LogStyle
from HamPhuTro.Exception import handle_exception
from Data.DataMoiTaiKhoan import lay_url_web, lay_thong_tin_tai_khoan
from Auto.Token import lay_chapter_token, lay_token

def dang_nhap(driver, account_number):
    """
    Đăng nhập sử dụng thông tin trực tiếp từ DataMoiTaiKhoan (AccountNumber mặc định là 1).
    """
    url_trinh_duyet = lay_url_web()
    tai_khoan = lay_thong_tin_tai_khoan(account_number)
    id_dang_nhap = tai_khoan.get("IdLogin")
    mat_khau = tai_khoan.get("Password")
    ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
    
    try:
        # Bước 1: Mở trang đăng nhập
        ghi_log(ten_tai_khoan, "Mở trang đăng nhập", level='info')       
        driver.get(url_trinh_duyet + "/user/game/dashboard")
        
        # Bước 2: Tìm và click nút đăng nhập
        attempts = 0
        while attempts < 3:
            try:
                login_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[1]/header/div[3]/div[2]/div[3]/button[2]")
                    )
                )
                if login_button.is_displayed():
                    login_button.click()
                    ghi_log(ten_tai_khoan, "Đã click nút đăng nhập", level='info')
                    break
            except Exception as e:
                ghi_log(ten_tai_khoan, f"Lỗi khi tìm nút đăng nhập: {e}", level='warning')
                handle_exception(e)
                time.sleep(4)
                attempts += 1

        if attempts == 3:
            ghi_log(ten_tai_khoan, "Không tìm thấy nút đăng nhập, tải lại trang", level='error')
            driver.refresh()
            return dang_nhap(driver, account_number)
        
        # Bước 3: Đợi popup đăng nhập xuất hiện và điền thông tin đăng nhập
        ghi_log(ten_tai_khoan, "Chờ popup hiện và đăng nhập", level='info')
        while True:
            try:
                popup = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "popup_module.popup_login.center_div"))
                )
                if popup.is_displayed():
                    break
            except Exception as e:
                ghi_log(ten_tai_khoan, f"Lỗi khi tìm popup đăng nhập: {e}", level='warning')
                handle_exception(e)
                time.sleep(1)
        
        try:
            ghi_log(ten_tai_khoan, "Điền thông tin đăng nhập", level='info')
            id_field = driver.find_element(By.ID, "login_username")
            password_field = driver.find_element(By.ID, "login_password")
            id_field.send_keys(id_dang_nhap)
            password_field.send_keys(mat_khau)
            login_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[5]/div/div/div[2]/div[3]/button")
            
            # Sử dụng JavaScript để click vào nút đăng nhập
            driver.execute_script("arguments[0].click();", login_button)
            
            time.sleep(5)  # Đợi trang chuyển sau khi đăng nhập
            
            attempts = 0
            while attempts < 3:
                try:
                    login_button = driver.find_element(By.XPATH, "/html/body/div[1]/header/div[3]/div[2]/div[3]/button[2]")
                    if not login_button.is_displayed():
                        ghi_log(ten_tai_khoan, "Đăng nhập thành công", level='info')
                        time.sleep(5)
                        # Gọi các hàm lấy token với đúng đối số account_number
                      
                        asyncio.run(lay_chapter_token(account_number))
                        return True
                except Exception as e:
                    ghi_log(ten_tai_khoan, f"Lỗi khi kiểm tra nút đăng nhập: {e}", level='warning')
                    handle_exception(e)
                    time.sleep(5)
                    attempts += 1
            
            ghi_log(ten_tai_khoan, "Đăng nhập thất bại: Nút đăng nhập vẫn hiển thị", level='error')
            return False
        except Exception as e:
            ghi_log(ten_tai_khoan, f"Lỗi khi điền thông tin đăng nhập: {e}", level='error')
            handle_exception(e)
            return False
    except Exception as e:
        ghi_log(ten_tai_khoan, f"Lỗi khi mở trang đăng nhập: {e}", level='error')
        handle_exception(e)
        return False

def dang_xuat(driver, account_number):
    tai_khoan = lay_thong_tin_tai_khoan(account_number)
    ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Không xác định")
    ghi_log("Hệ thống", f"Bắt đầu đăng xuất {ten_tai_khoan}", level='info')
    try:
        # Tìm và click vào phần tử có class "profile" (menu mở)
        menu_open = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "profile"))
        )
        menu_open.click()
        ghi_log(ten_tai_khoan, "Đã click vào menu", level='info')
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "setting menu_hidden"))
        )
        
        logout_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/header/div[3]/div[2]/div[2]/ul/li[11]/a")
            )
        )
        driver.execute_script("arguments[0].click();", logout_button)
        ghi_log(ten_tai_khoan, "Đã click nút đăng xuất", level='info')
    except Exception as e:
        ghi_log("Hệ thống", f"Lỗi khi đăng xuất: {e}", level='error')
        handle_exception(e)