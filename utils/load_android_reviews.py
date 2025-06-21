from google_play_scraper import reviews, Sort
import json
from tqdm.auto import tqdm
from pathlib import Path
import os
from utils.load_android_app_info import parse_date

def get_android_reviews(country, app_id, count=300):
    try:
        result, continuation_token = reviews(
            app_id,
            lang='en',
            country=country,
            count=count,
            sort=Sort.NEWEST
        )
        
        reviews_list = []
        for review in result:
            parsed_date = parse_date(review.get('at', ''))
            
            review_dict = {
                "author": review.get('userName', 'Anonymous'),
                "date": parsed_date,
                "rating": review.get('score', 0),
                "app_version": review.get('reviewCreatedVersion', review.get('appVersion','Unknown')),
                "content": review.get('content', '')
            }
            reviews_list.append(review_dict)
        
        return reviews_list
        
    except Exception as e:
        print(f"Error loading reviews for {app_id} from {country}: {e}")
        return []

def load_android_reviews(app_id, save_path=None, countries=["us", "ca", "au", "ru", "it", "in", "fr", "gb", "ua", "jp", "cn", "tw", "my", "de"]):
    all_reviews = []
    pbar = tqdm(countries)
    
    for country in pbar:
        pbar.set_description_str(f"Load Android reviews from: {country}")
        country_reviews = get_android_reviews(country=country, app_id=app_id)
        all_reviews.extend(country_reviews)
    
    if save_path:
        json.dump(all_reviews, open(save_path, "w"), ensure_ascii=False)
    
    return all_reviews

if __name__ == "__main__":
    app_id = "com.whatsapp"
    downloads_path = str(Path.home() / "Downloads")
    load_android_reviews(app_id, save_path=os.path.join(downloads_path, f"android_{app_id}_reviews.json"))