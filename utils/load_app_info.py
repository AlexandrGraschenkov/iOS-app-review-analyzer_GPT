import requests
import json

def __load_app_info(store: str, app_id: str) -> dict:
    # App Store lookup API URL
    #              https://itunes.apple.com/lookup?id=1460032075
    lookup_url = f'https://itunes.apple.com/lookup?id={app_id}&country={store}'

    # Make a GET request to the API
    response = requests.get(lookup_url)
    
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        results = data.get('results')
        
        if results:
            app_info = results[0]  # Assuming the first result is the app we're looking for
            
            # Retrieve the required information
            app_name = app_info.get('trackName')
            # app_subtitle = app_info.get('subtitle', 'N/A')  # Subtitle might not be available
            app_description = app_info.get('description')
            app_update_history = app_info.get('releaseNotes', 'N/A')  # Update history might not be detailed in the lookup API
            app_icon = app_info.get('artworkUrl512')
            app_screenshots = app_info.get('screenshotUrls', [])
            app_release_date = app_info.get('releaseDate', '').split("T")[0]
            app_update_date = app_info.get('currentVersionReleaseDate', '').split("T")[0]
            if len(app_screenshots) == 0 and len(app_info.get('ipadScreenshotUrls', [])) > 0:
                app_screenshots = app_info.get('ipadScreenshotUrls', [])

            # Prepare the dictionary with the app information
            app_info_dict = {
                'name': app_name,
                # 'subtitle': app_subtitle,
                'description': app_description,
                'update_history': app_update_history,
                'icon': app_icon,
                'screenshots': app_screenshots,
                'release': app_release_date,
                'update': app_update_date
            }
            return app_info_dict
        else:
            raise ValueError('No results found for the provided App ID.')
    else:
        response.raise_for_status()

def load_app_info(app_id, save_path = None, try_stores=["us", "gb"]):
    info = None
    for store in try_stores:
        info = __load_app_info(store=store, app_id=app_id)
        if "name" in info: break
    
    if save_path:
        json.dump(info, open(save_path, "w"))
    return info

if __name__ == "__main__":
    app_id = "1460032075"
    load_app_info(app_id, save_path=f"/Users/alex/Downloads/appstore_{app_id}_app.json")