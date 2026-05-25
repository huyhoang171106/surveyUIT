# -*- coding: utf-8 -*-
"""
Công cụ tự động điền nhanh phiếu khảo sát môn học dành cho sinh viên UIT.
- Phát triển bởi: Truoc Phan (truocphan112017@gmail.com)
- Cập nhật & tối ưu hóa tốc độ, đa luồng bởi: Huy Hoang
"""
import sys
import os
import time
import requests
import re
import random
from concurrent.futures import ThreadPoolExecutor

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

hocluc = 'A1'
tylethoigian = 'A3'
chuandaura = 'A5'
thangdiem = 'MH04'
ykien_hailong = ''
ykien_khonghailong = ''


def banner():
    print(r"""
                                  _    _ _____ _______ 
            v20.19.01.10         | |  | |_   _|__   __|
 ___ _   _ _ ____   _____ _   _  | |  | | | |    | |   
/ __| | | | '__\ \ / / _ \ | | | | |  | | | |    | |   
\__ \ |_| | |   \ V /  __/ |_| | | |__| |_| |_   | |   
|___/\__,_|_|    \_/ \___|\__, |  \____/|_____|  |_|   
                           __/ |                       
                          |___/    by Truoc Phan
                                   & Huy Hoang (Optimized & Multithreaded)

----------------------------------------------------
  Facebook: https://www.facebook.com/TruocPT
  Twitter: https://twitter.com/TruocPhan
  Gmail: truocphan112017@gmail.com
  GitHub: https://github.com/TruocPhan
----------------------------------------------------
""")


def print_config():
    print("--- Cấu hình khảo sát tự động ---")
    print("Học lực: Giỏi")
    print("Tỷ lệ lên lớp: >80%")
    print("Đạt chuẩn đầu ra: Trên 90%")
    print("Đánh giá giảng viên: 4 điểm (tất cả câu hỏi)")
    print("Ý kiến khác: Trống")
    print("---------------------------------\n")


def run_survey(url):
    try:
        s = requests.Session()
        s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        
        time.sleep(random.randint(1, 2))
        req = s.get(url)
        
        surveyname = re.findall(r'<p class="surveyname">(.*?)</p>', req.text)[0]
        print(f"Bắt đầu khảo sát: {surveyname}")
        
        move = re.findall(r'<input type="hidden" name="move" value="(.*?)" id="movenext" />', req.text)[0]
        move2 = re.findall(r"value='(.*?)' name='move2' id='movenextbtn' >", req.text)[0]
        sid = re.findall(r"<input type='hidden' name='sid' value='(.*?)' id='sid' />", req.text)[0]
        token = re.findall(r"<input type='hidden' name='token' value='(.*?)' id='token' />", req.text)[0]
        lastgroupname = re.findall(r"<input type='hidden' name='lastgroupname' value='(.*?)' id='lastgroupname' />", req.text)[0]
        LEMpostKey = re.findall(r"<input type='hidden' name='LEMpostKey' value='(.*?)' id='LEMpostKey' />", req.text)[0]
        thisstep = re.findall(r"<input type='hidden' name='thisstep' id='thisstep' value='(.*?)' />", req.text)[0]
        
        cookies = req.cookies

        # Tiến hành bước tiếp theo
        submit_step1(s, move, move2, sid, token, lastgroupname, LEMpostKey, thisstep, cookies, url)
    except Exception:
        print(f"Lỗi: Link khảo sát đã hoàn thành hoặc không hợp lệ: {url}")


def submit_step1(s, move, move2, sid, token, lastgroupname, LEMpostKey, thisstep, cookies, url):
    data = {
        "move": move,
        "move2": move2,
        "sid": sid,
        "token": token,
        "lastgroupname": lastgroupname,
        "LEMpostKey": LEMpostKey,
        "thisstep": thisstep
    }
    try:
        time.sleep(random.randint(1, 2))
        req = s.post("https://survey.uit.edu.vn/index.php/survey/index", data=data, cookies=cookies)

        surveyinfo = re.findall(r"Môn học:\s*(?:<strong>)?(.*?)(?:</strong>)?<br>Mã lớp:\s*(?:&nbsp;)?(?:<strong>)?(.*?)(?:</strong>)?<br>Giảng viên:\s*(?:&nbsp;)?(?:<strong>)?(.*?)(?:</strong>)?<br>", req.text)
        if not surveyinfo:
            surveyinfo = re.findall(r"Khảo sát môn:\s*(?:<strong>)?(.*?)(?:</strong>)?<br>Mã lớp:\s*(?:&nbsp;)?(?:<strong>)?(.*?)(?:</strong>)?<br>Tên giáo viên:\s*(?:&nbsp;)?(?:<strong>)?(.*?)(?:</strong>)?<br>", req.text)

        if surveyinfo:
            print(f"Môn học: {surveyinfo[0][0]} | Mã lớp: {surveyinfo[0][1]} | Giảng viên: {surveyinfo[0][2]}")

        move = re.findall(r'<input type="hidden" name="move" value="(.*?)" id="movenext" />', req.text)[0]
        move2 = re.findall(r"value='(.*?)' name='move2' id='movenextbtn' >", req.text)[0]
        sid = re.findall(r"<input type='hidden' name='sid' value='(.*?)' id='sid' />", req.text)[0]
        token = re.findall(r"<input type='hidden' name='token' value='(.*?)' id='token' />", req.text)[0]
        lastgroupname = re.findall(r"<input type='hidden' name='lastgroupname' value='(.*?)' id='lastgroupname' />", req.text)[0]
        LEMpostKey = re.findall(r"<input type='hidden' name='LEMpostKey' value='(.*?)' id='LEMpostKey' />", req.text)[0]
        thisstep = re.findall(r"<input type='hidden' name='thisstep' id='thisstep' value='(.*?)' />", req.text)[0]

        submit_step2(s, move, move2, sid, token, lastgroupname, LEMpostKey, thisstep, cookies, url)
    except Exception:
        print(f"Lỗi khi gửi thông tin bước 1 cho link: {url}")


def submit_step2(s, move, move2, sid, token, lastgroupname, LEMpostKey, thisstep, cookies, url):
    data = {
        "move": move,
        "move2": move2,
        "sid": sid,
        "token": token,
        "lastgroupname": lastgroupname,
        "LEMpostKey": LEMpostKey,
        "thisstep": thisstep
    }
    try:
        time.sleep(random.randint(1, 2))
        req = s.post("https://survey.uit.edu.vn/index.php/survey/index", data=data, cookies=cookies)

        mapped_fields = {}
        questions_list = [
            ("hocluc", "Xếp loại học lực trong học kỳ vừa qua?"),
            ("tylethoigian", "Tỷ lệ thời gian Anh/Chị lên lớp đối với môn học này"),
            ("chuandaura", "Anh chị tự đánh giá đạt được bao nhiêu % chuẩn đầu ra của môn học này:")
        ]
        for key, q_text in questions_list:
            pos = req.text.find(q_text)
            if pos != -1:
                match = re.search(r"name=['\"](\d+X\d+X\d+)['\"]", req.text[pos:])
                if match:
                    mapped_fields[key] = match.group(1)

        fieldnames = re.findall(r"<input type='hidden' name='fieldnames' value='(.*?)' id='fieldnames' />", req.text)[0]
        lastgroup = re.findall(r"<input type='hidden' name='lastgroup' value='(.*?)' id='lastgroup' />", req.text)[0]
        relevance = re.findall(r"<input type='hidden' id='relevance(.*?)' name='relevance\1' value='(.*?)'/>", req.text)
        move = re.findall(r'<input type="hidden" name="move" value="(.*?)" id="movenext" />', req.text)[0]
        thisstep = re.findall(r"<input type='hidden' name='thisstep' value='(.*?)' id='thisstep' />", req.text)[0]
        sid = re.findall(r"<input type='hidden' name='sid' value='(.*?)' id='sid' />", req.text)[0]
        start_time = re.findall(r"<input type='hidden' name='start_time' value='(.*?)' id='start_time' />", req.text)[0]
        LEMpostKey = re.findall(r"<input type='hidden' name='LEMpostKey' value='(.*?)' id='LEMpostKey' />", req.text)[0]
        token = re.findall(r"<input type='hidden' name='token' value='(.*?)' id='token' />", req.text)[0]

        submit_step3(s, fieldnames, lastgroup, relevance, move, thisstep, sid, start_time, LEMpostKey, token, cookies, url, mapped_fields)
    except Exception:
        print(f"Lỗi khi gửi thông tin bước 2 cho link: {url}")


def submit_step3(s, fieldnames, lastgroup, relevance, move, thisstep, sid, start_time, LEMpostKey, token, cookies, url, mapped_fields):
    data = {
        "fieldnames": fieldnames,
        "lastgroup": lastgroup,
        "move": move,
        "thisstep": thisstep,
        "sid": sid,
        "start_time": start_time,
        "LEMpostKey": LEMpostKey,
        "token": token
    }
    try:
        for field in fieldnames.split("|"):
            if field == mapped_fields.get("hocluc"):
                data[field] = hocluc
                data["java" + field] = hocluc
            elif field == mapped_fields.get("tylethoigian"):
                data[field] = tylethoigian
                data["java" + field] = tylethoigian
            elif field == mapped_fields.get("chuandaura"):
                data[field] = chuandaura
                data["java" + field] = chuandaura

        for i in relevance:
            data["relevance" + i[0]] = "1"

        time.sleep(random.randint(1, 2))
        req = s.post("https://survey.uit.edu.vn/index.php/survey/index", data=data, cookies=cookies)
        
        fieldnames = re.findall(r"<input type='hidden' name='fieldnames' value='(.*?)' id='fieldnames' />", req.text)[0]
        lastgroup = re.findall(r"<input type='hidden' name='lastgroup' value='(.*?)' id='lastgroup' />", req.text)[0]
        relevance = re.findall(r"<input type='hidden' id='relevance(.*?)' name='relevance\1' value='(.*?)'/>", req.text)
        move = re.findall(r'<input type="hidden" name="move" value="(.*?)" id="movenext" />', req.text)[0]
        thisstep = re.findall(r"<input type='hidden' name='thisstep' value='(.*?)' id='thisstep' />", req.text)[0]
        sid = re.findall(r"<input type='hidden' name='sid' value='(.*?)' id='sid' />", req.text)[0]
        start_time = re.findall(r"<input type='hidden' name='start_time' value='(.*?)' id='start_time' />", req.text)[0]
        LEMpostKey = re.findall(r"<input type='hidden' name='LEMpostKey' value='(.*?)' id='LEMpostKey' />", req.text)[0]
        token = re.findall(r"<input type='hidden' name='token' value='(.*?)' id='token' />", req.text)[0]
        
        points = {}
        for field in fieldnames.split("|"):
            if "MH" in field:
                points[field] = thangdiem

        data_p3 = {
            "fieldnames": fieldnames,
            "lastgroup": lastgroup,
            "move": move,
            "thisstep": thisstep,
            "sid": sid,
            "start_time": start_time,
            "LEMpostKey": LEMpostKey,
            "token": token
        }
        for i in points:
            data_p3[i] = points[i]
            data_p3["java" + i] = points[i]
        for i in relevance:
            data_p3["relevance" + i[0]] = "1"

        time.sleep(random.randint(1, 2))
        req_p3 = s.post("https://survey.uit.edu.vn/index.php/survey/index", data=data_p3, cookies=cookies)

        if "movesubmit" in req_p3.text:
            fieldnames = re.findall(r"<input type='hidden' name='fieldnames' value='(.*?)' id='fieldnames' />", req_p3.text)[0]
            lastgroup = re.findall(r"<input type='hidden' name='lastgroup' value='(.*?)' id='lastgroup' />", req_p3.text)[0]
            relevance = re.findall(r"<input type='hidden' id='relevance(.*?)' name='relevance\1' value='(.*?)'/>", req_p3.text)
            move = re.findall(r'<input type="hidden" name="move" value="(.*?)" id="movesubmit" />', req_p3.text)[0]
            thisstep = re.findall(r"<input type='hidden' name='thisstep' value='(.*?)' id='thisstep' />", req_p3.text)[0]
            sid = re.findall(r"<input type='hidden' name='sid' value='(.*?)' id='sid' />", req_p3.text)[0]
            start_time = re.findall(r"<input type='hidden' name='start_time' value='(.*?)' id='start_time' />", req_p3.text)[0]
            LEMpostKey = re.findall(r"<input type='hidden' name='LEMpostKey' value='(.*?)' id='LEMpostKey' />", req_p3.text)[0]
            token = re.findall(r"<input type='hidden' name='token' value='(.*?)' id='token' />", req_p3.text)[0]

            submit_step4(s, fieldnames, lastgroup, relevance, move, thisstep, sid, start_time, LEMpostKey, token, cookies, url, req_p3.text)
        else:
            print(f"Đã hoàn thành khảo sát: {url}")
    except Exception:
        print(f"Lỗi khi gửi thông tin bước 3 cho link: {url}")


def submit_step4(s, fieldnames, lastgroup, relevance, move, thisstep, sid, start_time, LEMpostKey, token, cookies, url, html_content):
    data = {
        "fieldnames": fieldnames,
        "lastgroup": lastgroup,
        "move": move,
        "thisstep": thisstep,
        "sid": sid,
        "start_time": start_time,
        "LEMpostKey": LEMpostKey,
        "token": token
    }
    try:
        comment_questions = [
            ("hailong", "Điều Anh/ Chị hài lòng nhất về"),
            ("khonghailong", "Điều Anh/ Chị không hài lòng nhất về"),
            ("dexuat", "Đề xuất của Anh/Chị để hoạt động giảng dạy của môn học này")
        ]
        mapped_comments = {}
        for key, q_text in comment_questions:
            q_text_norm = re.sub(r'\s+', ' ', q_text.lower())
            html_clean = re.sub(r'\s+', ' ', html_content.lower())
            pos = html_clean.find(q_text_norm)
            if pos != -1:
                orig_pos = re.search(re.escape(q_text[0:15]), html_content, re.IGNORECASE)
                if orig_pos:
                    match = re.search(r"name=['\"](\d+X\d+X\d+)['\"]", html_content[orig_pos.start():])
                    if match:
                        mapped_comments[key] = match.group(1)

        for field in fieldnames.split("|"):
            if field == mapped_comments.get("hailong"):
                data[field] = ykien_hailong
            elif field == mapped_comments.get("khonghailong"):
                data[field] = ykien_khonghailong
            else:
                data[field] = ""

        for i in relevance:
            data["relevance" + i[0]] = "1"

        time.sleep(random.randint(1, 2))
        req = s.post("https://survey.uit.edu.vn/index.php/survey/index", data=data, cookies=cookies)

        if "HOÀN THÀNH KHẢO SÁT" in req.text or "hoàn thành khảo sát" in req.text.upper():
            print(f"Đã hoàn thành khảo sát: {url}")
        else:
            print(f"Lỗi: Không thể xác nhận hoàn thành cho link: {url}")
    except Exception:
        print(f"Lỗi khi gửi thông tin bước 4 cho link: {url}")


def main():
    banner()
    if len(sys.argv) < 2:
        print(f"Cách sử dụng:\n  python {sys.argv[0]} [link_portal] [cookie]\nhoặc:\n  python {sys.argv[0]} [file_chứa_link]")
        sys.exit(1)

    print_config()
    arg1 = sys.argv[1]
    urls = []

    if arg1.startswith("http://") or arg1.startswith("https://"):
        if len(sys.argv) < 3:
            print("Lỗi: Vui lòng cung cấp cookie khi sử dụng link portal.")
            sys.exit(1)
        cookie_arg = sys.argv[2]
        cookie_dict = {}
        if "=" in cookie_arg:
            parts = cookie_arg.split("=", 1)
            cookie_dict[parts[0].strip()] = parts[1].strip()
        else:
            cookie_dict["SSESSdf6f777d3f8a1d0fb2e4e5d1ec62f6e2"] = cookie_arg.strip()

        print("Đang quét danh sách khảo sát từ Portal...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            req = requests.get(arg1, cookies=cookie_dict, headers=headers)
            rows = re.findall(r'<tr.*?>.*?</tr>', req.text, re.DOTALL)
            for row in rows:
                if "survey.uit.edu.vn" in row:
                    if "Chưa khảo sát" in row:
                        link_match = re.search(r'href=["\'](https?://survey\.uit\.edu\.vn/[^"\']+)["\']', row)
                        if link_match:
                            urls.append(link_match.group(1).replace("http://", "https://"))
            print(f"Tìm thấy {len(urls)} khảo sát chưa hoàn thành.")
        except Exception as e:
            print(f"Lỗi khi tải danh sách khảo sát từ Portal: {e}")
            sys.exit(1)
    else:
        if not os.path.isfile(arg1):
            print(f"Lỗi: File '{arg1}' không tồn tại.")
            sys.exit(1)
        with open(arg1, "r", encoding="utf-8") as f:
            for url in f:
                u = url.strip()
                if u:
                    urls.append(u.replace("http://", "https://"))
        print(f"Đọc thành công {len(urls)} link từ file.")

    if urls:
        print("Bắt đầu điền khảo sát tự động (sử dụng tối đa 4 luồng)...")
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(run_survey, urls)
        print("Đã hoàn tất toàn bộ khảo sát.")


if __name__ == "__main__":
    main()