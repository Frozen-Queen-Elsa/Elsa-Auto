import os
import time
from selenium.webdriver.common.by import By

from HamPhuTro.GhiLog import ghi_log, LogStyle
from Data.DataMoiTaiKhoan import lay_thong_tin_tai_khoan

def AutoDocTruyen(trinh_duyet,account_number):
    """
    Tự động chuyển chap truyện theo cấu hình được lưu trong setting.json thông qua DataMoiTaiKhoan.
    Lấy thông tin tài khoản trực tiếp từ DataMoiTaiKhoan (sử dụng account mặc định là 1).
    """
    # Lấy thông tin tài khoản mặc định (AccountNumber = 1)
    
    tai_khoan = lay_thong_tin_tai_khoan(account_number)
    ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Không xác định")
    doc_truyen = tai_khoan.get("ĐọcTruyện", {})
    link_truyen = doc_truyen.get("LinkTruyện", "")  # Sử dụng key "LinkTruyện" thay vì "LinkTruyen"
    
    try:
        url = trinh_duyet.current_url
        ghi_log(ten_tai_khoan, f"URL hiện tại: {url}", level='info', style=LogStyle.GREEN)
        if "/chapter-undefined" in url:
            ghi_log(ten_tai_khoan,
                    f'URL chứa "/chapter-undefined", chuyển hướng đến trang truyện: {link_truyen}',
                    level='info', style=LogStyle.GREEN)
            trinh_duyet.get(link_truyen)
        elif "/chapter-" in url and "/chapter-undefined" not in url:
            ghi_log(ten_tai_khoan,
                    'URL chứa "/chapter-" và không chứa "/chapter-undefined"',
                    level='info', style=LogStyle.GREEN)
            time.sleep(5)
            nut_next_chapter = trinh_duyet.find_element(By.CLASS_NAME, 'next_chapter')
            ghi_log(ten_tai_khoan,
                    f'Nút Next Chapter: {nut_next_chapter}',
                    level='info', style=LogStyle.GREEN)
            if nut_next_chapter and nut_next_chapter.is_displayed():
                ghi_log(ten_tai_khoan,
                        'Nút Next Chapter hiển thị, bấm nút',
                        level='info', style=LogStyle.GREEN)
                nut_next_chapter.click()
                ghi_log(ten_tai_khoan,
                        'Đợi 61 giây để chuyển chap',
                        level='info', style=LogStyle.GREEN)
                time.sleep(61)
                AutoDocTruyen(trinh_duyet)
            elif nut_next_chapter and not nut_next_chapter.is_displayed():
                ghi_log(ten_tai_khoan,
                        'Nút Next Chapter ẩn, tìm và bấm vào album truyện',
                        level='info', style=LogStyle.GREEN)
                phan_tu_muc_tieu = trinh_duyet.find_element(By.XPATH,
                                                           '/html/body/div[2]/div/div[1]/h2/span[2]/a/span')
                ghi_log(ten_tai_khoan,
                        f'Phần tử mục tiêu: {phan_tu_muc_tieu}',
                        level='info', style=LogStyle.GREEN)
                if phan_tu_muc_tieu:
                    phan_tu_muc_tieu.click()
            else:
                ghi_log(ten_tai_khoan,
                        'Không tìm thấy nút Next Chapter, kiểm tra lại sau 61 giây',
                        level='info', style=LogStyle.GREEN)
                time.sleep(61)
                AutoDocTruyen(trinh_duyet)
        elif "/ref/" in url:
            ghi_log(ten_tai_khoan,
                    'URL chứa "/ref/", đợi 10 giây để tìm và bấm nút "read_first"',
                    level='info', style=LogStyle.GREEN)
            time.sleep(10)
            lan_thu = 0
            def bam_read_first():
                nonlocal lan_thu
                nut_read_first = trinh_duyet.find_element(By.CLASS_NAME, 'read_first')
                ghi_log(ten_tai_khoan,
                        f'Lần thử tìm nút Read First thứ {lan_thu + 1}: {nut_read_first}',
                        level='info', style=LogStyle.GREEN)
                if nut_read_first:
                    ghi_log(ten_tai_khoan,
                            'Tìm thấy nút Read First, bấm nút',
                            level='info', style=LogStyle.GREEN)
                    nut_read_first.click()
                elif lan_thu < 4:
                    lan_thu += 1
                    ghi_log(ten_tai_khoan,
                            'Không tìm thấy nút Read First, thử lại sau 5 giây',
                            level='info', style=LogStyle.GREEN)
                    time.sleep(5)
                    bam_read_first()
                else:
                    ghi_log(ten_tai_khoan,
                            'Đã thử 5 lần mà không tìm thấy nút Read First',
                            level='error', style=LogStyle.RED)
            bam_read_first()
    except Exception as e:
        ghi_log(ten_tai_khoan,
                f"Lỗi trong AutoDocTruyen: {e}",
                level='error', style=LogStyle.RED)

def vao_trang_truyen(trinh_duyet,account_number):
    """
    Chuyển hướng trình duyệt đến trang truyện dựa trên LinkTruyen trong cấu hình.
    Sử dụng thông tin tài khoản trực tiếp từ DataMoiTaiKhoan (mặc định AccountNumber = 1).
    Sau khi chuyển hướng, tự động bắt đầu chuyển chap.
    """
    
    tai_khoan = lay_thong_tin_tai_khoan(account_number)
    ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Không xác định")
    doc_truyen = tai_khoan.get("ĐọcTruyện", {})
    link_truyen = doc_truyen.get("LinkTruyện", "")  # Sử dụng key "LinkTruyện" thay vì "LinkTruyen"
    
    try:
        ghi_log(ten_tai_khoan,
                f"Chuyển đến trang truyện: {link_truyen}",
                level='info', style=LogStyle.GREEN)
        trinh_duyet.get(link_truyen)
        # Sau khi vào trang truyện, bắt đầu tự động chuyển chap
        AutoDocTruyen(trinh_duyet,account_number)
    except Exception as e:
        ghi_log(ten_tai_khoan,
                f"Lỗi khi chuyển trang truyện: {e}",
                level='error', style=LogStyle.RED)