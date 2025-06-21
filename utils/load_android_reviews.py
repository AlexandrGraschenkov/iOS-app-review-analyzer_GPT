from google_play_scraper import reviews, Sort
import json
from tqdm.auto import tqdm
from pathlib import Path
import os
from datetime import datetime

def parse_date(date_input):
    if not date_input:
        return ''
    
    if isinstance(date_input, datetime):
        return date_input.strftime('%Y-%m-%d')
    
    return ""

def get_android_reviews(language, app_id, count=2000):
    try:
        result, continuation_token = reviews(
            app_id,
            lang=language,
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

def load_android_reviews(app_id, save_path=None, languages=["en", "fr", "ru", "it", "hi", "de", "uk", "ja", "zh-CN", "zh-TW", "ms", "es", "pt-BR", "ko", "ar", "tr", "pl", "vi", "id", "th"]):
    all_reviews = []
    pbar = tqdm(languages)
    
    for lang in pbar:
        pbar.set_description_str(f"Load Android reviews from language: {lang}")
        country_reviews = get_android_reviews(language=lang, app_id=app_id)
        all_reviews.extend(country_reviews)
    
    if save_path:
        json.dump(all_reviews, open(save_path, "w"), ensure_ascii=False)
    
    return all_reviews

if __name__ == "__main__":
    app_id = "io.instories"
    downloads_path = str(Path.home() / "Downloads")
    load_android_reviews(app_id, save_path=os.path.join(downloads_path, f"android_{app_id}_reviews.json"),languages=["en", "ru"])