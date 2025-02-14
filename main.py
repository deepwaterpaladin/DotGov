import os
from app.navigator import navigate_pages
from app.analytics_engine import create_log
from datetime import datetime, timedelta


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
    "US Citizenship and Immigration Services": "https://www.uscis.gov",
    "FBI":"https://www.fbi.gov",
    "CIA":"https://www.cia.gov",
    "DOGE":"https://doge.gov/"
}


def generate_folder_path(date_str: str) -> str:
    """
    Generate folder path based on the given date string.

    Args:
        date_str (str): Date in format 'dd-mm-YYYY'

    Returns:
        str: Folder path in format 'reports/Mth-Year/dd-MM-YYYY/'
    """
    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
    month_year = date_obj.strftime("%b-%Y")
    folder_path = os.path.join('reports', month_year, date_str)

    return folder_path


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
    try:
        os.makedirs(fin_path)
    except:
        print(f"{fin_path} already exists.\n\n\n")

    return fin_path


if __name__ == "__main__":
    today_str = datetime.now().strftime("%d-%m-%Y")
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")
    today_folder = generate_folder_path(today_str)
    yesterday_folder = generate_folder_path(yesterday_str)
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
    create_log(today_folder, yesterday_folder)
    print(f"Scan compelete with {tot} pages found & {errs} errors.")
