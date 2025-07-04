import argparse, os
from utils.analyzer import gpt_models, GPTWrapper
from utils.load_app_info import load_ios_app_info
from utils.load_reviews import load_ios_reviews
from utils.load_android_app_info import load_android_app_info
from utils.load_android_reviews import load_android_reviews
from utils.create_html import create_html
from utils.sensortower import get_revenue_and_downloads

def parse_arguments():
    parser = argparse.ArgumentParser(description='Python script localize your application powered with GPT.')
    
    parser.add_argument('--gpt_api_key',
                        type=str,
                        required=True,
                        help='Your GPT API key')
    
    list_models = ", ".join(list(gpt_models.keys()))
    parser.add_argument('--gpt_model',
                        type=str,
                        default="gpt-4.1-mini",
                        help=f'Choose model from: {list_models}')
    
    parser.add_argument('--app_ids',
                        type=str,
                        required=True,
                        help='Array of Apps IDs: "1620725834,1448868559"')
    
    parser.add_argument('--stores',
                        type=str,
                        default="us,ca,au,ru,it,in,fr,gb,ua,jp,cn,tw,my,de,kr,br,mx,es,sa,ae,vn,tr",
                        help='Array of Stores: "us,it"; Only for AppStore')
    
    parser.add_argument('--with_app_description',
                        action='store_true',
                        help='By default do not use app description for analyzing only user reviews')
    
    save_folder = os.path.join(os.path.dirname(__file__), "temp")
    parser.add_argument('--save_folder',
                        type=str,
                        default=save_folder,
                        help='Where to save final HTML')
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    gpt = GPTWrapper(api_key=args.gpt_api_key, model=args.gpt_model)
    if not gpt: exit

    app_ids = args.app_ids.split(",")
    app_ids = [x for x in app_ids if len(x)>0]
    app_ids = [x.strip() for x in app_ids]
    stores = args.stores.split(",")
    stores = [x.strip() for x in stores]

    for app_id in app_ids:
        is_appstore = app_id.isdigit() and len(app_id) > 5
        print(f"Load app info: {app_id} ({'AppStore' if is_appstore else 'GooglePlay'})")

        if is_appstore:
            app_info = load_ios_app_info(app_id)
        else:
            app_info = load_android_app_info(app_id)
            
        if "name" in app_info:
            print(f"Info loaded for app: {app_info['name']};\nStart load reviews..")
        else:
            print(f"Can't load app info: {app_id}; Break")
            continue

        if is_appstore:
            app_reviews = load_ios_reviews(app_id, stores=stores)
            app_info["reviews_count"] = len(app_reviews)
        else:
            app_reviews = load_android_reviews(app_id)
            
        if len(app_reviews) > 5:
            print(f"{len(app_reviews)} reviews of the app have been downloaded; Start analyzing..")
        else:
            print(f"There are not enough reviews to analyze the app. You can look at them yourself.\n{app_reviews}")
            print("Break!")
            continue
        
        process_app_info = app_info.copy()
        process_app_info.pop('icon', None)
        process_app_info.pop('screenshots', None)
        process_app_info.pop('description', None) # With description it take Pros from it

        # reviews with more symbols othen cares more info about app
        app_reviews.sort(key=lambda x: (len(x["content"]) + len(x.get("title", ""))), reverse=True)
        app_reviews = app_reviews[:500] # seams useless to process more than 500 reviews
        app_reviews.sort(key=lambda x: (x["date"]), reverse=True)
        reviews_to_process = [review.copy() for review in app_reviews]
        for review in reviews_to_process:
            review.pop('author', None)
            review.pop('date', None)
        analysis = gpt.process_reviews(app_info=process_app_info, reviews=reviews_to_process)
        sensor_info = get_revenue_and_downloads(app_id=app_id)
        # analysis = gpt.get_debug_analysis()

        print(f"Analyze is done:\n{analysis}")
        print(f"Prepare HTML..")

        dir_path = os.path.abspath(args.save_folder)
        os.makedirs(dir_path, exist_ok=True)
        platform_prefix = "ios" if is_appstore else "android"
        name = f"{platform_prefix}_{app_id}_{app_info['name']}.html"
        name = name.replace(" ", "_")
        file_name = os.path.join(dir_path, name)
        create_html(app_analysis=analysis["app_analysis"], 
                    app_info=app_info, 
                    app_reviews=app_reviews, 
                    sensortower_info=sensor_info, 
                    save_to_path=file_name,
                    app_id=app_id,
                    is_appstore=is_appstore)
        print(f"Done: {app_info['name']};\nResult saved to: {file_name}")
        

if __name__ == '__main__':
    main()
