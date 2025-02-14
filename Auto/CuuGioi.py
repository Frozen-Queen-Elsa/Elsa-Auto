from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from HamPhuTro.GhiLog import ghi_log, LogStyle
from HamPhuTro.Exception import handle_exception
from HamPhuTro.RefreshWeb import reload_by_ajax, auto_check_and_reload, auto_reload_by_ajax
from Data.DataMoiTaiKhoan import lay_url_web, lay_thong_tin_tai_khoan, lay_refer_link, set_thread_var, get_thread_var, set_thread_var_int, set_delay_lum
from Auto.DangNhap import dang_nhap,dang_xuat
from Auto.CuuGioiHelper import check_tai_phu, pre_logout, restore_mau, check_sua_do
from Auto.CuuGioiDiChuyen import chay_cuu_vuc


import aiohttp, asyncio, time, json

def vao_trang_cuu_gioi(trinh_duyet, account_number):
    try:
        URL = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        
        # Bước 1: Vào trang game dashboard
        ghi_log(ten_tai_khoan, "Mở trang game dashboard", level='info')    
        trinh_duyet.get(URL + "/user/game/dashboard")
        
        # Bước 2: Tìm và click vào element "Cửu Giới"
        ghi_log(ten_tai_khoan, "Tìm và click vào Cửu Giới", level='info')
        element = WebDriverWait(trinh_duyet, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div[3]/div[2]/div/div[7]/img"))
        )
        element.click()
        
        time.sleep(5)
        
        # Bước 3: Kiểm tra xem đã vào trang Cửu Giới chưa
        if not kiem_tra_trang_cuu_gioi(trinh_duyet, account_number):
            ghi_log(ten_tai_khoan, "Không vào được trang Cửu Giới", level='error')
            vao_trang_cuu_gioi(trinh_duyet, account_number)
        
        # Bước 4: Thực hiện hành động nếu đã vào trang Cửu Giới
        tieu_de = WebDriverWait(trinh_duyet, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div[3]/p"))
        ).text
        if tieu_de in ["Cửu Giới", "Địa Hải Giới (Tân Thủ)", "Băng Nguyên Giới", "Hỏa Viêm Vực", "Minh Giới", "Tổ Long Sào", "Loạn Lôi Đảo"]:
            if tieu_de == "Cửu Giới":
                ghi_log(ten_tai_khoan, "Đang ở trang Cửu Giới và chưa vào map", level='info')
                isBlockedCuuGioi = get_thread_var("isBlockedCuuGioi")
                if not isBlockedCuuGioi:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)                
                    time.sleep(5)
                    elements = trinh_duyet.find_elements(By.XPATH, "//div[contains(@class, 'Item') and contains(@class, 'disable map_position_1')]")
                    if elements:
                        ghi_log(ten_tai_khoan, "Đang trong hoạt động Cửu Giới", level='info')
                    else:
                        asyncio.run(log_cuu_gioi(trinh_duyet, account_number))
                
                else:
                    ghi_log(ten_tai_khoan, "Cửu Giới bị khóa", level='error')
            
            else:
                ghi_log(ten_tai_khoan, f"Đang ở trang Cửu Giới và ở trong map {tieu_de}", level='info')                
                elements = trinh_duyet.find_elements(By.XPATH, "//div[contains(@class, 'Item') and contains(@class, 'disable map_position_1')]")
                if elements:
                    ghi_log(ten_tai_khoan, "Đang trong hoạt động Cửu Giới map {tieu_de}", level='info')
                else:
                    elements = trinh_duyet.find_elements(By.CLASS_NAME, "battle_map_join text_battle_map_join")
                    for element in elements:
                        if element.get_attribute("placeholder") == "Vào map":
                            element.click()
                            ghi_log(ten_tai_khoan, "Đã click vào nút Vào Map", level='info')
                            break
                    
        else:
            ghi_log(ten_tai_khoan, "Không ở trong trang Cửu Giới", level='error')
            vao_trang_cuu_gioi(trinh_duyet, account_number)
        
        set_thread_var("isLogCuuGioi",True)        
        
        
        async def auto_sua_do(trinh_duyet,account_number):
            while True:
                await check_sua_do(trinh_duyet,account_number)
                await asyncio.sleep(300)  # 5 minutes

      
        async def auto_restore_mau(trinh_duyet,account_number):
            while True:
                await restore_mau(trinh_duyet,account_number)
                await asyncio.sleep(61)
        async def auto_chay_cuu_vuc(trinh_duyet, account_number):
            while True:
                try:
                    await chay_cuu_vuc(trinh_duyet, account_number)
                except Exception as e:
                    ghi_log("Hệ thống", f"Lỗi trong chay_cuu_vuc: {e}", level="error")
                await asyncio.sleep(5)

        async def auto_check_tai_phu(trinh_duyet,account_number):
            while True:
                await check_tai_phu(trinh_duyet,account_number)
                await asyncio.sleep(60)

        async def auto_reload_web(trinh_duyet):
            while True:
                await asyncio.sleep(1800)  # 30 minutes
                ghi_log("Hệ thống", "Tự động reload trang web", level='info')
                trinh_duyet.refresh()
                
                        
        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)
       # Bắt đầu tự động chạy cửu vực
        loop.create_task(auto_chay_cuu_vuc(trinh_duyet,account_number))      

        # Chạy event loop (khối dưới đây sẽ chạy mãi do các task lặp vô hạn)
        loop.run_forever()
        
    except Exception as e:
        handle_exception(e)
        ghi_log(ten_tai_khoan, f"Lỗi khi vào trang Cửu Giới: {str(e)}", level='error')

def kiem_tra_trang_cuu_gioi(trinh_duyet,account_number):
    try:
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        tieu_de = WebDriverWait(trinh_duyet, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div[3]/p"))
        ).text
        cac_tieu_de_hop_le = [
            "Cửu Giới", "Địa Hải Giới (Tân Thủ)", "Băng Nguyên Giới", 
            "Hỏa Viêm Vực", "Minh Giới", "Tổ Long Sào", "Loạn Lôi Đảo"
        ]
        for tieu_de_hop_le in cac_tieu_de_hop_le:
            if tieu_de_hop_le in tieu_de:
                return True
        return False
    except Exception as e:
        handle_exception(e)
        ghi_log(ten_tai_khoan, f"Lỗi khi kiểm tra trang Cửu Giới: {str(e)}", level='error')
        return False

async def log_cuu_gioi(trinh_duyet, account_number):
    """
    Async: Thực hiện join Cửu Giới.
    Gọi API POST với body 'action=join&type=word&area={khuVuc}'.
    Nếu phản hồi chứa 'Bạn đang trong thời gian hồi sinh', tính thời gian chờ và log thông báo;
    nếu chứa 'thành công' sẽ log và reload (mô phỏng reload ở đây);
    ngược lại, đặt cờ isBlockedCuuGioi = True.
    """
    try:
        URL = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        cuu_gioi = tai_khoan.get("CửuGiới", {})
        khu_vuc = cuu_gioi.get("KhuVực")
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
            body: `action=join&type=word&area={khu_vuc}`,
        }});
        const res = await response.text();
        return res;
        """
        res_text= trinh_duyet.execute_script(js_code)
        ghi_log(ten_tai_khoan, f"Phản hồi từ API: {res_text}", level="info")


        
        # Nếu phản hồi chứa "Bạn đang trong thời gian hồi sinh", log và chờ
        if "you_are_reviving" in res_text or "Bạn đang trong thời gian hồi sinh" in res_text:
            times = res_text.split("second = ")[1].split(";")[0]
            minutes = int(times) / 60
            ghi_log(ten_tai_khoan, f"Đang trong thời gian hồi sinh: còn {minutes} phút để vào Cửu Giới", level="info", style=LogStyle.YELLOW)
            set_thread_var("isLogCuuGioi", True)
            next_time = time.time() + int(times)
            ghi_log(ten_tai_khoan, f"Thời gian tiếp theo có thể vào lại: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(next_time))}", level="info", style=LogStyle.YELLOW)
            set_thread_var_int("timeLogCuuGioi", next_time)
            await asyncio.sleep(int(times) + 1)
            await log_cuu_gioi(trinh_duyet, account_number)
        
        # Nếu phản hồi chứa "trình duyệt", đăng nhập lại
        elif "trình duyệt" in res_text:
            ghi_log(ten_tai_khoan, "Lỗi đổi trình duyệt chuẩn bị đăng nhập lại", level="info", style=LogStyle.YELLOW)   
          
            
            dang_xuat(trinh_duyet, account_number)
            time.sleep(5)
            dang_nhap(trinh_duyet, account_number)
            vao_trang_cuu_gioi(trinh_duyet, account_number)
            return
        
        # Nếu phản hồi chứa "thành công", log và reload trang
        elif "thành công" in res_text:
            ghi_log(ten_tai_khoan, "Tham gia Cửu Giới thành công", level="info", style=LogStyle.GREEN)
            await reload_by_ajax(trinh_duyet, "/html/body/div[2]/div[2]")
        else:           
            ghi_log(ten_tai_khoan, "Không có phản hồi API", level="info", style=LogStyle.YELLOW)
            #set_thread_var("isBlockedCuuGioi", True) 
            return
    except Exception as error:
        ghi_log(ten_tai_khoan, f"Lỗi trong log_cuu_gioi: {error}", level="error", style=LogStyle.RED)
        
async def get_battle(account_number, battle_id):
    try:
        URL = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        query_url = f"{URL}/api/get_data_by_id?table=game_battle&data=data&id={battle_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(query_url, timeout=10) as response:
                response_data = await response.json()
                parsed_data = json.loads(response_data.get("data", "{}"))

                team = parsed_data.get("team", {})
                winner = parsed_data.get("winner")

                teams = list(team.keys())
                team1 = teams[0] if len(teams) > 0 else None
                team2 = teams[1] if len(teams) > 1 else None

                print("Team1:", team1)
                print("Team2:", team2)
                print("Winner:", winner)

                if winner == 'monster':
                    set_thread_var("isBlockLog", False)
                    ghi_log(ten_tai_khoan, "Quái cắn tử nạn", level="info")
                    print(" ➙ Bị creept cắn tử nạn!")
                elif team2 == 'monster' and team1 == winner:
                    ghi_log(ten_tai_khoan, "Giết Quái", level="info")
                    print(" ➙😈 Creept...! 😈")
                elif team2 != 'monster' and team1 == winner:
                    ghi_log(ten_tai_khoan, "Lụm Shipper", level="info")
                    print(" ➙🎅 Lụm Shipper..! 🎅")
                elif team2 != 'monster' and team2 == winner:
                    set_thread_var("isBlockLog", False)
                    ghi_log(ten_tai_khoan, "Bị bem tử nạn", level="info")
                    print(" ➙ Bị bem tử nạn")
    except Exception as e:
        print(f"Lỗi trong get_battle: {e}")
        ghi_log(ten_tai_khoan, f"Lỗi trong get_battle: {e}", level="error")

async def listen_for_events(account_number):
    """
    Lắng nghe các sự kiện từ API và thực hiện hành động tương ứng.
    """
    try:
        URL = lay_url_web()
        tai_khoan = lay_thong_tin_tai_khoan(account_number)
        ten_tai_khoan = tai_khoan.get("TênTàiKhoản", "Hệ thống")
        refe_link = lay_refer_link()
        post_url = f"{URL}/assets/ajax/battle_map.php"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Referer": refe_link,
        }
        payload = {"action": "listen_events"}
        async with aiohttp.ClientSession() as session:
            async with session.post(post_url, headers=headers, data=payload, timeout=10) as response:
                res_text = await response.text()
                ghi_log(ten_tai_khoan, f"Lắng nghe event Phản hồi từ API: {res_text}", level="info")
                if 'Túi trữ vật đã đạt giới hạn tối đa' in res_text:
                    ghi_log(ten_tai_khoan, "Túi trữ vật đã đạt giới hạn tối đa", level="info")
                    await pre_logout(account_number)
                    return
                if 'popup_load' in res_text:
                    print('Đã lụm...!')
                    set_thread_var_int("countLum", 0)
                    ghi_log(ten_tai_khoan, "Đã lụm", level="info")
                    await check_tai_phu(account_number)
                    set_delay_lum(account_number, 0)
                    return
                if 'battle_id' in res_text:
                    await restore_mau(account_number)
                    battle_id = res_text.split("battle_id = '")[1].split("';frame_loa")[0]
                    ghi_log(ten_tai_khoan, f"Đã vào trận đấu {battle_id}", level="info")
                    print('battle_id: ', battle_id)
                    await get_battle(account_number, battle_id)
                    return
                if 'Đây không phải là mục tiêu của bạn' in res_text or 'Chỉ dành cho nhiệm vụ Tông Môn' in res_text or 'guild_quest' in res_text:
                    print(f"➙ Boss nhiệm vụ..")
                    ghi_log(ten_tai_khoan, "Boss nhiệm vụ", level="info")
                    set_delay_lum(account_number, 0)
                    return
    except Exception as e:
        ghi_log(ten_tai_khoan if 'ten_tai_khoan' in locals() else "Hệ thống",
                f"Lỗi trong listen_for_events: {e}", level="error", style=LogStyle.RED)
        
        
