from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright

def worker(url: str):
    # Everything inside the thread
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    print(f"{url} → {page.title()}")
    browser.close()          # optional; also closed by context manager

urls = ["https://example.com", "https://google.com", "https://github.com"]
with ThreadPoolExecutor(max_workers=3) as pool:
    pool.map(worker, urls)