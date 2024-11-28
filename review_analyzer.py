import argparse, os
from utils.analyzer import gpt_models, GPTWrapper
from utils.load_app_info import load_app_info
from utils.load_reviews import load_reviews
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
                        default="gpt-4o-mini-2024-07-18",
                        help=f'Choose model from: {list_models}')
    
    parser.add_argument('--app_ids',
                        type=str,
                        required=True,
                        help='Array of Apps IDs: "1620725834,1448868559"')
    
    parser.add_argument('--stores',
                        type=str,
                        default="us,ca,au,ru,it,in,fr,gb,ua,jp,cn,tw,my",
                        help='Array of Stores: "us,it"')
    
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
    stores = args.stores.split(",")

    for app_id in app_ids:
        print(f"Load app info: {app_id}")
        app_info = load_app_info(app_id)
        if "name" in app_info:
            print(f"Info loaded for app: {app_info['name']};\nStart load reviews..")
        else:
            print(f"Can't load app info: {app_id}; Break")
            continue

        app_reviews = load_reviews(app_id, stores=stores)
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
        app_reviews.sort(key=lambda x: (len(x["content"]) + len(x["title"])), reverse=True)
        app_reviews = app_reviews[:500] # seams useless to process more than 500 reviews
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
        name = f"app_{app_id}_{app_info['name']}.html"
        name = name.replace(" ", "_")
        file_name = os.path.join(dir_path, name)
        create_html(app_analysis=analysis["app_analysis"], 
                    app_info=app_info, 
                    app_reviews=app_reviews, 
                    sensortower_info=sensor_info, 
                    save_to_path=file_name)
        print(f"Done: {app_info['name']};\nResult saved to: {file_name}")
        

if __name__ == '__main__':
    main()
