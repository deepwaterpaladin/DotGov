from playwright.sync_api import sync_playwright
from datetime import datetime


def generate_markdown_report(sub_pages, url):
    # Header for the markdown report
    markdown = f"# {url} Sub-Pages\n\n"
    markdown += f"### Below is a list of sub-pages found on [{url.lower()}](https://www.{url.lower()}):\n\n"

    # Add each URL as a markdown list item
    for url in sub_pages:
        markdown += f"1. [{url}]({url})\n"

    return markdown


def navigate_subpages(page, sub_pages):
    for s in sub_pages:
        page.goto(s)
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(2000)


def create_whitehouse_report():
    with sync_playwright() as p:
        # Launch a browser instance
        # Set to True for headless mode
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(record_video_dir="recordings/wh/")
        page.goto("https://www.whitehouse.gov")
        sub_pages = page.evaluate("""
            Array.from(document.querySelectorAll('a'))
                .map(anchor => anchor.href)
                .filter(href => href.includes('whitehouse.gov') && !href.endsWith('#'))
        """)
        sub_pages = list(set(sub_pages))

        markdown_report = generate_markdown_report(sub_pages, "WhiteHouse.gov")
        print(markdown_report)
        today_str = datetime.now().strftime("%d-%m-%Y")
        filename = f"{today_str}-WhiteHouse_SubPages_Report.md"

        with open(f"reports/{filename}", "w") as file:
            file.write(markdown_report)

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(2000)

        navigate_subpages(page, sub_pages)

        # Close the browser
        browser.close()


def create_cdc_report():
    with sync_playwright() as p:
        # Launch a browser instance
        # Set to True for headless mode
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(record_video_dir="recordings/cdc/")

        # Go to whitehouse.gov
        page.goto("https://www.cdc.gov/")

        # Execute JavaScript to collect all sub-page URLs from anchor tags
        sub_pages = page.evaluate("""
            Array.from(document.querySelectorAll('a'))
                .map(anchor => anchor.href)
                .filter(href => href.includes('cdc.gov') && !href.endsWith('#'))
        """)
        sub_pages = list(set(sub_pages))

        markdown_report = generate_markdown_report(sub_pages, "CDC.gov")
        print(markdown_report)
        today_str = datetime.now().strftime("%d-%m-%Y")
        filename = f"{today_str}-CDC_SubPages_Report.md"

        # Save the markdown report to a file with the generated filename
        with open(f"reports/{filename}", "w") as file:
            file.write(markdown_report)

        # Scroll to the bottom of the page
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        # Wait for 2 seconds to simulate natural scrolling
        page.wait_for_timeout(2000)

        # Scroll back to the top of the page
        page.evaluate("window.scrollTo(0, 0)")
        # Wait for 2 seconds to simulate natural scrolling
        page.wait_for_timeout(2000)

        # Close the browser
        browser.close()


if __name__ == "__main__":
    create_whitehouse_report()
    create_cdc_report()
