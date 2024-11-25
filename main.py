import os
from playwright.sync_api import sync_playwright
from datetime import datetime


gov_urls = {
    "White House": "https://www.whitehouse.gov",
    "USA": "https://www.usa.gov",
    "Library of Congress": "https://www.loc.gov",
    "Defense": "https://www.defense.gov",
    "US Army": "https://www.army.mil",
    "US Navy": "https://www.navy.mil",
    "US Air Force": "https://www.af.mil",
    "State": "https://www.state.gov",
    "Justice": "https://www.justice.gov",
    "DHS": "https://www.dhs.gov",
    "Department of the Treasury": "https://www.treasury.gov",
    "Health and Human Services": "https://www.hhs.gov",
    "CDC": "https://www.cdc.gov",
    "Department of Education": "https://www.ed.gov",
    "Veterans Affairs": "https://www.va.gov",
    "Environmental Protection Agency": "https://www.epa.gov",
    "National Institutes of Health": "https://www.nih.gov",
    "National Science Foundation": "https://www.nsf.gov",
    "US Geological Survey": "https://www.usgs.gov",
    "IRS": "https://www.irs.gov",
    "Federal Reserve": "https://www.federalreserve.gov",
    "Securities and Exchange Commission": "https://www.sec.gov",
    "Small Business Administration": "https://www.sba.gov",
    "Social Security Administration": "https://www.ssa.gov",
    "FEMA": "https://www.fema.gov",
    "TSA": "https://www.tsa.gov",
    "US Citizenship and Immigration Services": "https://www.uscis.gov"
}


def handle_current_dir(root: str = "reports") -> str:
    dates = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sept",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }
    today_str = datetime.now().strftime("%d-%m-%Y")
    mnth_dir = dates[int(today_str.split('-')[1])]
    folder_path = f"{root}/{mnth_dir}-{int(today_str.split('-')[2])}/"
    if int(today_str.split('-')[0]) == 1:
        os.makedirs(folder_path)
    fin_path = folder_path+today_str
    os.makedirs(fin_path)

    return fin_path


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
        page = browser.new_page(record_video_dir=f"{rec_path}/{name}", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
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
        browser.close()

    return len(sub_pages)


if __name__ == "__main__":
    today_str = datetime.now().strftime("%d-%m-%Y")
    folder_path = handle_current_dir()
    rec_path = handle_current_dir('recordings')
    errs = 0
    tot = 0
    print(f"{'*'*50}\n{' '*16}{today_str} Scan{' '*20}\n{'*'*50}\n")
    for k, v in gov_urls.items():
        try:
            sp = navigate_pages(k, v, folder_path, rec_path)
            print(f"- {k} found with {sp} sub pages.")
            tot += sp
        except Exception as e:
            print(f"Issue navigating to {v}")
            print(e)
            errs += 1
            continue
    print(f"Scan compelete with {tot} pages found & {errs} errors.")
