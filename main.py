import requests
import csv
import os
import re
import sys
import argparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import urllib.parse

def scrape_wikipedia_tables(url, timeout, user_agent):
    # Get the directory name from the URL
    parsed_url = urllib.parse.urlparse(url)
    directory_name = parsed_url.path.strip("/").replace("/", "-") or "root"

    # Create a folder using the directory name
    os.makedirs(directory_name, exist_ok=True)

    # Send a GET request to the Wikipedia page
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": user_agent})
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Error: The requested Wikipedia page '{url}' does not exist.")
        else:
            print(f"Error: Failed to fetch the Wikipedia page '{url}'.\n{str(e)}")
        return
    except requests.RequestException as e:
        print(f"Error: Failed to fetch the Wikipedia page '{url}'.\n{str(e)}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the tables in the page
    tables = soup.find_all("table")
    num_tables = len(tables)

    # Initialize the progress bar
    progress_bar = tqdm(total=num_tables, desc=f"Scraping Tables for '{url}'")

    # Iterate over each table
    for index, table in enumerate(tables):
        # Get the table heading
        heading = table.caption.get_text() if table.caption else f"Table {index + 1}"

        # Sanitize the heading for use as a file name
        file_name = sanitize_file_name(heading)

        # Create a CSV file for the current table
        file_path = os.path.join(directory_name, f"{file_name}.csv")
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Extract the table data and write it to the CSV file
            rows = table.find_all("tr")
            for row in rows:
                csv_row = [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
                writer.writerow(csv_row)

        progress_bar.update(1)
        progress_bar.set_postfix({"Table": heading})

    progress_bar.close()
    print(f"\nScraping completed for '{url}'. {num_tables} table(s) extracted.")



def sanitize_file_name(heading):
    # Remove invalid characters for file names
    sanitized_heading = re.sub(r'[<>:"/\\|?*]', "", heading)

    # Trim leading and trailing spaces and dots
    sanitized_heading = sanitized_heading.strip(" .")

    return sanitized_heading


def validate_url(url):
    # Check if the URL is a valid Wikipedia page
    match = re.match(r"https?://en\.wikipedia\.org/wiki/[\w()]+", url)
    return bool(match)


def read_urls_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            urls = file.read().splitlines()
            return urls
    except IOError as e:
        print(f"Error: Failed to read the URL file '{file_path}'.\n{str(e)}")
        sys.exit(1)


def main():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Scrape Wikipedia tables")
    parser.add_argument("--url", type=str, help="URL of the Wikipedia page")
    parser.add_argument("--timeout", "-T", type=int, default=15, help="Timeout value for the HTTP request (in seconds)")
    parser.add_argument("--user_agent", "-UA", type=str, default="requests", help="User-Agent header value")
    parser.add_argument("--file", type=str, help="Path to a file containing multiple URLs (one per line)")

    args = parser.parse_args()

    if args.file:
        # Read URLs from file
        urls = read_urls_from_file(args.file)
        for url in urls:
            if validate_url(url):
                scrape_wikipedia_tables(url, args.timeout, args.user_agent)
                time.sleep(1)  # Pause for 1 second before processing the next URL
                print("\n")  # Clear console
            else:
                print(f"Error: Invalid Wikipedia page URL '{url}'")
    elif args.url:
        # Validate the URL
        if not validate_url(args.url):
            print("Error: Invalid Wikipedia page URL.")
            sys.exit(1)

        # Scrape the tables and save them as separate CSV files
        scrape_wikipedia_tables(args.url, args.timeout, args.user_agent)
    else:
        print("Error: Please provide either --url or --file argument.")
        sys.exit(1)


if __name__ == "__main__":
    main()
