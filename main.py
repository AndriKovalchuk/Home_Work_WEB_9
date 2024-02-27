import json

import requests
from bs4 import BeautifulSoup


def parse_authors_data():
    authors_store = []
    processed_authors = set()

    for page_number in range(1, 11):
        main_url = f"https://quotes.toscrape.com/page/{page_number}/"
        response = requests.get(main_url)
        soup_main = BeautifulSoup(response.text, "lxml")

        authors = soup_main.find_all("small", class_="author")

        for author in authors:
            author_name = author.text.strip()

            if author_name not in processed_authors:
                author_name_url = (
                    author_name.replace(". ", " ")
                    .replace(".", "-")
                    .replace(" ", "-")
                    .replace("'", "")
                    .replace("é", "e")
                    .rstrip("-")
                )
                author_info_url = (
                    f"https://quotes.toscrape.com/author/{author_name_url}/"
                )
                response_author_info = requests.get(author_info_url)
                soup_author_info = BeautifulSoup(response_author_info.text, "lxml")

                born_date = soup_author_info.find(
                    "span", class_="author-born-date"
                ).text.strip()
                born_location = soup_author_info.find(
                    "span", class_="author-born-location"
                ).text.strip()
                description = soup_author_info.find(
                    "div", class_="author-description"
                ).text.strip()

                author_info = {
                    "fullname": author_name,
                    "born_date": born_date,
                    "born_location": born_location,
                    "description": description,
                }
                authors_store.append(author_info)
                processed_authors.add(author_name)

    return authors_store


def parse_quotes_data():
    quotes_store = []

    for page_number in range(1, 11):
        url = f"https://quotes.toscrape.com/page/{page_number}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            quote_text = quote.find("span", class_="text").text.strip()
            tags = [tag.text.strip() for tag in quote.find_all("a", class_="tag")]
            author = quote.find("small", class_="author").text.strip()

            quote_info = {
                "tags": tags,
                "author": author,
                "quote": quote_text,
            }
            quotes_store.append(quote_info)

    return quotes_store


if __name__ == "__main__":
    with open("authors.json", "w", encoding="utf-8") as fd:
        json.dump(parse_authors_data(), fd, ensure_ascii=False)

    with open("quotes.json", "w", encoding="utf-8") as fd:
        json.dump(parse_quotes_data(), fd, ensure_ascii=False)
