
import requests
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# Website URL
BASE_URL = "https://quotes.toscrape.com/"


# ==========================================
# FETCH QUOTES FROM WEBSITE
# ==========================================

def scrape_quotes(number_of_pages):

    all_quotes = []

    current_url = BASE_URL

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print("\nConnecting to website...")

    for page in range(number_of_pages):

        try:

            response = requests.get(
                current_url,
                headers=headers,
                timeout=15
            )

            # Check HTTP response
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            quote_blocks = soup.find_all(
                "div",
                class_="quote"
            )

            if not quote_blocks:
                print("No more quotes found.")
                break

            # Extract information
            for block in quote_blocks:

                quote_text = block.find(
                    "span",
                    class_="text"
                )

                author = block.find(
                    "small",
                    class_="author"
                )

                tags = block.find_all(
                    "a",
                    class_="tag"
                )

                quote_data = {

                    "quote": quote_text.get_text(strip=True)
                    if quote_text else "",

                    "author": author.get_text(strip=True)
                    if author else "Unknown",

                    "tags": [
                        tag.get_text(strip=True)
                        for tag in tags
                    ]

                }

                all_quotes.append(quote_data)

            print(
                f"Page {page + 1}: "
                f"{len(quote_blocks)} quotes extracted."
            )

            # Find next page
            next_button = soup.find(
                "li",
                class_="next"
            )

            if next_button:

                next_link = next_button.find("a")

                if next_link:
                    current_url = urljoin(
                        current_url,
                        next_link["href"]
                    )
                else:
                    break

            else:
                break

            # Avoid sending requests too quickly
            time.sleep(1)

        except requests.exceptions.Timeout:

            print("Request timed out.")
            break

        except requests.exceptions.ConnectionError:

            print("Unable to connect to the website.")
            break

        except requests.exceptions.HTTPError as error:

            print("HTTP error:", error)
            break

        except requests.exceptions.RequestException as error:

            print("Request failed:", error)
            break

    return all_quotes


# ==========================================
# DISPLAY SCRAPED QUOTES
# ==========================================

def display_quotes(quotes):

    if not quotes:

        print("No quotes available.")
        return

    print("\n===== SCRAPED QUOTES =====")

    for index, item in enumerate(quotes, start=1):

        print(f"\nQuote {index}")

        print("Text:", item["quote"])

        print("Author:", item["author"])

        print("Tags:", ", ".join(item["tags"]))


# ==========================================
# SAVE DATA AS TEXT FILE
# ==========================================

def save_as_text(quotes):

    with open(
        "quotes.txt",
        "w",
        encoding="utf-8"
    ) as file:

        for index, item in enumerate(quotes, start=1):

            file.write(f"Quote {index}\n")

            file.write(item["quote"] + "\n")

            file.write(
                "Author: " + item["author"] + "\n"
            )

            file.write(
                "Tags: " + ", ".join(item["tags"]) + "\n"
            )

            file.write("-" * 60 + "\n")

    print("\nQuotes saved successfully in quotes.txt!")


# ==========================================
# SAVE DATA AS JSON FILE
# ==========================================

def save_as_json(quotes):

    with open(
        "quotes.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            quotes,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Quotes saved successfully in quotes.json!")


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("\n====================================")
    print("       WEB SCRAPER APPLICATION")
    print("====================================")

    while True:

        print("\n1. Scrape Quotes")
        print("2. Display Scraped Quotes")
        print("3. Save as Text File")
        print("4. Save as JSON File")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":

            while True:

                try:

                    pages = int(
                        input("Enter number of pages to scrape (1-10): ")
                    )

                    if 1 <= pages <= 10:
                        break

                    print("Please enter a number between 1 and 10.")

                except ValueError:

                    print("Please enter a valid whole number.")

            quotes = scrape_quotes(pages)

            print(
                f"\nTotal quotes extracted: {len(quotes)}"
            )

            # Keep extracted data available
            main.quotes = quotes

        elif choice == "2":

            quotes = getattr(main, "quotes", [])

            display_quotes(quotes)

        elif choice == "3":

            quotes = getattr(main, "quotes", [])

            if quotes:
                save_as_text(quotes)
            else:
                print("Please scrape quotes first.")

        elif choice == "4":

            quotes = getattr(main, "quotes", [])

            if quotes:
                save_as_json(quotes)
            else:
                print("Please scrape quotes first.")

        elif choice == "5":

            print("\nThank you for using Web Scraper!")
            print("Goodbye!")

            break

        else:

            print("Invalid choice! Select between 1 and 5.")


# Run application
if __name__ == "__main__":

    main()
