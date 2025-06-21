import requests
import json
from tqdm.auto import tqdm
from pathlib import Path
import os

def get_reviews(store, app_id):
    base_url = f"https://itunes.apple.com/{store}/rss/customerreviews"

    def fetch(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad statuses
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return []

    all_reviews = []
    has_next_page = True
    page = 0
    pbar = tqdm(total=10, desc=f"Store {store}, App ID {app_id}", leave=False)
    while has_next_page:
        page += 1
        url = f"{base_url}/page={page}/id={app_id}/sortby=mostrecent/json"
        data = fetch(url)
        if not data: break

        res_data = process_response(data)
        if not res_data: break
        next_page = get_page_number_from_data(data, "next")
        last_page = get_page_number_from_data(data, "last")
        has_next_page = next_page > page
        all_reviews += res_data

        pbar.total = last_page
        pbar.update()
        # print(f"Loaded: {page}/{last_page}")

    return all_reviews

def process_response(data) -> dict:
    reviews = data.get('feed', {}).get('entry')
    if isinstance(reviews, dict):
        reviews = [reviews]
    if not reviews: 
        feed = data.get('feed', {})
        if "author" in feed:
            reviews = [feed]
    
    if not reviews: return None

    result = []
    for elem in reviews:
        elem = Hasher(elem)

        total_rating_obj = elem["im:voteCount"]["label"]
        total_rating = 0
        try:
            total_rating = int(total_rating_obj)
        except:
            # Handle the exception
            continue

        usefull_rating = int(elem["im:voteSum"]["label"])
        useless_rating = total_rating-usefull_rating
        rating = int(elem["im:rating"]["label"])
        review = {
            "author":elem["author"]["name"]["label"],
            "date":elem["updated"]["label"],
            "rating":rating,
            "app_version":elem["im:version"]["label"],
            "title":elem["title"]["label"],
            "content":elem["content"]["label"]
        }

        if usefull_rating > 0:
            review["usefull"] = usefull_rating
        if useless_rating > 0:
            review["useless"] = useless_rating

        result.append(review)

    return result


def get_page_number_from_data(data: dict, name: str) -> int:
    feed = data["feed"]
    if not feed: return -1

    next_page_link = [link["attributes"]["href"] 
                      for link in feed["link"] 
                      if link["attributes"]["rel"] == name][0]
    page_number = get_page_number(next_page_link)
    return page_number

def check_has_next_page(page_number: int, data: dict) -> bool:
    feed = data["feed"]
    if not feed: return False

    next_page_link = [link["attributes"]["href"] 
                      for link in feed["link"] 
                      if link["attributes"]["rel"] == "next"][0]
    next_page_number = get_page_number(next_page_link)
    result = next_page_number == page_number
    return result

def get_page_number(url: str) -> int:
    # Find the starting index of "page="
    start_index = url.find('page=') + len('page=')

    # If "page=" is found, continue to find the page number
    if start_index != -1:
        # Find the end index, which is the next "/" after "page="
        end_index = url.find('/', start_index)

        # Extract the page number using slicing
        if end_index != -1:
            page_number = url[start_index:end_index]
        else:
            # If there is no "/" after "page=", take the rest of the string
            page_number = url[start_index:]

        # Convert the page number to an integer and print it
        page_number = int(page_number)
        return page_number
    else:
        return -1


# for easy access to nested elements
class Hasher(dict):
    # https://stackoverflow.com/a/3405143/190597
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def load_ios_reviews(app_id, save_path=None, stores=["us", "ca", "au", "ru", "it", "in", "fr", "gb", "ua", "jp", "cn", "tw", "my", "de"]):
    reviews = []
    pbar = tqdm(stores)
    for store in pbar:
        pbar.set_description_str(f"Load from store: {store}")
        reviews += get_reviews(store=store, app_id=app_id)
    if save_path:
        json.dump(reviews, open(save_path, "w"), ensure_ascii=False)
    return reviews

if __name__ == "__main__":
    app_id = "6469359134"
    downloads_path = str(Path.home() / "Downloads")
    load_ios_reviews(app_id, save_path=os.path.join(downloads_path, f"appstore_{app_id}_reviews.json"))