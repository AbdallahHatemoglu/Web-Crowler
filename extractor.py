import os
import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urlparse, urljoin

# Define the starting URL
starting_url = ""
base_dir = "web_crawler_output"

# Create directories for resource types if they don't exist
resource_types = ["images", "stylesheets", "javascript", "others"]

for resource_type in resource_types:
    os.makedirs(os.path.join(base_dir, resource_type), exist_ok=True)

# Initialize dictionaries to store resource URLs
resource_urls = {resource_type: [] for resource_type in resource_types}


# Function to download and store a resource
def download_resource(url, resource_type):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Generate a filename based on the URL
        filename = os.path.basename(urlparse(url).path)

        # Determine the directory to save the resource based on its type
        resource_dir = os.path.join(base_dir, resource_type)

        # Save the resource to the appropriate directory
        with open(os.path.join(resource_dir, filename), "wb") as f:
            f.write(response.content)

        # Add the resource URL to the corresponding list in the dictionary
        resource_urls[resource_type].append(url)

    except Exception as e:
        print(f"Failed to download {url}: {e}")


# Function to extract and store resources from a page
def extract_and_store_resources(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract image links
        img_links = [urljoin(url, link['src']) for link in soup.find_all('img', src=True)]

        # Extract CSS links
        css_links = [urljoin(url, link['href']) for link in soup.find_all('link', href=True, rel='stylesheet')]

        # Extract JavaScript links
        js_links = [urljoin(url, link['src']) for link in soup.find_all('script', src=True)]

        # Extract other links (e.g., PDF, DOCX, XLSX)
        other_links = [urljoin(url, link['href']) for link in soup.find_all(href=re.compile(r'\.(pdf|docx|xlsx)$'))]

        # Download and store the resources
        for img_link in img_links:
            download_resource(img_link, "images")

        for css_link in css_links:
            download_resource(css_link, "stylesheets")

        for js_link in js_links:
            download_resource(js_link, "javascript")

        for other_link in other_links:
            download_resource(other_link, "others")

    except Exception as e:
        print(f"Failed to crawl {url}: {e}")


# Generate and save the report
report_filename = os.path.join(base_dir, "crawler_report.json")
with open(report_filename, "w") as report_file:
    json.dump(resource_urls, report_file, indent=4)

print("Crawling and resource extraction completed.")
