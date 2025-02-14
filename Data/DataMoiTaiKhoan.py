# Sử dụng biến riêng của luồng để lưu cấu hình đã load từ file setting.json
import json
import asyncio
import os
import threading

bien_rieng_cau_hinh = threading.local()

def get_delay_lum():
    """
    Lấy ra dictionary delayLum riêng của luồng từ bien_rieng_cau_hinh.
    Nếu chưa tồn tại, khởi tạo nó là dictionary rỗng.
    """
    if not hasattr(bien_rieng_cau_hinh, "delayLum"):
        bien_rieng_cau_hinh.delayLum = {}
    return bien_rieng_cau_hinh.delayLum

def set_delay_lum(ID, delay):
    """
    Cập nhật delay cho một ID cụ thể trong cấu hình của luồng hiện tại.
    
    ID: Khóa định danh riêng cho phần tử.
    delay: Khoảng thời gian delay (tính bằng giây).
    
    Hàm sử dụng asyncio.get_event_loop().time() để lấy thời gian hiện tại,
    sau đó cộng thêm delay và lưu kết quả vào dictionary delayLum riêng của luồng.
    """
    delay_lum = get_delay_lum()
    delay_lum[ID] = asyncio.get_event_loop().time() + delay

def check_delay_lum(ID):
    """
    Kiểm tra xem delay của ID cụ thể trong cấu hình của luồng hiện tại còn hiệu lực không.
    
    Nếu thời gian lưu trong delayLum cho ID này lớn hơn thời gian hiện tại,
    trả về True (delay còn hiệu lực); ngược lại, trả về False.
    """
    delay_lum = get_delay_lum()
    return delay_lum.get(ID, 0) > asyncio.get_event_loop().time()


def get_thread_var(var_name, default=False):
    """
    Lấy giá trị của biến thread-local với tên var_name.
    Nếu biến không tồn tại, trả về default (mặc định là False).

    Ví dụ:
        value = get_thread_var("isBlockedCuuGioi")
        value = get_thread_var("isBlockTaiPhu")
        value = get_thread_var("isLogCuuGioi")
        value = get_thread_var("isNumCuuGioi")
    """
    return getattr(bien_rieng_cau_hinh, var_name, default)

def get_thread_var_json(var_name, default=None):
    """
    Lấy giá trị của biến thread-local được lưu dưới dạng JSON.
    Nếu biến không tồn tại hoặc không thể giải mã được, trả về đối tượng default (mặc định là {}).

    Args:
        var_name (str): Tên biến.
        default (Any, optional): Giá trị trả về nếu biến không tồn tại hoặc lỗi giải mã.
                                 Mặc định là {}.
    
    Returns:
        object: Đối tượng được giải mã từ JSON.
    """
    import json
    value = getattr(bien_rieng_cau_hinh, var_name, None)
    if value is None:
        return {} if default is None else default
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return {} if default is None else default
    # Nếu không phải chuỗi, trả về giá trị nguyên thủy
    return value

def set_thread_var_json(var_name, value):
    """
    Cập nhật giá trị cho biến thread-local dưới dạng JSON.
    Giá trị value sẽ được chuyển thành chuỗi JSON trước khi lưu.

    Args:
        var_name (str): Tên biến cần cập nhật.
        value (Any): Giá trị cần lưu, phải có thể chuyển thành JSON.
    """
    import json
    try:
        json_value = json.dumps(value)
    except Exception as e:
        json_value = "{}"
    setattr(bien_rieng_cau_hinh, var_name, json_value)

def set_thread_var(var_name, value):
    """
    Cập nhật giá trị cho biến thread-local với tên var_name.

    Ví dụ:
        set_thread_var("isBlockedCuuGioi", True)      # Thiết lập isBlockedCuuGioi thành True
        set_thread_var("isBlockTaiPhu", False)         # Thiết lập isBlockTaiPhu thành False
        set_thread_var("isLogCuuGioi", True)           # Thiết lập isLogCuuGioi thành True
        set_thread_var("isNumCuuGioi", True)            # Thiết lập isNumCuuGioi thành True
    """
    setattr(bien_rieng_cau_hinh, var_name, value)

def get_thread_var_text(var_name, default=""):
    """
    Lấy giá trị của biến thread-local với tên var_name.
    Nếu biến không tồn tại, trả về default (mặc định là False).

    Ví dụ:
        
        value = get_thread_var("isReturnCuuGioi")
        
    """
    return getattr(bien_rieng_cau_hinh, var_name, default)


def set_thread_var_text(var_name, value):
    """
    Cập nhật giá trị cho biến thread-local với tên var_name.

    Ví dụ:
        
        set_thread_var("isReturnCuuGioi", "goctrentrai")         # Thiết lập isReturnCuuGioi thành False
        
    """
    setattr(bien_rieng_cau_hinh, var_name, value)

def get_thread_var_int(var_name, default=0):
    """
    Lấy giá trị của biến thread-local với tên var_name và ép kiểu về int.
    Nếu biến không tồn tại, trả về default (mặc định 0).

    Ví dụ:
        countLuomCuuGioi = get_thread_var_int("countLuomCuuGioi")    # Lấy giá trị của countLuomCuuGioi dưới dạng int
        countPkCuuGioi = get_thread_var_int("countPkCuuGioi")          # Lấy giá trị của countPkCuuGioi dưới dạng int
    """
    return int(getattr(bien_rieng_cau_hinh, var_name, default))

def set_thread_var_int(var_name, value):
    """
    Cập nhật giá trị cho biến thread-local với tên var_name với giá trị kiểu int.

    Ví dụ:
        set_thread_var_int("countLuomCuuGioi", 1)      # Thiết lập countLuomCuuGioi thành 1
        set_thread_var_int("countPkCuuGioi", 0)           # Thiết lập countPkCuuGioi thành 0 
    """
    setattr(bien_rieng_cau_hinh, var_name, int(value))

def tai_cau_hinh():
    """
    Tải cấu hình từ file setting.json vào biến riêng của luồng (chỉ chạy 1 lần cho mỗi luồng).
    
    Returns:
        dict: Cấu hình từ file setting.json.
    """
    if not hasattr(bien_rieng_cau_hinh, "cau_hinh"):
        duong_dan_setting = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setting.json")
        with open(duong_dan_setting, "r", encoding="utf-8") as f:
            bien_rieng_cau_hinh.cau_hinh = json.load(f)
    return bien_rieng_cau_hinh.cau_hinh

def lay_so_account():
    """
    Lấy số account từ cấu hình đã được load.
    
    Returns:
        int: Giá trị của SốAccount.
    
    Raises:
        ValueError: Nếu SốAccount không được cấu hình trong setting.json.
    """
    cau_hinh = tai_cau_hinh()
    so_account = cau_hinh.get("SốAccount")
    if so_account is None:
        raise ValueError("SốAccount không được cấu hình trong setting.json")
    return so_account

def lay_url_web():
    """
    Lấy giá trị của UrlWeb từ cấu hình đã được tải.
    
    Returns:
        str: Giá trị của UrlWeb, không có dấu "/" ở cuối.
    
    Raises:
        ValueError: Nếu UrlWeb không được cấu hình.
    """
    cau_hinh = tai_cau_hinh()
    url_web = cau_hinh.get("UrlWeb", "").strip()
    if not url_web:
        raise ValueError("UrlWeb không được cấu hình trong setting.json")
    if url_web.endswith("/"):
        url_web = url_web[:-1]
    return url_web

def lay_refer_link():
    """
    Lấy referer link dựa trên URLWeb cấu hình, trả về dạng: {URLWeb}/user/user_game_dashboard.
    """
    URLWeb = lay_url_web()
    return f"{URLWeb}/user/user_game_dashboard"

def lay_thong_tin_tai_khoan(account_number):
    """
    Lấy thông tin của tài khoản có AccountNumber bằng account_number từ cấu hình đã được tải.
    
    Args:
        account_number: Số AccountNumber cần tìm.
    
    Returns:
        dict: Thông tin tài khoản nếu tìm thấy, ngược lại raise Exception.
    """
    cau_hinh = tai_cau_hinh()
    danh_sach_tai_khoan = cau_hinh.get("Accounts", [])
    tai_khoan = next((acc for acc in danh_sach_tai_khoan if acc.get("AccountNumber") == account_number), None)
    if not tai_khoan:
        raise ValueError(f"Không tìm thấy tài khoản với AccountNumber = {account_number}")
    return tai_khoan

def in_thong_tin_tai_khoan(account_number):
    """
    In ra giá trị của từng biến (key) trong tài khoản được chọn.
    """
    tai_khoan = lay_thong_tin_tai_khoan(account_number)
    
    print("AccountNumber:", tai_khoan.get("AccountNumber"))
    print("IdIngame:", tai_khoan.get("IdIngame"))
    print("TênTàiKhoản:", tai_khoan.get("TênTàiKhoản"))
    print("IdLogin:", tai_khoan.get("IdLogin"))
    print("Password:", tai_khoan.get("Password"))
    
    than_ma = tai_khoan.get("ThầnMa", {})
    print("ThầnMa:", than_ma)
    
    cuu_gioi = tai_khoan.get("CửuGiới", {})
    print("CửuGiới:", cuu_gioi)
    
    tong_mon_chien = tai_khoan.get("TôngMônChiến", {})
    print("TôngMônChiến:", tong_mon_chien)
    
    doc_truyen = tai_khoan.get("ĐọcTruyện", {})
    print("ĐọcTruyện -> ĐọcTruyện:", doc_truyen.get("ĐọcTruyện"))
    print("ĐọcTruyện -> LinkTruyện:", doc_truyen.get("LinkTruyen"))
    
    thanh_chien = tai_khoan.get("ThánhChiến", {})
    print("ThánhChiến:", thanh_chien)
    
    hang_ngay = tai_khoan.get("HằngNgày", {})
    print("HằngNgày:", hang_ngay)
    
    event = tai_khoan.get("Event", {})
    print("Event:", event)

if __name__ == "__main__":
    try:
        so_account = 1
        print("Thông tin tài khoản:")
        in_thong_tin_tai_khoan(so_account)
        print("\nUrlWeb từ setting.json:", lay_url_web())
    except Exception as loi:
        print("Lỗi:", loi)