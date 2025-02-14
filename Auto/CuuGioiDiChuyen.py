import aiohttp
import asyncio
import json
import time
import random
from selenium.webdriver.common.by import By
import asyncio
from Data.DataMoiTaiKhoan import (
    lay_url_web,
    lay_thong_tin_tai_khoan,
    lay_refer_link,
    get_thread_var_int,
    set_thread_var_int,
    get_thread_var,
    set_thread_var,
    set_delay_lum,
    check_delay_lum,
    get_thread_var_text,
    set_thread_var_text,
    get_thread_var_json,
    set_thread_var_json
)
from HamPhuTro.GhiLog import ghi_log, LogStyle
from Auto.Token import lay_chapter_token, lay_token
from Auto.DangNhap import dang_nhap
from Auto.CuuGioiHelper import get_random_index,thong_tin_xung_quanh,lay_thong_tin

import datetime


async def di_chuyen_cuu_gioi(trinh_duyet, account_number):
    tai_khoan = lay_thong_tin_tai_khoan(account_number)
    ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
    id_ingame = tai_khoan.get("IdIngame")
    cuu_gioi = tai_khoan.get("CửuGiới", {})

    goc_chay=cuu_gioi.get("GócChạy")

    
    dataP = get_thread_var(f"thong_tin_nhan_vat_{account_number}")
    data = get_thread_var(f"thong_tin_vi_tri_{account_number}")
    ghi_log(ten_tai_khoan, f"🔍 Đang xử lý vị trí", level="info", style=LogStyle.YELLOW)
    try:
        is_return = get_thread_var("isReturn")
        is_num = get_thread_var("isNumCuuGioi")

        positions = [int(data.get(f"position{i}", 0)) for i in range(1, 9)]
        position1, position2, position3, position4, position5, position6, position7, position8 = positions

        if len(data) == 3:
            if int(dataP['position']) < position1 and dataP['position'] < position2 and dataP['position'] < position3 and is_num != 'true':
                set_thread_var("isReturn", 'gocTrenTrai')
                set_thread_var("isNumCuuGioi", 'true')
            elif int(dataP['position']) > position1 and dataP['position'] < position2 and dataP['position'] < position3 and is_num != 'true':
                set_thread_var("isReturn", 'gocTrenPhai')
                set_thread_var("isNumCuuGioi", 'true')
            elif int(dataP['position']) > position1 and dataP['position'] > position2 and dataP['position'] < position3 and is_num != 'true':
                set_thread_var("isReturn", 'gocDuoiTrai')
                set_thread_var("isNumCuuGioi", 'true')
            elif int(dataP['position']) > position1 and dataP['position'] > position2 and dataP['position'] > position3 and is_num != 'true':
                set_thread_var("isReturn", 'gocDuoiPhai')
                set_thread_var("isNumCuuGioi", 'true')

        elif len(data) == 5:
            if int(dataP['position']) > position1 and dataP['position'] < position2 and dataP['position'] < position3 and dataP['position'] < position4 and dataP['position'] < position5 and is_num != 'true':
                set_thread_var("isReturn", 'canhTren')
                set_thread_var("isNumCuuGioi", 'true')
            elif int(dataP['position']) > position1 and dataP['position'] > position2 and dataP['position'] > position3 and dataP['position'] < position4 and dataP['position'] < position5 and is_num != 'true':
                set_thread_var("isReturn", 'canhPhai')
                set_thread_var("isNumCuuGioi", 'true')
            elif int(dataP['position']) > position1 and dataP['position'] > position2 and dataP['position'] < position3 and dataP['position'] < position4 and dataP['position'] < position5 and is_num != 'true':
                set_thread_var("isReturn", 'canhTrai')
                set_thread_var("isNumCuuGioi", 'true')
            elif int(dataP['position']) > position1 and dataP['position'] > position2 and dataP['position'] > position3 and dataP['position'] > position4 and dataP['position'] < position5 and is_num != 'true':
                set_thread_var("isReturn", 'canhDuoi')
                set_thread_var("isNumCuuGioi", 'true')

        if is_return == 'gocTrenTrai':
            if is_num == 'true':
                random_index = random.choice([3, 3])
                selected_position = positions[random_index - 1]
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')
                return
            else:
                random_index = random.choice([0, 1, 5, 7, 8])
                selected_position = positions[random_index - 1]
                if selected_position == 0:
                    set_thread_var("isNumCuuGioi", 'true')
                    return
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')

        elif is_return == 'gocTrenPhai':
            if is_num == 'true':
                random_index = random.choice([2, 2])
                selected_position = positions[random_index - 1]
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')
                return
            else:
                random_index = random.choice([0, 1, 4, 6, 7])
                selected_position = positions[random_index - 1]
                if selected_position == 0:
                    set_thread_var("isNumCuuGioi", 'true')
                    return
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')

        elif is_return == 'gocDuoiTrai':
            if is_num == 'true':
                random_index = random.choice([2, 2])
                selected_position = positions[random_index - 1]
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')
                return
            else:
                random_index = random.choice([0, 1, 2, 3, 5])
                selected_position = positions[random_index - 1]
                if selected_position == 0:
                    set_thread_var("isNumCuuGioi", 'true')
                    return
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')

        elif is_return == 'gocDuoiPhai':
            if is_num == 'true':
                random_index = random.choice([1, 1])
                selected_position = positions[random_index - 1]
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')
                return
            else:
                random_index = random.choice([0, 1, 1, 2, 4])
                selected_position = positions[random_index - 1]
                if selected_position == 0:
                    set_thread_var("isNumCuuGioi", 'true')
                    return
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')

        elif is_return == 'canhTren':
            if is_num == 'true':
                random_index = random.choice([0, 1, 3, 4, 5])
                selected_position = positions[random_index - 1]
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')
                return
            else:
                random_index = random.choice([0, 1, 6, 7, 8])
                selected_position = positions[random_index - 1]
                if selected_position == 0:
                    set_thread_var("isNumCuuGioi", 'true')
                    return
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')

        elif is_return == 'canhDuoi':
            if is_num == 'true':
                random_index = random.choice([0, 1, 1, 2, 3])
                selected_position = positions[random_index - 1]
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')
                return
            else:
                random_index = random.choice([0, 1, 1, 2, 3])
                selected_position = positions[random_index - 1]
                if selected_position == 0:
                    set_thread_var("isNumCuuGioi", 'true')
                    return
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')

        elif is_return == 'canhPhai':
            if is_num == 'true':
                random_index = random.choice([0, 1, 1, 3, 4])
                selected_position = positions[random_index - 1]
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')
                return
            else:
                random_index = random.choice([0, 1, 1, 4, 6])
                selected_position = positions[random_index - 1]
                if selected_position == 0:
                    set_thread_var("isNumCuuGioi", 'true')
                    return
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')

        elif is_return == 'canhTrai':
            if is_num == 'true':
                random_index = random.choice([0, 1, 2, 3, 5])
                selected_position = positions[random_index - 1]
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')
                return
            else:
                random_index = random.choice([0, 1, 3, 5, 8])
                selected_position = positions[random_index - 1]
                if selected_position == 0:
                    set_thread_var("isNumCuuGioi", 'true')
                    return
                trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()
                set_thread_var("isNumCuuGioi", 'false')

        else:
            random_index = get_random_index(goc_chay)
            selected_position = positions[random_index]
            trinh_duyet.find_element(By.ID, f'battle_position_{selected_position}').click()

    except Exception as e:
        ghi_log(ten_tai_khoan, f"Lỗi trong di_chuyen_cuu_gioi: {e}", level="error", style=LogStyle.RED)
        count_error = get_thread_var_int("countError")
        count_error += 1
        set_thread_var_int("countError", count_error)
        
        if 20 <= count_error < 22:
            from Auto.CuuGioi import log_cuu_gioi
            await log_cuu_gioi(trinh_duyet, account_number)
            lay_token(account_number)
        elif count_error >= 25:
            await trinh_duyet.refresh()

async def xu_ly_vi_tri(trinh_duyet, account_number):
    """
    Async: Xử lý vị trí và đếm số lượng các loại giá trị.
    """
    URL = lay_url_web()
    tai_khoan = lay_thong_tin_tai_khoan(account_number)
    ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
    id_ingame = tai_khoan.get("IdIngame")
    cuu_gioi = tai_khoan.get("CửuGiới", {})
    khu_vuc = cuu_gioi.get("KhuVực")
    gap_shipper = cuu_gioi.get("GặpShipper")
    guild_quest = get_thread_var_int("guildQuest")
    is_block_tai_phu = get_thread_var("isBlockTaiPhu")
    delay_lum = check_delay_lum(account_number)
    
    chapter_token = get_thread_var_text("ChapterToken","")
    count_lum = get_thread_var_int("countLuomCuuGioi")  
    
    
    dataP=get_thread_var_json(f"thong_tin_nhan_vat_{account_number}")
    ghi_log(ten_tai_khoan,f"Thông tin nhân vật {dataP}",level="info",style=LogStyle.GREEN)
    data=get_thread_var_json(f"thong_tin_vi_tri_{account_number}")
    ghi_log(ten_tai_khoan,f"Thông tin vị trí {data}",level="info",style=LogStyle.GREEN)

    
    try:
        thong_tin = await thong_tin_xung_quanh(trinh_duyet, account_number)
        player_count = 0
        gold_count = 0
        none_count = 0
        other_count = 0
        guild_quest_count = 0
        total_count = 0

        player_positions = []
        gold_positions = []
        none_positions = []
        other_positions = []
        guild_quest_positions = []
        total_positions = []

        for key, value in thong_tin.items():
            position = key.replace("position", "")
            total_count += 1
            total_positions.append(position)
            if "player" in value:
                player_count += 1
                player_positions.append(position)
            elif "gold" in value:
                gold_count += 1
                gold_positions.append(position)
            elif "none" in value:
                none_count += 1
                none_positions.append(position)
            elif "guild_quest" in value and int(position) == int(guild_quest):
                guild_quest_count += 1
                guild_quest_positions.append(position)
            else:
                other_count += 1
                other_positions.append(position)

        if player_positions:
            ghi_log(ten_tai_khoan, f"Phát hiện Shipper ở các vị trí: {', '.join(player_positions)}", level="info", style=LogStyle.GREEN)
            if khu_vuc > 1:
                if gap_shipper == 0:                    
                    pass
                elif gap_shipper == 1:
                    # Đấm vỡ mồm shipper
                    item_position = random.choice(player_positions)
                    trinh_duyet.find_element_by_id(f'battle_position_{item_position}').click()
                    ghi_log(ten_tai_khoan, f"Đấm vỡ mồm Shipper tại [{item_position}]", level="info", style=LogStyle.GREEN)
                    return
                elif gap_shipper == 2:
                    # Né không đánh nhau
                    ghi_log(ten_tai_khoan, f"☞ Phát hiện Shipper tại [{item_position}] (bỏ qua)", level="info", style=LogStyle.YELLOW)
                    available_positions = [i for i in range(1, 9) if i != item_position]
                    random_index = random.choice(available_positions)
                    trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    
                    vi_tri_me = await lay_thong_tin(data, item_position, dataP, *total_positions)
                    ghi_log(ten_tai_khoan, f" ➙ ⚠️⚠️⚠️ {vi_tri_me}", level="info", style=LogStyle.YELLOW)

                    if vi_tri_me == '8canhTren':
                        random_index = random.choice([6, 7, 8])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '8canhPhai':
                        random_index = random.choice([1, 4, 6])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '8canhDuoi':
                        random_index = random.choice([1, 2, 3])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '8canhTrai':
                        random_index = random.choice([3, 5, 8])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhTrenTrai':
                        random_index = random.choice([2, 5])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhTrenPhai':
                        random_index = random.choice([1, 3])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhTrenDuoi':
                        random_index = random.choice([1, 2])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhPhaiTren':
                        random_index = random.choice([4, 5])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhPhaiDuoi':
                        random_index = random.choice([1, 2])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhPhaiTrai':
                        random_index = random.choice([1, 5])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhTraiTren':
                        random_index = random.choice([4, 5])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhTraiDuoi':
                        random_index = random.choice([1, 2])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhTraiPhai':
                        random_index = random.choice([1, 4])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhDuoiTrai':
                        random_index = random.choice([3, 5])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhDuoiPhai':
                        random_index = random.choice([1, 4])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                    elif vi_tri_me == '5canhDuoiTren':
                        random_index = random.choice([4, 5])
                        ghi_log(ten_tai_khoan, f" ➙ Trốn ._. : {random_index}", level="info", style=LogStyle.YELLOW)
                        trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()                    
                    return
        
        delay_lum = check_delay_lum(account_number)
        if delay_lum.get(id_ingame) > int(time.time() * 1000):
            return
        
        if guild_quest_positions:
            ghi_log(ten_tai_khoan, f"Phát hiện Guild Quest ở các vị trí: {', '.join(guild_quest_positions)}", level="info", style=LogStyle.GREEN)
            if is_block_tai_phu:
                available_positions = [i for i in range(1, 9) if i != int(guild_quest)]
                random_index = random.choice(available_positions)
                trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                return
        if other_positions:            
            ghi_log(ten_tai_khoan, f"Phát hiện Item ở các vị trí: {', '.join(other_positions)}", level="info", style=LogStyle.GREEN)
            set_delay_lum(id_ingame, int(time.time() * 1000) + 65000)
            vi_tri_vp = int(item_position)
            set_thread_var_int("countLuomCuuGioi", count_lum + 1)
            set_thread_var("guildQuest", int(item_position))
            await asyncio.sleep(4)
            ghi_log(ten_tai_khoan, f"➙ Phát hiện VP tại [{item_position}]", level="info", style=LogStyle.GREEN)
            trinh_duyet.find_element_by_id(f'battle_position_{item_position}').click()
            return
        if gold_positions:
            ghi_log(ten_tai_khoan, f"Phát hiện Gold ở các vị trí: {', '.join(gold_positions)}", level="info", style=LogStyle.GREEN)
            if (is_block_tai_phu) :                    
                random_index = random.choice(none_positions) 
                trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()                
                pass
            else:
                ghi_log(ten_tai_khoan, f"Không phát hiện vật phẩm nào", level="info", style=LogStyle.GREEN)                
                random_index = random.choice(gold_positions)
                ghi_log(ten_tai_khoan, f"Di chuyển đến vị trí vàng: {random_index}", level="info", style=LogStyle.GREEN)
                trinh_duyet.find_element_by_id(f'battle_position_{random_index}').click()
                return 
        if none_positions:
            ghi_log(ten_tai_khoan, f"Các vị trí có thể di chuyển là: {', '.join(none_positions)}", level="info", style=LogStyle.GREEN)
            await di_chuyen_cuu_gioi(trinh_duyet, account_number)
            
    except Exception as e:
        ghi_log(ten_tai_khoan, f"Lỗi trong xu_ly_vi_tri: {e}", level="error", style=LogStyle.RED)
        return None




async def chay_cuu_vuc(trinh_duyet, account_number):
    tai_khoan = lay_thong_tin_tai_khoan(account_number)
    ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
    cuu_gioi = tai_khoan.get("CửuGiới", {})        
    is_return_cuu_gioi = get_thread_var("isReturnCuuGioi")
    is_num_cuu_gioi = get_thread_var("isNumCuuGioi")
    is_block_tai_phu = get_thread_var("isBlockTaiPhu")
    countLuomCuuGioi = get_thread_var("countLuomCuuGioi",0)
    maxErrorCuuGioi = get_thread_var("maxErrorCuuGioi",20)
    token = get_thread_var_text("Token")
    is_log_cuu_gioi = get_thread_var("isLogCuuGioi")
    chapter_token = get_thread_var_text("ChapterToken","")
    ghi_log(ten_tai_khoan, "Bắt đầu chạy Cửu Giới", level="info", style=LogStyle.GREEN)
    try:        
        if get_thread_var("isBlockedCuuGioi"):
            return
        # Sửa lại lệnh tìm phần tử theo class name
        elements = trinh_duyet.find_elements(By.CLASS_NAME, 'item')
        for element in elements:
            if "Cửu Giới" in element.text:
                element.click()
                break

        if not is_log_cuu_gioi:
            ghi_log(ten_tai_khoan, "Chưa log Cửu Giới", level="info", style=LogStyle.YELLOW)
          
            from Auto.CuuGioi import log_cuu_gioi
            await log_cuu_gioi(trinh_duyet, account_number)
            return

        TàiPhúOut = cuu_gioi.get("TàiPhúOut", 0)
        NhatVang=cuu_gioi.get("NhặtVàng", True)
        if not NhatVang and not is_block_tai_phu:            
            set_thread_var("isBlockTaiPhu", True)

        if countLuomCuuGioi >= maxErrorCuuGioi:
            await trinh_duyet.refresh()
        ghi_log(ten_tai_khoan, "🔍 Đang xử lý vị trí", level="info", style=LogStyle.YELLOW)
        await xu_ly_vi_tri(trinh_duyet, account_number)
    except Exception as e:
        ghi_log(ten_tai_khoan, f"Lỗi trong chay_cuu_vuc: {e}", level="error", style=LogStyle.RED)