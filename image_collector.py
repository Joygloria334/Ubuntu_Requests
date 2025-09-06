import requests
import os
from urllib.parse import urlparse

# Function to fetch and save a single image
def fetch_image(url):
    try:
        # Community → connect with the wider web community
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Respect → check for HTTP errors

        # Check important headers before saving
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped (not an image): {url}")
            return

        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > 5_000_000:  # limit: 5 MB
            print(f"✗ Skipped (file too large): {url}")
            return

        # Create folder if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)

        # Extract filename or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"

        filepath = os.path.join("Fetched_Images", filename)

        # Prevent duplicates
        if os.path.exists(filepath):
            print(f"✗ Skipped duplicate: {filename}")
            return

        # Save image in binary mode
        with open(filepath, 'wb') as f:
            f.write(response.content)

        # Sharing → saving images neatly for later use
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        # Respect → error handling without crashing
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Allow multiple URLs, separated by commas
    urls = input("Enter image URLs (separated by commas): ").split(",")

    for url in urls:
        url = url.strip()
        if url:  # skip empty strings
            fetch_image(url)

    print("\nConnection strengthened. Community enriched.")
    print('"A person is a person through other persons." - Ubuntu Philosophy')

if __name__ == "__main__":
    main()
