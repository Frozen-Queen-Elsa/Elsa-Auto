# Thêm hàm ghi_log mới vào file GhiLog.py
import logging
import os
import time
from datetime import datetime

# Đường dẫn tới file log
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, '../Logs/logs.txt')
exception_log_file_path = os.path.join(current_dir, '../Logs/exceptions_logs.txt')

# Reset lại file log khi bắt đầu project
with open(log_file_path, 'w', encoding='utf-8') as file:
    current_time = datetime.now().strftime("%A %d-%m-%Y %H:%M:%S")
    file.write(f"Thứ {current_time}\n\n\n")

# Reset lại file exception log khi bắt đầu project
with open(exception_log_file_path, 'w', encoding='utf-8') as file:
    current_time = datetime.now().strftime("%A %d-%m-%Y %H:%M:%S")
    file.write(f"Thứ {current_time}\n\n\n")

# Cấu hình logging để ghi lại các lỗi vào file log và console
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Chỉ ghi log từ mức INFO trở lên

file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(' %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Formatter cho console với màu sắc
class ConsoleFormatter(logging.Formatter):
    def format(self, record):
        log_style = {
            'DEBUG': LogStyle.CYAN,
            'INFO': LogStyle.GREEN,
            'WARNING': LogStyle.YELLOW,
            'ERROR': LogStyle.RED,
            'CRITICAL': LogStyle.BOLD + LogStyle.RED
        }
        style = log_style.get(record.levelname, LogStyle.RESET)
        record.msg = f"{style}{record.msg}{LogStyle.RESET}"
        return super().format(record)

console_formatter = ConsoleFormatter(' %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ANSI escape codes cho định dạng text
class LogStyle:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    RED = "\033[31m"
    ERROR = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

def log_message(message, level='info', style=None):
    """
    Ghi log với các tùy chọn về màu sắc và kiểu chữ.
    :param message: Nội dung log
    :param level: Mức độ log ('debug', 'info', 'warning', 'error', 'critical')
    :param style: Kiểu chữ (LogStyle)
    """
    if style:
        message = f"{style}{message}{LogStyle.RESET}"
    
    if level == 'debug':
        logger.debug(message)
    elif level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)
        # Ghi log lỗi vào exceptions_logs.txt
        current_time = datetime.now().strftime("%A %d-%m-%Y %H:%M:%S")
        with open(exception_log_file_path, 'a', encoding='utf-8') as file:
            file.write(f"{current_time} : {message}\n")
    elif level == 'critical':
        logger.critical(message)
    else:
        logger.info(message)

def ghi_log(ten_tk, noi_dung, level='info', style=LogStyle.GREEN):
    """
    Ghi log với cấu trúc: Ngày/Tháng/năm Giờ-Phút-Giây : Tài Khoản {tên tài khoản} - nội dung log
    """
    thoi_gian = time.strftime("%d/%m/%Y %H-%M-%S")
    thong_bao = f"{thoi_gian} : Tài Khoản {ten_tk} - {noi_dung}"
    log_message(thong_bao, level=level, style=style)