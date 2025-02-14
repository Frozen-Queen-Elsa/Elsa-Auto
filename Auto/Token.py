import asyncio
import aiohttp
import json
import os
import re
import threading
from Data.DataMoiTaiKhoan import lay_thong_tin_tai_khoan,lay_url_web,set_thread_var_text  # đường dẫn chính xác đến DataMoiTaiKhoan.py
from HamPhuTro.GhiLog import ghi_log, LogStyle
duong_dan_setting = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Data', 'setting.json')


# Sử dụng threading.local để lưu biến TOKEN riêng cho mỗi luồng
local_cho_luong = threading.local()




import aiohttp
import re
import threading

# Sử dụng threading.local để lưu biến TOKEN riêng cho mỗi luồng
local_cho_luong = threading.local()

async def lay_token(account_number):
    try:
        URL = lay_url_web()
        tai_khoan=lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        query_url = f"{URL}/user/user_game_dashboard"
        ghi_log(ten_tai_khoan, f"Đang lấy token từ {query_url}", level='info')
        async with aiohttp.ClientSession() as session:
            async with session.get(query_url, timeout=10) as response:
                dataP = await response.text()
                script_regex = re.compile(r'<script\b[^>]*>(.*?)<\/script>', re.DOTALL)
                match_script = script_regex.search(dataP)
                if match_script:
                    script_content = match_script.group(1)
                    ghi_log(ten_tai_khoan, f"Nội dung <script> đầu tiên: {script_content}", level='info')
                else:
                    ghi_log(ten_tai_khoan, "Không tìm thấy block <script>", level='warning')
                #ghi_log(ten_tai_khoan, f"Kết quả lấy token: {dataP}", level='info')
                regex = re.compile(r"token_character\s*=\s*'([^']+)'")
       
                match = regex.search(dataP)
                ghi_log(ten_tai_khoan, f"Kết quả lấy token: {match}", level='info')
                if match and match.group(1):
                    token = match.group(1)
                    # Lưu token vào biến riêng của luồng
                    set_thread_var_text("Token", token)
                    ghi_log(ten_tai_khoan, f"Lấy token thành công: {token}", level='info')
                    return token
        return None
    except Exception as error:
        print(f"Lỗi trong lay_token: {error}")
        return None

async def lay_chapter_token(account_number):
    """
    Lấy chapterToken với token từ lay_token() và ID từ IdIngame của tài khoản.
    
    Args:
        account_number: Giá trị AccountNumber cần tìm (kiểu int hoặc chuỗi có thể chuyển sang int).
    
    Returns:
        str: chapterToken được tạo thành từ token và IdIngame.
    """
    # Lấy thông tin tài khoản
    thong_tin_tai_khoan = lay_thong_tin_tai_khoan(account_number)
    id_ingame = thong_tin_tai_khoan.get("IdIngame")
    ten_tai_khoan = thong_tin_tai_khoan.get("TênTàiKhoản", "Hệ thống")
    if not id_ingame:
        raise ValueError(f"Không tìm thấy IdIngame cho tài khoản với AccountNumber = {account_number}")
    
    # Lấy token
    token = await lay_token(account_number)
    
    # Tạo chapterToken
    chapter_token = f"{token}&player={id_ingame}"
    ghi_log(ten_tai_khoan, f"ChapterToken: {chapter_token}", level='info')
    # Lưu chapterToken vào biến riêng của luồng
    set_thread_var_text("ChapterToken", chapter_token)
    
    return chapter_token

# Ví dụ sử dụng hàm lay_token
if __name__ == "__main__":
    try:
        gia_tri_token = asyncio.run(lay_token())
        print("Token:", gia_tri_token)
    except Exception as loi:
        print("Lỗi:", loi)