import json
import csv
from milestone_2.configs import config

JSON_FILE_NAME = "./utils/json_book_collection.json"
CSV_FILE_NAME = "./utils/csv_book_collection.csv"
MISSING_BOOK_MESSAGE = "\"{name}\" is not found in your book collection."
books = []


def save_collection_to_file(book_collection):
    if config.DATA_TYPE == "csv":
        _save_collection_to_csv_file(book_collection)
    elif config.DATA_TYPE == "json":
        _save_collection_to_json_file(book_collection)


def load_collection_from_file():
    if config.DATA_TYPE == "csv":
        _load_collection_from_csv_file()
    elif config.DATA_TYPE == "json":
        _load_collection_from_json_file()


def _save_collection_to_csv_file(book_collection):
    with open(CSV_FILE_NAME, "w", newline="") as file:
        if len(book_collection) > 0:
            writer = csv.DictWriter(file, fieldnames=list(book_collection[0].keys()))
            writer.writeheader()
            writer.writerows(book_collection)


def _load_collection_from_csv_file():
    global books
    try:
        with open(CSV_FILE_NAME, "r") as file:
            books = list(csv.DictReader(file))
    except FileNotFoundError:
        with open(CSV_FILE_NAME, "w"):  # create empty file if it doesn't exist
            pass


def _save_collection_to_json_file(book_collection):
    with open(JSON_FILE_NAME, "w") as file:
        json.dump(book_collection, file)


def _load_collection_from_json_file():
    global books
    try:
        with open(JSON_FILE_NAME, "r") as file:
            books = json.load(file)
    except FileNotFoundError:
        with open(JSON_FILE_NAME, "w") as file:  # create empty file if it doesn't exist and add empty [] to avoid JSONDecodeError when reading empty file
            json.dump([], file)


def add_book(name, author):
    books.append({'name': name, 'author': author, 'read': False})
    save_collection_to_file(books)
    print(f"\"{name}\" by {author} was added to your book collection successfully!")


def get_book_collection():
    return books


def mark_book_as_read(name):
    for book in books:
        if book['name'].lower() == name.lower():
            book['read'] = True
            save_collection_to_file(books)
            print(f"\"{name}\" was marked as 'Read' in your book collection successfully!")
            return

    print(MISSING_BOOK_MESSAGE.format(name=name))


def delete_book(name):
    global books
    for book in books:
        if book['name'].lower() == name.lower():
            books = [book for book in books if book['name'].lower() != name.lower()]
            save_collection_to_file(books)
            print(f"\"{name}\" was deleted from your book collection successfully!")
            return

    print(MISSING_BOOK_MESSAGE.format(name=name))
