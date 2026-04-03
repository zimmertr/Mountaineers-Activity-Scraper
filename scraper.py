import argparse
import requests
from sheet_manager import SheetManager
import time
from datetime import datetime
from date_utils import DateFormatter
from scraper_utils import Scraper


def read_urls(filename):
    try:
        with open(filename) as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {filename}", flush=True)
        return []


def build_row(html, url):
    scraper = Scraper(html)
    raw_name = scraper.scrape_element_text("h1")
    type_name = ""
    clean_name = raw_name
    if " - " in raw_name:
        type_name, clean_name = raw_name.split(" - ", 1)
    date_str = scraper.scrape_date_range()
    start_date, end_date = DateFormatter.parse_dates(date_str)
    reg_open = scraper.scrape_from_ul_details("Registration Open", tag_type="label")
    reg_open_fmt = DateFormatter.format_registration_open(reg_open)
    reg_closed = scraper.scrape_from_ul_details("Registration Closed", tag_type="label")
    reg_closed_fmt = DateFormatter.format_registration_open(reg_closed)
    reg_nonpriority = scraper.scrape_from_ul_details("Non-Priority Registration Open", tag_type="label")
    reg_nonpriority_fmt = DateFormatter.format_registration_date(reg_nonpriority)
    return [
        url,
        type_name,
        clean_name,
        scraper.scrape_element_text("p", "documentDescription"),
        scraper.scrape_primary_leader(),
        start_date,
        end_date,
        scraper.scrape_from_ul_details("Committee", tag_type="label", extract_tag="a"),
        reg_open_fmt,
        reg_nonpriority_fmt,
        reg_closed_fmt,
        scraper.scrape_from_ul_details("Mileage", tag_type="strong", extract_tag="span"),
        scraper.scrape_from_ul_details("Elevation Gain", tag_type="strong", extract_tag="span"),
        scraper.scrape_from_ul_details("Availability", tag_type="label").split("(")[0].strip(),
        scraper.scrape_from_ul_details("Availability", tag_type="label", extract_tag="span"),
        scraper.scrape_element_text("div", "content-text", find_child="div", skip_label=True)
    ]


def main():
    parser = argparse.ArgumentParser(description="Scrape trip data and write to Google Sheet")
    parser.add_argument("--file", required=True, help="Text file with URLs")
    parser.add_argument("--sheet", required=True, help="Google Sheet name")
    parser.add_argument("--creds", required=True, help="Service account JSON file")
    args = parser.parse_args()

    urls = read_urls(args.file)
    if not urls:
        print("No URLs found", flush=True)
        return


    HEADERS = [
        "URL", "Type", "Name", "Description", "Leader", "Start Date", "End Date", "Committee",
        "Registration Open", "Non-Priority Registration Open", "Registration Closed",
        "Mileage", "Elevation Gain", "Availability", "Capacity", "Leader's Notes",
        "Last Updated (UTC)"
    ]
    sheet_manager = SheetManager(args.sheet, args.creds, HEADERS)

    for idx, url in enumerate(urls, start=1):
        print(f"[{idx}/{len(urls)}] Processing: {url}", flush=True)
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            row_data = build_row(resp.text, url)
            sheet_manager.write_row(row_data)
            time.sleep(1)  # rate limit
        except Exception as e:
            print(f"Failed to process {url}: {e}", flush=True)


if __name__ == "__main__":
    main()