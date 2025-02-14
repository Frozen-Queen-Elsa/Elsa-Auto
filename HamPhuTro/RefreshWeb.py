
from selenium.webdriver.common.by import By
import time
from Data.DataMoiTaiKhoan import lay_thong_tin_tai_khoan
from HamPhuTro.GhiLog import ghi_log


def checkAndReload(trinh_duyet,account_number):
    time.sleep(10)
    items_to_check = ["Chức năng", "Nhân Vật", "Kỹ Năng", "Túi Đồ", "Nghề"]
    tai_khoan = lay_thong_tin_tai_khoan(account_number)
    ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Không xác định")
    for item_text in items_to_check:
        elements = trinh_duyet.find_elements(By.TAG_NAME, "p")
        found = any(item_text in element.text for element in elements)

        try:
            battle_map_area = trinh_duyet.find_element(By.CSS_SELECTOR, ".user_game_module.battle_map.area")
        except Exception:
            battle_map_area = None

        if not found and battle_map_area is None:
            trinh_duyet.refresh()
            ghi_log(ten_tai_khoan, f"Không phải trang Cửu Giới, tải lại trang", level='info')
            from Auto.CuuGioi import vao_trang_cuu_gioi
            vao_trang_cuu_gioi(trinh_duyet,account_number)
            ghi_log(ten_tai_khoan, f"Đã tải lại trang Cửu Giới", level='info')
            return
        
def reload_by_ajax(trinh_duyet, duong_dan_xpath,account_number):
    tai_khoan = lay_thong_tin_tai_khoan(account_number)
    ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Không xác định")
    script = """
    var duong_dan_xpath = arguments[0];
    var phan_tu = document.evaluate(duong_dan_xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    if(phan_tu){
        var url = window.location.href;
        if(window.jQuery){
            $(phan_tu).load(url + ' ' + duong_dan_xpath);
        } else {
            console.log("jQuery không khả dụng trên trang này.");
        }
    }
    """
    ghi_log(ten_tai_khoan, f"Tải lại trang bằng AJAX", level='info')
    trinh_duyet.execute_script(script, duong_dan_xpath)
    
def auto_check_and_reload(trinh_duyet, interval_seconds,account_number):
    while True:
        checkAndReload(trinh_duyet,account_number)
        time.sleep(interval_seconds)

def auto_reload_by_ajax(trinh_duyet, duong_dan_xpath, interval_seconds,account_number):
    while True:
        reload_by_ajax(trinh_duyet, duong_dan_xpath,account_number)
        time.sleep(interval_seconds)

def reLoad(trinh_duyet):
    trinh_duyet.refresh()