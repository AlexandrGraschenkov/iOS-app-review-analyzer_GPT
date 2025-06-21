from google_play_scraper import app
import json
from datetime import datetime

def parse_date(date_input):
    """Convert Android date format 'Aug 7, 2022' or datetime object to '2022-08-07'"""
    if not date_input:
        return ''
    
    try:
        # Try to parse the date string like 'Aug 7, 2022'
        parsed_date = datetime.strptime(date_input, '%b %d, %Y')
        return parsed_date.strftime('%Y-%m-%d')
    
    except ValueError:
        return ""

def __load_android_app_info(country: str, app_id: str) -> dict:
    try:
        result = app(
            app_id,
            lang='en',
            country=country
        )
        
        if result:
            app_info_dict = {
                'name': result.get('title', ''),
                'description': result.get('description', ''),
                'update_history': result.get('recentChanges', 'N/A'),
                'icon': result.get('icon', ''),
                'screenshots': result.get('screenshots', []),
                'release': parse_date(result.get('released', '')),
                'update': parse_date(result.get('lastUpdatedOn', '')),
                'developer': result.get('developer', ''),
                'genre': result.get('genre', ''),
                'installs': result.get('installs', ''),
                'price': result.get('price', 0),
                'free': result.get('free', True),
                'rating': result.get('score', 0),
                'rating_count': result.get('ratings', 0),
                'reviews_count': result.get('reviews', 0)
            }
            return app_info_dict
        else:
            print(f'No results found for Android App ID: {app_id}; Country: {country}')
            return dict()
            
    except Exception as e:
        print(f'Error loading Android app info for {app_id}: {e}')
        return dict()

def load_android_app_info(app_id, save_path=None, try_countries=["us", "gb"]):
    info = None
    for country in try_countries:
        info = __load_android_app_info(country=country, app_id=app_id)
        if "name" in info: 
            break
    
    if save_path and info:
        json.dump(info, open(save_path, "w"))
    return info

if __name__ == "__main__":
    app_id = "io.instories"
    load_android_app_info(app_id, save_path=f"/Users/alex/Downloads/android_{app_id}_app.json") 