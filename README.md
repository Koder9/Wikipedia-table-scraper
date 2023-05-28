# Wikipedia Table Scraper

## Description
The Wikipedia Table Scraper is a Python script that allows you to scrape tables from Wikipedia pages and save them as separate CSV files. It uses the BeautifulSoup library to parse HTML content and retrieve table data.

## Usage
The script can be run from the command line with the following options:

1. Scrape tables from a single Wikipedia page:
$ python main.py --url <Wikipedia page URL>

2. Scrape tables from multiple Wikipedia pages specified in a file:
$ python main.py --file <path to URL file>

## Arguments
- `--url`: The URL of the Wikipedia page from which tables will be scraped.
- or
- `--file`: The path to a file containing multiple Wikipedia page URLs (one URL per line).

## Optional Arguments
- `--timeout`, `-T`: Timeout value for the HTTP request in seconds (default: 15).
- `--user_agent`, `-UA`: User-Agent header value to be used in the HTTP request (default: "requests").

## Output
The script creates a separate folder for each Wikipedia page based on the URL's directory name. Inside each folder, it saves the scraped tables as individual CSV files. The file names are derived from the table headings.

## Dependencies
The script requires the following Python libraries:
- requests
- beautifulsoup4
- tqdm

## Examples
1. Scrape tables from a single Wikipedia page:
$ python main.py --url https://en.wikipedia.org/wiki/List_of_schools_in_Karachi

2. Scrape tables from multiple Wikipedia pages specified in a file:
$ python main.py --file urls.txt

**Note:**
- Make sure to provide valid Wikipedia page URLs. The script validates the URLs before scraping.
- If a URL is invalid or the page does not exist, the script will display an error message.
