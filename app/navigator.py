import os
from playwright.sync_api import sync_playwright


def generate_markdown_report(sub_pages: list[str], url: str, site_name: str):
    markdown = f"# {site_name} Sub-Pages\n\n"
    markdown += f"## Below is a list of sub-pages found on [{site_name}](https://www.{url}):\n\n"
    for url in sub_pages:
        markdown += f"1. [{url}]({url})\n"

    return markdown


def navigate_subpages(page, sub_pages):
    for s in sub_pages:
        page.goto(s, timeout=0)
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(2000)


def navigate_pages(name: str, url: str, path: str, rec_path: str) -> int:
    with sync_playwright() as p:
        split = url.split('.')
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(record_video_dir=f"{rec_path}", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                                viewport={"width": 1920, "height": 1080})
        page.goto(url=url, timeout=0, wait_until='domcontentloaded')
        page.wait_for_timeout(2500)
        sub_pages = page.evaluate(f"""
            Array.from(document.querySelectorAll('a'))
                .map(anchor => anchor.href)
                .filter(href => href.includes('{split[1]}') && !href.endsWith('#'))
        """)
        sub_pages = list(set(sub_pages))

        markdown_report = generate_markdown_report(
            sub_pages, f"{split[1].replace(' ', '')}.gov", name)
        filename = f"{name.replace(' ','_')}_SubPages_Report.md"

        with open(f"{path}/{filename}", "w") as file:
            file.write(markdown_report)

        page.evaluate("window.scrollTo(0, document.body.scrollHeight/4)")
        page.wait_for_timeout(1500)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
        page.wait_for_timeout(1500)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1500)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1000)

        # navigate_subpages(page, sub_pages[:10])

        page.close()
        init_path = page.video.path()
        page.video.save_as(f"{rec_path}/{name}.webm")
        browser.close()
        os.remove(init_path)

    return len(sub_pages)