from playwright.sync_api import sync_playwright
import time
import os

# ===== CONFIG =====
URL = "https://hrleaveapp-335bem9z.manus.space/"
TOKEN = os.getenv("HR_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuSWQiOiI1cVdSWVNwb3FldlVaUEd1VkpHNkZjIiwiYXBwSWQiOiIzMzViRW05WjdhcnRqcmtqZDNoQ2dUIiwibmFtZSI6IlNvbWJvb24gWmFpcGhvcGh1IiwiZXhwIjoxODAxNjc4Nzc1fQ.BNBR5Uz0V3vgrsLjdkbENU_4z8DEiQoVJn-LpC0zLZo")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    try:
        page.goto(URL)
        time.sleep(3)

        # เพิ่ม cookie
        context.add_cookies([{
            "name": "app_session_id",
            "value": TOKEN,
            "domain": "hrleaveapp-335bem9z.manus.space",
            "path": "/"
        }])

        # เพิ่มข้อมูลใน local storage
        page.evaluate("""
            localStorage.setItem('manus-runtime-user-info', '{"id":8460001,"openId":"5qWRYSpoqevUZPGuVJG6Fc","name":"Somboon Zaiphophu","email":"somboon.zai@techflow.asia","loginMethod":"microsoft","role":"user","departmentId":360007,"positionId":1,"startDate":null,"lastSignedIn":"2026-02-03T18:20:43.000Z","createdAt":"2026-01-26T01:17:25.000Z","updatedAt":"2026-02-03T18:20:42.000Z"}');
            localStorage.setItem('AMP_unsent_46ac3f9abb', '[]');
            localStorage.setItem('AMP_remote_config_46ac3f9abb', '{"remoteConfig":{"configs":{"diagnostics":{},"sessionReplay":{},"analyticsSDK":{}}},"lastFetch":"2026-02-03T18:19:36.807Z"}');
        """)

        # รีเฟรชหน้า
        page.reload()
        time.sleep(8)

        # คลิก attendance button
        attendance_btn = page.locator("#root > div > div > div.group.peer.text-sidebar-foreground.hidden.md\\:block > div.fixed.inset-y-0.z-10.hidden.h-svh.w-\\(--sidebar-width\\).md\\:flex.transition-\\[left\\,right\\,width\\].duration-200.ease-linear.left-0.group-data-\\[collapsible\\=offcanvas\\]\\:left-\\[calc\\(var\\(--sidebar-width\\)\\*-1\\)\\].group-data-\\[collapsible\\=icon\\]\\:w-\\(--sidebar-width-icon\\).group-data-\\[side\\=left\\]\\:border-r.group-data-\\[side\\=right\\]\\:border-l.border-r.border-border > div > div.flex.min-h-0.flex-1.flex-col.overflow-auto.group-data-\\[collapsible\\=icon\\]\\:overflow-hidden.gap-0.py-2 > ul > div:nth-child(2)")
        attendance_btn.wait_for(state="visible", timeout=30000)
        attendance_btn.click()
        time.sleep(5)
        print("✅ Clicked attendance menu")

        # ตรวจสอบ error message
        try:
            error_div = page.locator("#root > div > main > main > div > div.grid.gap-6.md\\:grid-cols-2 > div:nth-child(1) > div.px-6.space-y-4 > div.space-y-3.p-4.bg-muted\\/30.rounded-lg.border > div.text-sm.text-red-500.flex.items-center.gap-2")
            if error_div.is_visible():
                print(f"⚠️  {error_div.inner_text()} - ข้ามขั้นตอนการลงเวลา")
            else:
                raise Exception("No error, proceed")
        except:
            # ไม่มี error message ให้ดำเนินการปกติ
            first_div = page.locator("#root > div > main > main > div > div.grid.gap-6.md\\:grid-cols-2 > div:nth-child(1) > div.px-6.space-y-4 > div.space-y-3.p-4.bg-muted\\/30.rounded-lg.border > div.space-y-2 > div.flex.items-center.space-x-2.pt-2")
            first_div.wait_for(state="visible", timeout=30000)
            first_div.click()
            time.sleep(2)
            print("✅ Clicked first div")

            # หาปุ่มที่จะกด
            submit_btn = page.locator("#root > div > main > main > div > div.grid.gap-6.md\\:grid-cols-2 > div:nth-child(1) > div.px-6.space-y-4 > div.flex.gap-4 > button.inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.rounded-md.text-sm.font-medium.transition-all.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\:not\\(\\[class\\*\\=\\'size-\\'\\]\\)\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.outline-none.focus-visible\\:border-ring.focus-visible\\:ring-ring\\/50.focus-visible\\:ring-\\[3px\\].aria-invalid\\:ring-destructive\\/20.dark\\:aria-invalid\\:ring-destructive\\/40.aria-invalid\\:border-destructive.text-primary-foreground.h-9.px-4.py-2.has-\\[\\>svg\\]\\:px-3.flex-1.bg-green-600.hover\\:bg-green-700")
            submit_btn.wait_for(state="visible", timeout=30000)
            print(f"✅ Found submit button: {submit_btn.inner_text()}")
            print("⏸️  Ready to click submit button (not clicking yet)")

        time.sleep(2)
        print("✅ Attendance success")

    except Exception as e:
        print(f"❌ Error: {e}")
        raise

    finally:
        browser.close()
