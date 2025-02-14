import aiohttp
import asyncio
import json
import time
import random

from Data.DataMoiTaiKhoan import lay_url_web,lay_thong_tin_tai_khoan,lay_refer_link,get_thread_var_int,set_thread_var_int,get_thread_var,set_thread_var,set_delay_lum,check_delay_lum,get_thread_var_text,set_thread_var_text,set_thread_var_json

from HamPhuTro.GhiLog import ghi_log, LogStyle
from Auto.Token import lay_chapter_token, lay_token
from Auto.DangNhap import dang_nhap
import datetime

KhuVucConvert = {
    1: "Địa Hải Giới (Tân Thủ)",
    2: "Băng Nguyên Giới",
    3: "Hoả Nguyên Giới",
    4: "Minh Giới",
    5: "Tổ Long Sào",
    6: "Loạn Lôi Đảo"
}

VatPhamConvert = {
    "gold": "Vàng",
    "crystal": "Linh Thạch",
    "guild_ore": "Địa Nguyên Thạch",
    "add_option": "Tinh Luyện Châu",
    "equipment_upgrade": "Huyền Thiết",
    "job_exp_6": "Thông Thạo Quyển Lv6",
    "job_exp_5": "Thông Thạo Quyển Lv5",
    "job_exp_4": "Thông Thạo Quyển Lv4",
    "job_exp_3": "Thông Thạo Quyển Lv3",
    "job_exp_2": "Thông Thạo Quyển Lv2",
    "job_exp_1": "Thông Thạo Quyển Lv1",
    "medicinal_exp_1": "Tăng Ích Đan Lv1",
    "medicinal_exp_2": "Tăng Ích Đan Lv2",
    "medicinal_exp_3": "Tăng Ích Đan Lv3",
    "equipment_upgrade_1": "Thiên Mộc Thạch (Hạ)",
    "equipment_upgrade_2": "Thiên Mộc Thạch (Trung)",
    "equipment_upgrade_3": "Thiên Mộc Thạch (Thượng)",
    "guild_quest_vegetable": "Quân Lương - Nông Sản",
    "guild_quest_ore": "Quân Nhu - Đá",
    "guild_quest_wood": "Quân Nhu - Gỗ",
    "guild_quest_cloth": "Quân Nhu - Vải",
    "guild_quest_seed": "Quân Lương - Hạt Giống",
    "guild_quest_meat": "Quân Lương - Thịt",
    "guild_quest_bar": "Quân Lương - Sắt",
    "guild_quest_fish": "Quân Lương - Cá",
    "medicinal_point_plus": "Tư Chất Đan",
    "medicinal_upgrade_king": "Tam Sinh Quả",
    "event_2023_red": "Bao Lì Xì",
    "egg_rare": "Trứng Hiếm",
    "egg_legendary": "Trúng Huyền Thoại",
    "egg_mystic": "Trứng Thần Thoại",
    "pet_evolve_1": "Sơ cấp Thú Hồn",
    "pet_evolve_2": "Trung cấp Thú Hồn",
    "pet_evolve_3": "Cao cấp Thú Hồn",
    "pet_skill_1": "Thú Kỹ Nhân",
    "pet_skill_2": "Thú Kỹ Địa",
    "pet_skill_3": "Thú Kỹ Thiên",
    "pet_skill_4": "Thú Kỹ Thần",
}




async def check_sua_do(account_number):
    """
    Async: Kiểm tra deteriorate của nhân vật, nếu lớn hơn 0 thì thực hiện sửa đồ.
    URL lấy từ DataMoiTaiKhoan (lay_url_web) và Id lấy từ IdIngame trong tài khoản.
    """
    try:
        URL = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        id_ingame = tai_khoan.get("IdIngame")
        refe_link = lay_refer_link()
        
        query_url = f"{URL}/api/get_data_by_id?table=game_character&data=info,data&id={id_ingame}"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Referer": refe_link,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(query_url, headers=headers, timeout=10) as response:
                res_json = await response.json()
                deteriorate_value = json.loads(res_json.get("data", "{}"))
                so_ben = deteriorate_value.get("deteriorate", 0)
                if so_ben > 0:
                    await sua_do(account_number)
    except Exception as e:
        ghi_log(ten_tai_khoan if 'ten_tai_khoan' in locals() else "Hệ thống",
                f"Lỗi trong check_sua_do: {e}", level="error", style=LogStyle.RED)

async def sua_do(account_number):
    """
    Async: Thực hiện sửa đồ cho nhân vật.
    """
    try:
        URL = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        refe_link = lay_refer_link()
        post_url = f"{URL}/assets/ajax/character.php"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Referer": refe_link,
        }
        payload = {"action": "equipment_repair"}
        async with aiohttp.ClientSession() as session:
            async with session.post(post_url, headers=headers, data=payload, timeout=10) as response:
                res_text = await response.text()
                if "Sửa chửa thành công" in res_text:
                    ghi_log(ten_tai_khoan, "Sửa chửa thành công", level="info", style=LogStyle.GREEN)
    except Exception as e:
        ghi_log(ten_tai_khoan, f"Lỗi trong sua_do: {e}", level="error", style=LogStyle.RED)

async def restore_mau(trinh_duyet,account_number):
    """
    Async: Thực hiện hồi phục trạng thái nếu khu vực khác 1.
    Gọi API POST với body 'action=restore&type=word' và kiểm tra phản hồi.
    """
    try:
        URL = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        cuu_gioi=tai_khoan.get("CửuGiới", {})
        khuvuc = cuu_gioi.get("KhuVực")
        refe_link = lay_refer_link()
        if khuvuc == 1:
            return
        js_code = f"""
        const response = await fetch('{URL}/assets/ajax/battle_map.php', {{
            headers: {{
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Referer": '{refe_link}',
            }},
            method: "POST",
            body: `action=restore&type=word`,
        }});
        const res = await response.text();
        return res;
        """
        res_text= trinh_duyet.execute_script(js_code)
        
        if "Hồi phục thành công" in res_text:
            ghi_log(ten_tai_khoan, "❤️️ Hồi phục thành công ❤️️", level="info", style=LogStyle.GREEN)
    except Exception as e:
        ghi_log(ten_tai_khoan, f"Lỗi trong restore_mau: {e}", level="error", style=LogStyle.RED)

async def check_tai_phu(trinh_duyet,account_number):
    """
    Async: Kiểm tra tài phú của nhân vật và thực hiện hành động tương ứng.
    """
    try:
        URL = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        chapter_token = tai_khoan.get("ChapterToken")

        js_code = f"""
        const response = await fetch('{URL}/api/battle_map_player_data?token_character={chapter_token}&type=word');
        const res = await response.json();
        return res;
        """
        
        res_json = trinh_duyet.execute_script(js_code)
        tai_phu = json.loads(res_json.get("data", "{}"))
        currencies = tai_phu.get("bag", {})
        gold_amount = currencies.get("gold", {}).get("amount", 0)
        crystal_amount = currencies.get("crystal", {}).get("amount", 0)
        total_value = int(tai_phu.get("score", {}).get("rich", 0))
        
        # Check certain currencies to trigger logout
        for currency, details in currencies.items():
            if currency in ['medicinal_point_plus', 'add_option', 'medicinal_upgrade_king', 
                            'egg_legendary', 'egg_rare', 'guild_boss_1', 'guild_boss_2']:
                item_name = VatPhamConvert.get(currency, currency)
                ghi_log(ten_tai_khoan, f"➙ Chạy OUT... (lụm được {item_name})", level="info", style=LogStyle.YELLOW)
                await pre_logout(account_number)
                return
        
        cuu_gioi = tai_khoan.get("CửuGiới", {})    
        TàiPhúOut = cuu_gioi.get("TàiPhúOut", 0)    
        MaxTàiPhú= cuu_gioi.get("MaxTàiPhú", 0)
        ĐiMaxTàiPhú= cuu_gioi.get("ĐiMaxTàiPhú", False)
        NhặtVàng= cuu_gioi.get("NhặtVàng", 0)

        
        
        if total_value >= TàiPhúOut and NhặtVàng :
            if ĐiMaxTàiPhú == 'NO':
                await pre_logout(account_number)
                return
            if ĐiMaxTàiPhú == 'YES' and total_value >= MaxTàiPhú:
                await pre_logout(account_number)
                return              
            set_thread_var("isBlockTaiPhu", True)
            
            currency_details = []
            for currency, details in currencies.items():
                currency_detail = details.get("amount", "Unknown")
                currency_name = VatPhamConvert.get(currency, currency)
                currency_details.append(f"{currency_name}: {currency_detail}")
            combined_details = "\n+ ".join(currency_details)
            ghi_log(ten_tai_khoan, f"😻\n+ {combined_details}\n➙ Tài Phú: {total_value}", level="info", style=LogStyle.GREEN)
            
            
            
        elif total_value >= MaxTàiPhú and not NhặtVàng :
            await pre_logout(account_number)
        else:
            currency_details = [f"{cur}: {det.get('amount', 'Unknown')}" for cur, det in currencies.items()]
            combined_details = "\n+ ".join(currency_details)
            ghi_log(ten_tai_khoan, f"😻\n+ {combined_details}\n➙ Tài Phú: {total_value}",
                    level="info", style=LogStyle.GREEN)
    except Exception as e:
        ghi_log(ten_tai_khoan if 'ten_tai_khoan' in locals() else "Hệ thống",
                f"Lỗi trong check_tai_phu: {e}", level="error", style=LogStyle.RED)

async def pre_logout(account_number):
    """
    Async: Thực hiện các bước trước khi đăng xuất.
    """
    try:
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        ghi_log(ten_tai_khoan, "➙ Chạy OUT...!", level="info", style=LogStyle.YELLOW)
        await out_cuu_gioi(account_number)
    except Exception as e:
        ghi_log(ten_tai_khoan if 'ten_tai_khoan' in locals() else "Hệ thống",
                f"Lỗi trong pre_logout: {e}", level="error", style=LogStyle.RED)

async def out_cuu_gioi(trinh_duyet,account_number):
    """
    Async: Thực hiện hành động out khỏi Cửu Giới.
    """
    try:
        URL = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        cuu_gioi=tai_khoan.get("CửuGiới", {})
        khuvuc = cuu_gioi.get("KhuVực")
        refe_link = lay_refer_link()
        
        js_code = f"""
        const response = await fetch('{URL}/assets/ajax/battle_map.php', {{
            headers: {{
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Referer": '{refe_link}',
            }},
            method: "POST",
            body: `action=word_exit&target=1`,
        }});
        const res = await response.text();
        return res;
        """
        res_text= trinh_duyet.execute_script(js_code)
        if "game_word_history" in res_text:
            khu_vuc_ten = KhuVucConvert.get(khuvuc, "Khu vực không xác định")
            ghi_log(ten_tai_khoan, f"➙ Out thành công khỏi khu vực {khu_vuc_ten}..",
                    level="info", style=LogStyle.GREEN)
            set_thread_var("isLogCuuGioi",False)
                # Reload trang
            ghi_log(ten_tai_khoan, "Reloading trang...", level="info", style=LogStyle.BLUE)
            await trinh_duyet.refresh()
    except Exception as e:
        ghi_log(ten_tai_khoan, f"Lỗi trong out_cuu_gioi: {e}", level="error", style=LogStyle.RED)





async def thong_tin_nhan_vat(trinh_duyet, account_number):
    """
    Async: Lấy thông tin nhân vật từ API.
    """
    try:
        URL = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        # Lấy chapter token từ thread variable (đã được set từ khi đăng nhập)
        chapter_token = get_thread_var_text("ChapterToken")
        id_ingame = tai_khoan.get("IdIngame")
        api_url = f"{URL}/api/battle_map_player_data?token_character={chapter_token}&type=word"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Referer": lay_refer_link(),
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers, timeout=10) as response:
                try:
                    data = await response.json()
                except Exception as e:
                    ghi_log("Hệ thống", f"Lỗi parse JSON: {e}", level="error", style=LogStyle.RED)
                    data = {}
                ghi_log("Hệ thống", f"Thong tin nhan vat: {data}", level="info", style=LogStyle.GREEN)
                set_thread_var_json(f"thong_tin_nhan_vat_{account_number}", data)
                return data
    except Exception as e:
        ghi_log(ten_tai_khoan, f"Lỗi trong thong_tin_nhan_vat: {e}", level="error", style=LogStyle.RED)
        return None

async def thong_tin_vi_tri(trinh_duyet, account_number):
    """
    Async: Lấy thông tin vị trí từ API.
    """
    try:
        URL = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        chapter_token = get_thread_var_text("ChapterToken")
        id_ingame = tai_khoan.get("IdIngame")
        api_url = f"{URL}/api/battle_map_position_data?token_character={chapter_token}&type=word"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Referer": lay_refer_link(),
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers, timeout=10) as response:
                try:
                    data = await response.json()
                except Exception as e:
                    ghi_log("Hệ thống", f"Lỗi parse JSON: {e}", level="error", style=LogStyle.RED)
                    data = {}
                ghi_log("Hệ thống", f"Thong tin vi tri: {data}", level="info", style=LogStyle.GREEN)
                set_thread_var_json(f"thong_tin_vi_tri_{account_number}", data)
                return data
    except Exception as e:
        ghi_log(ten_tai_khoan, f"Lỗi trong thong_tin_vi_tri: {e}", level="error", style=LogStyle.RED)
        return [0] * 8
    
async def thong_tin_xung_quanh(trinh_duyet, account_number):
    """
    Async: Lấy thông tin xung quanh từ API và thực hiện hành động dựa trên dữ liệu.
    """
    try:
        tai_khoan= lay_thong_tin_tai_khoan(account_number)
        cuu_gioi= tai_khoan.get("CửuGiới", {})
        khu_vuc=cuu_gioi.get("KhuVực")
        gap_shipper=cuu_gioi.get("GặpShipper")
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        id_ingame = tai_khoan.get("IdIngame",0)
        
        delay_lum = check_delay_lum(account_number)
        is_block_tai_phu = get_thread_var("isBlockTaiPhu")
        guild_quest = get_thread_var("guildQuest")
        count_lum = get_thread_var_int("countLuomCuuGioi")        
       
      
        data = await thong_tin_vi_tri(trinh_duyet, account_number)    
        vitri = {}  # Dictionary lưu thông tin vị trí cho các id_ingame
        
        # Tạo dictionary cho id_ingame nếu chưa tồn tại
        
        vitri[id_ingame] = {}
        """
        vitri[id_ingame]=
        {
        "position1": "player:10",
        "position2": "gold:20",
        "position3": "itemname:5",
        ...
        }
        """
        for idx, item in enumerate(data, start=1):
            json_data = json.loads(item.get("data", "{}"))
            target = json_data.get("target")
            position_key = f"position{idx}"
            item_position = int(item.get("position", 0))
            
            if target == 'player':
                value = f"player:{item_position}"
            elif json_data.get("target_data"):
                sign = json_data["target_data"].get("sign", "")
                value = f"{sign}:{item_position}"
            else:
                value = f"none:{item_position}"
            
            vitri[id_ingame][position_key] = value
        return vitri[id_ingame]
    except Exception as e:
        ghi_log(ten_tai_khoan, f"Lỗi trong thong_tin_xung_quanh: {e}", level="error", style=LogStyle.RED)


   
            
def get_random_index(goc_chay):
    ranges = {
        1: [1, 2, 4],
        2: [2, 3, 5],
        3: [4, 6, 7],
        4: [5, 7, 8]
    }

    if goc_chay in ranges:
        return random.choice(ranges[goc_chay])
    return None


async def lay_thong_tin(data, ke_dich, data_p, *positions):
    vitrime = ''
    is_num=get_thread_var("isNumCuuGioi")
    if len(data) == 8:
        if int(ke_dich) in positions[:3]:
            vitrime = '8canhTren'
        elif int(ke_dich) in positions[4:]:
            vitrime = '8canhPhai'
        elif int(ke_dich) in positions[5:7]:
            vitrime = '8canhDuoi'
        elif int(ke_dich) == positions[3]:
            vitrime = '8canhTrai'
    elif len(data) == 5:
        if int(data_p['position']) > positions[0] and int(data_p['position']) < positions[1] and int(data_p['position']) < positions[2] and int(data_p['position']) < positions[3] and int(data_p['position']) < positions[4] and is_num != True:
            if int(ke_dich) == positions[0] or int(ke_dich) == positions[2]:
                vitrime = '5canhTrenTrai'
            if int(ke_dich) == positions[1] or int(ke_dich) == positions[4]:
                vitrime = '5canhTrenPhai'
            if int(ke_dich) == positions[3]:
                vitrime = '5canhTrenDuoi'
        if int(data_p['position']) > positions[0] and int(data_p['position']) > positions[1] and int(data_p['position']) > positions[2] and int(data_p['position']) < positions[3] and int(data_p['position']) < positions[4] and is_num != True:
            if int(ke_dich) == positions[0] or int(ke_dich) == positions[1]:
                vitrime = '5canhPhaiTren'
            if int(ke_dich) == positions[3] or int(ke_dich) == positions[4]:
                vitrime = '5canhPhaiDuoi'
            if int(ke_dich) == positions[2]:
                vitrime = '5canhPhaiTrai'
        if int(data_p['position']) > positions[0] and int(data_p['position']) > positions[1] and int(data_p['position']) < positions[2] and int(data_p['position']) < positions[3] and int(data_p['position']) < positions[4] and is_num != True:
            if int(ke_dich) == positions[0] or int(ke_dich) == positions[1]:
                vitrime = '5canhTraiTren'
            if int(ke_dich) == positions[3] or int(ke_dich) == positions[4]:
                vitrime = '5canhTraiDuoi'
            if int(ke_dich) == positions[2]:
                vitrime = '5canhTraiPhai'
        if int(data_p['position']) > positions[0] and int(data_p['position']) > positions[1] and int(data_p['position']) > positions[2] and int(data_p['position']) > positions[3] and int(data_p['position']) < positions[4] and is_num != True:
            if int(ke_dich) == positions[0] or int(ke_dich) == positions[3]:
                vitrime = '5canhDuoiTrai'
            if int(ke_dich) == positions[2] or int(ke_dich) == positions[4]:
                vitrime = '5canhDuoiPhai'
            if int(ke_dich) == positions[1]:
                vitrime = '5canhDuoiTren'
    return vitrime

