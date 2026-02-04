from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# ===== CONFIG =====
URL = "https://hrleaveapp-335bem9z.manus.space/"
TOKEN = os.getenv("HR_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuSWQiOiI1cVdSWVNwb3FldlVaUEd1VkpHNkZjIiwiYXBwSWQiOiIzMzViRW05WjdhcnRqcmtqZDNoQ2dUIiwibmFtZSI6IlNvbWJvb24gWmFpcGhvcGh1IiwiZXhwIjoxODAxNjc4Nzc1fQ.BNBR5Uz0V3vgrsLjdkbENU_4z8DEiQoVJn-LpC0zLZo")

# ===== Chrome options =====
options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

# ใช้ webdriver-manager เพื่อจัดการ ChromeDriver อัตโนมัติ
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(URL)
    time.sleep(3)

    # เพิ่ม token ลงใน cookie
    driver.add_cookie({
        "name": "app_session_id",
        "value": TOKEN,
        "domain": "hrleaveapp-335bem9z.manus.space"
    })

    # เพิ่มข้อมูลใน local storage
    driver.execute_script("""
        localStorage.setItem('manus-runtime-user-info', '{"id":8460001,"openId":"5qWRYSpoqevUZPGuVJG6Fc","name":"Somboon Zaiphophu","email":"somboon.zai@techflow.asia","loginMethod":"microsoft","role":"user","departmentId":360007,"positionId":1,"startDate":null,"lastSignedIn":"2026-02-03T18:20:43.000Z","createdAt":"2026-01-26T01:17:25.000Z","updatedAt":"2026-02-03T18:20:42.000Z"}');
        localStorage.setItem('AMP_unsent_46ac3f9abb', '[]');
        localStorage.setItem('AMP_remote_config_46ac3f9abb', '{"remoteConfig":{"configs":{"diagnostics":{},"sessionReplay":{},"analyticsSDK":{}}},"lastFetch":"2026-02-03T18:19:36.807Z"}');
    """)

    # รีเฟรชหน้าเพื่อใช้ cookie และ local storage
    driver.refresh()
    time.sleep(8)

    # รอให้ attendance button โหลด
    wait = WebDriverWait(driver, 30)
    attendance_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#root > div > div > div.group.peer.text-sidebar-foreground.hidden.md\\:block > div.fixed.inset-y-0.z-10.hidden.h-svh.w-\\(--sidebar-width\\).md\\:flex.transition-\\[left\\,right\\,width\\].duration-200.ease-linear.left-0.group-data-\\[collapsible\\=offcanvas\\]\\:left-\\[calc\\(var\\(--sidebar-width\\)\\*-1\\)\\].group-data-\\[collapsible\\=icon\\]\\:w-\\(--sidebar-width-icon\\).group-data-\\[side\\=left\\]\\:border-r.group-data-\\[side\\=right\\]\\:border-l.border-r.border-border > div > div.flex.min-h-0.flex-1.flex-col.overflow-auto.group-data-\\[collapsible\\=icon\\]\\:overflow-hidden.gap-0.py-2 > ul > div:nth-child(2)")))
    attendance_btn.click()
    time.sleep(5)
    print("✅ Clicked attendance menu")

    # รอและคลิก div ตัวแรก
    try:
        # ขั้นตอนที่ 1: ลองกด switch (first_div) ถ้ามี
        switch_clicked = False
        try:
            first_div = driver.find_element(By.CSS_SELECTOR, "#root > div > main > main > div > div.grid.gap-6.md\\:grid-cols-2 > div:nth-child(1) > div.px-6.space-y-4 > div.space-y-3.p-4.bg-muted\\/30.rounded-lg.border > div.space-y-2 > div.flex.items-center.space-x-2.pt-2")
            if first_div.is_displayed():
                first_div.click()
                time.sleep(2)
                print("✅ Clicked switch (first_div)")
                switch_clicked = True
        except:
            pass
        
        # ขั้นตอนที่ 2: ถ้าไม่มี switch ต้องมี error_div
        if not switch_clicked:
            try:
                error_div = driver.find_element(By.CSS_SELECTOR, "#root > div > main > main > div > div.grid.gap-6.md\\:grid-cols-2 > div:nth-child(1) > div.px-6.space-y-4 > div.space-y-3.p-4.bg-muted\\/30.rounded-lg.border > div.text-sm.text-red-500.flex.items-center.gap-2")
                if error_div and error_div.is_displayed():
                    print(f"⚠️  {error_div.text}")
            except:
                print("⚠️  No switch and no error message found")

        # ขั้นตอนที่ 3: กด submit
        try:
            submit_btn = driver.find_element(By.CSS_SELECTOR, "#root > div > main > main > div > div.grid.gap-6.md\\:grid-cols-2 > div:nth-child(1) > div.px-6.space-y-4 > div.flex.gap-4 > button.inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.rounded-md.text-sm.font-medium.transition-all.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\:not\\(\\[class\\*\\=\\'size-\\'\\]\\)\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.outline-none.focus-visible\\:border-ring.focus-visible\\:ring-ring\\/50.focus-visible\\:ring-\\[3px\\].aria-invalid\\:ring-destructive\\/20.dark\\:aria-invalid\\:ring-destructive\\/40.aria-invalid\\:border-destructive.text-primary-foreground.h-9.px-4.py-2.has-\\[\\>svg\\]\\:px-3.flex-1.bg-green-600.hover\\:bg-green-700")
            if submit_btn.is_displayed():
                print(f"✅ Found submit button: {submit_btn.text}")
                submit_btn.click()
                time.sleep(2)
                print("✅ Clicked submit button - Check-in complete!")
        except:
            print("⏭️  Submit button not found, skipping...")
    except Exception as e:
        print(f"⚠️  Exception in attendance flow: {str(e)[:100]}")

    time.sleep(2)
    print("✅ Attendance success")

except Exception as e:
    print("❌ Error:", e)

finally:
    driver.quit()
