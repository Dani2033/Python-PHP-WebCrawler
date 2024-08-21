import sys
import requests
from bs4 import BeautifulSoup
import re
import os

def fetch_entries_from_web(url, limit=30):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all('tr', class_='athing', limit=limit)
    except (requests.RequestException, requests.ConnectionError) as e:
        print(f"Error fetching from the web: {e}. Using local backup instead.", file=sys.stderr)
        return None

def fetch_entries_from_file(file_path, limit=30):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
            return soup.find_all('tr', class_='athing', limit=limit)
    else:
        print(f"Local backup file not found: {file_path}", file=sys.stderr)
        return []

def clean_title(title):
    # Removes symbols from the title and counts only spaced words.
    # Use regex to replace non-alphabetical characters with a space
    cleaned_title = re.sub(r'[^a-zA-Z\s]', '', title)
    return cleaned_title

def parse_entry(entry):
    # Parses a single entry to extract relevant information.
    try:
        # Extract the number
        number_tag = entry.find('span', class_='rank')
        number = number_tag.text.strip('.') if number_tag else 'N/A'

        # Extract the title
        title_tag = entry.find('span', class_='titleline')
        unwanted_link = title_tag.find('span', class_='sitebit comhead')
        if unwanted_link:
            unwanted_link.extract()
        title = title_tag.text if title_tag else 'No title available'

        # Clean the title and count the words
        cleaned_title = clean_title(title)
        word_count = len(cleaned_title.split())

        # Find the sibling 'tr' that contains points and comments
        subtext = entry.find_next_sibling('tr').find('td', class_='subtext')

        # Extract the points
        points_tag = subtext.find('span', class_='score') if subtext else None
        points = int(points_tag.text.split()[0]) if points_tag else 0

        # Extract the number of comments
        comments_tag = subtext.find_all('a')[-1] if subtext else None
        comments = int(comments_tag.text.split()[0]) if comments_tag and 'comment' in comments_tag.text else 0

        return {
            'number': number,
            'title': title,
            'points': points,
            'comments': comments,
            'word_count': word_count
        }
    except Exception as e:
        print(f"An error occurred while processing entry: {e}", file=sys.stderr)
        return None
    
def determine_sort_order(order_by_direction):
    # Determine the boolean value for sorting order based on direction.
    if order_by_direction.lower() == "descending":
        return True
    elif order_by_direction.lower() == "ascending":
        return False
    else:
        raise ValueError("Invalid value for order_by_direction. Use 'ascending' or 'descending'.")

def filter_and_sort_entries(data, filter_type, filter_type_length, order_by, order_by_direction):
    # Filters and sorts entries based on the specified criteria.
    if filter_type == 'more_than':
        filtered_data = [d for d in data if d['word_count'] > filter_type_length]
        filtered_data.sort(key=lambda x: x[order_by], reverse=order_by_direction)
    elif filter_type == 'less_or_equal':
        filtered_data = [d for d in data if d['word_count'] <= filter_type_length]
        filtered_data.sort(key=lambda x: x[order_by], reverse=order_by_direction)
    else:
        filtered_data = data
    return filtered_data

def main():
    # Get parameters from command line
    filter_type = sys.argv[1]                               # 'more_than' or 'less_or_equal'
    filter_type_length = int(sys.argv[2])                   # length of the filter type (int)
    order_by = sys.argv[3]                                  # 'comments' or 'points'
    order_by_direction = determine_sort_order(sys.argv[4])  # 'True' descending or 'False' ascending

    # URL of the website
    url = "https://news.ycombinator.com/"
    backup_file = os.path.dirname(__file__) + "/hackerNewsExample.html"

    # Fetch and parse entries
    entries = fetch_entries_from_web(url)

    if not entries:  # If the web fetch failed, use the local backup file
        entries = fetch_entries_from_file(backup_file)

    data = [parse_entry(entry) for entry in entries if parse_entry(entry)]

    filtered_data = filter_and_sort_entries(data, filter_type, filter_type_length, order_by, order_by_direction)

    # Print the filtered and sorted results
    for entry in filtered_data:
        print(f"{entry['number']}. Title: {entry['title']}")
        print(f"Points: {entry['points']} | Comments: {entry['comments']}\n")

if __name__ == "__main__":
    main()
