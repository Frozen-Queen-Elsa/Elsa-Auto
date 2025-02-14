from HamPhuTro.GhiLog import log_message, LogStyle

def handle_exception(e):
    """
    Hàm xử lý ngoại lệ, ghi lại lỗi vào file log và in ra màn hình.
    """
    error_message = f"Đã xảy ra lỗi: {e}"
    log_message(error_message, level='error', style=LogStyle.RED)
    #print(error_message)