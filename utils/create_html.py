import json
import webbrowser, os, re
import html

def _create_reviews_html_part(reviews):
    review_items = []
    for review in reviews:
        review_content_escaped = html.escape(review['content'])
        review_title_escaped = html.escape(review['title'])
        text = f'''
            <div class="review-item">
                <div class="review-header">
                    <span class="review-rating">{"⭐" * review["rating"]}</span>
                    <span class="review-version">v{review["app_version"]}</span>
                </div>
                <div class="review-meta">
                    <span class="review-author">By {review["author"]}</span>
                    <span class="review-date">{review["date"]}</span>
                </div>
                <div class="review-name">
                    <h3 class="review-title">{review["title"]}</h3>
                    <div class="translation-buttons" data-title="{review_title_escaped}" data-content="{review_content_escaped}">
                        <button onclick="translateWithGoogle()" title="Translate with Google">🌐</button>
                        <button onclick="translateWithYandex()" title="Translate with Yandex">🅨</button>
                        <button onclick="translateWithDeepL()" title="Translate with DeepL">🔤</button>
                    </div>
                </div>
                <p class="review-content">{review["content"]}</p>
            </div>
        '''
        review_items.append(text)

    review_items = ''.join(review_items)
    newline = '\\n'
    return f'''
    <div class="reviews-section">
        <h2>User Reviews</h2>
        <div class="reviews-list">
            {review_items}
        </div>
        <style>
            .reviews-section {{
                margin: 10px;
                padding: 20px;
                background: #fbfbfb;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            }}
            .reviews-section h2 {{
                font-size: 1.5em;
                margin-bottom: 15px;
                color: #333;
                font-weight: 600;
            }}
            .review-item {{
                margin-bottom: 20px;
                padding: 15px;
                border-bottom: 1px solid #e0e0e0;
            }}
            .review-item:last-child {{
                border-bottom: none;
            }}
            .review-header {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 5px;
                font-size: 0.9em;
                color: #666;
            }}
            .review-meta {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
                font-size: 0.85em;
                color: #888;
            }}
            .review-name {{
                display: flex;
                justify-content: space-between;
            }}
            .review-author {{
                font-weight: 600;
            }}
            .review-date {{
                font-style: italic;
            }}
            .review-rating {{
                color: #ffcc00;
            }}
            .review-version {{
                font-style: italic;
            }}
            .review-title {{
                font-size: 1.1em;
                margin: 5px 0 5px;
                color: #222;
                font-weight: 500;
            }}
            .review-content {{
                font-size: 0.95em;
                line-height: 1.5;
                color: #444;
            }}
            .translation-buttons {{
                margin-top: 5px;
                display: flex;
            }}
            .translation-buttons button {{
                margin-right: 5px;
                padding: 5px;
                font-size: 1.2em;
                border: none;
                border-radius: 50%;
                cursor: pointer;
                width: 25px;
                height: 25px;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .translation-buttons button:hover {{
                background-color: #0056b3;
            }}
            .translation-buttons button:focus {{
                outline: none;
            }}
        </style>
        <script>
            function translateWithGoogle() {{
                const container = event.currentTarget.closest('.translation-buttons');
                const title = container.dataset.title;
                const content = container.dataset.content;
                const url = `https://translate.google.com/?sl=auto&text=${{encodeURIComponent(title + '\\n' + content)}}`;
                window.open(url, '_blank');
            }}

            function translateWithYandex() {{
                const container = event.currentTarget.closest('.translation-buttons');
                const title = container.dataset.title;
                const content = container.dataset.content;
                const url = `https://translate.yandex.com/?lang=auto-en&text=${{title + encodeURIComponent('\\n') + content}}`;
                window.open(url, '_blank');
            }}

            function translateWithDeepL() {{
                const container = event.currentTarget.closest('.translation-buttons');
                const title = container.dataset.title;
                const content = container.dataset.content;
                const url = `https://www.deepl.com/en/translator#en/${{title + encodeURIComponent('\\n') + content}}`;
                window.open(url, '_blank');
            }}
        </script>
    </div>
    '''

# HTML content
def _create_html(app_data):
    reviews_html = _create_reviews_html_part(app_data["reviews"])
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{app_data["app_analysis"]["name"]}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                color: #333;
            }}
            .container {{
                width: 80%;
                margin: auto;
                overflow: hidden;
            }}
            header {{
                background: #35424a;
                color: #ffffff;
                padding: 10px 0;
                text-align: center;
            }}
            header h1 {{
                margin: 0;
            }}
            .app-icon {{
                max-width: 100px;
                border: 1px solid #e0e5eb;
                border-radius: 20%;
                margin-right: 20px;
            }}
            .app-details {{
                flex-grow: 1;
            }}
            .row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 10px;
            }}
            .row p {{
                margin: 0;
                font-size: 1.3rem;
                color: #555;
            }}
            .app-header {{
                display: flex;
                align-items: center;
                background: #ffffff;
                margin: 20px 0;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .pros-cons {{
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
            }}
            .pros-cons div {{
                background: #ffffff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 45%;
            }}
            .pros-cons h2 {{
                margin-top: 0px;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin: 5px 0;
            }}
            .screenshots {{
                margin-top: 20px;
                text-align: center;
            }}
            .screenshots img {{
                max-width: 200px;
                margin: 0 10px;
            }}
            footer {{
                background: #35424a;
                color: #ffffff;
                text-align: center;
                padding: 10px 0;
                margin-top: 20px;
            }}
            .reviews {{
                margin-top: 20px;
            }}
            #review-list {{
                display: none;
                margin-top: 10px;
            }}
            #show-reviews-btn {{
                background: #35424a;
                color: #ffffff;
                border: none;
                display: flex;
                padding: 10px 15px;
                cursor: pointer;
                margin-top: 10px;
            }}
            #show-reviews-btn:hover {{
                background: #555;
            }}
        </style>
        <script>
            function toggleReviews() {{
                const reviewList = document.getElementById('review-list');
                const btn = document.getElementById('show-reviews-btn');
                if (reviewList.style.display !== 'block') {{
                    reviewList.style.display = 'block';
                    btn.textContent = 'Hide Reviews';
                }} else {{
                    reviewList.style.display = 'none';
                    btn.textContent = 'Show Reviews';
                }}
            }}
        </script>
    </head>
    <body>
        <header>
            <h1>{app_data["app_analysis"]["name"]}</h1>
        </header>
        <div class="container">
            <div class="app-header">
                <img class="app-icon" src="{app_data["icon"]}" alt="App Icon">
                <div class="app-details">
                    <div class="row">
                        <p><strong>Downloads:</strong> {app_data["downloads"]}</p>
                        <p><strong>Release Date:</strong> {app_data["release"]}</p>
                    </div>
                    <div class="row">
                        <p><strong>Revenue:</strong> {app_data["revenue"]}</p>
                        <p><strong>Last Update:</strong> {app_data["update"]}</p>
                    </div>
                </div>
            </div>
            <p><strong>Why the app is popular:</strong> {app_data["app_analysis"]["why_app_popular"]}</p>
            <div class="pros-cons">
                <div>
                    <h2>Pros</h2>
                    <ul>
                        {''.join(f"<li>• {pro}</li>" for pro in app_data["app_analysis"]["pros"])}
                    </ul>
                </div>
                <div>
                    <h2>Cons</h2>
                    <ul>
                        {''.join(f"<li>• {con}</li>" for con in app_data["app_analysis"]["cons"])}
                    </ul>
                </div>
            </div>
            <p><strong>Suggestions for Improvement:</strong> {app_data["app_analysis"]["suggest_what_improve"]}</p>
            <div class="screenshots">
                <h2>Screenshots</h2>
                {''.join(f'<img src="{screenshot}" alt="Screenshot">' for screenshot in app_data["screenshots"])}
            </div>
            <div class="reviews">
                <button id="show-reviews-btn" onclick="toggleReviews()">Show Reviews</button>
                <ul id="review-list">
                    {reviews_html}
                </ul>
            </div>
        </div>
        <footer>
            <p>&copy; 2024 iOS App Analytics, made by <a href="https://x.com/sharrikk" style="color: white;">Alex Gra 𝕏</a></p>
        </footer>
    </body>
    </html>
    '''
    return html_content

def create_html(app_analysis, app_info, app_reviews, sensortower_info, save_to_path, open_html_page=True):
    # Write the HTML content to a file
    app_data = {
        "app_analysis": app_analysis,
        "icon": app_info["icon"],
        "screenshots": app_info["screenshots"],
        "reviews": app_reviews,
        "update": app_info["update"],
        "release": app_info["release"],
        "downloads": sensortower_info["downloads"],
        "revenue": sensortower_info["revenue"]
    }

    html_content = _create_html(app_data)
    with open(save_to_path, "w") as file:
        file.write(html_content)

    if open_html_page:
        webbrowser.open('file://' + save_to_path)

    print("HTML file has been created successfully.")



# [ DEBUG ]

# Sample JSON data
_example_analytics = '''{
    "name": "Auto Captions for Video\u2014VidCap",
    "pros": [
        "High transcription accuracy",
        "Supports multiple languages",
        "Easy to use and edit captions",
        "Quick processing of videos",
        "Customizable text styles and positions",
        "No watermark on exported videos",
        "Good customer service and developer responsiveness",
        "Local transcription available for use without internet",
        "Ability to handle videos with different accents",
        "Can transcribe and translate simultaneously"
    ],
    "cons": [
        "Some users experience crashes and bugs",
        "Subscription model may be expensive for some users",
        "Trial period may be too short",
        "Some inaccuracies in transcription reported",
        "Limited editing options for caption placement",
        "Some users reported issues with exporting videos",
        "Auto-renewal of subscription may be seen as sneaky",
        "Some features like different styles for separate speakers are missing",
        "May struggle with certain accents or dialects"
    ],
    "suggest_what_improve": "Extend trial period, improve transcription accuracy, enhance editing features, and address app crashes and export issues",
    "why_app_popular": "The app is popular due to its high accuracy in transcription, ease of use, and the ability to customize and edit captions efficiently. Additionally, the lack of watermarks and the ability to handle multiple languages and accents contribute to its popularity."
}'''
_example_app_info = """
{"update": "2024/11/11",
"release": "2022/11/11",
"screenshots":[
    "https://is1-ssl.mzstatic.com/image/thumb/PurpleSource116/v4/a4/56/96/a45696eb-f521-9544-e7f6-0d3ab0e10295/0b3924aa-9136-4863-b19e-0f184dae368e_VCP_ASO_SS_5.5_01.jpg/392x696bb.jpg", 
    "https://is1-ssl.mzstatic.com/image/thumb/PurpleSource126/v4/82/ca/d1/82cad1f2-3732-456a-8e77-1d0c47075727/d284fea0-1122-4cb4-9601-1cbec06c6b43_VCP_ASO_SS_5.5_02.jpg/392x696bb.jpg", 
    "https://is1-ssl.mzstatic.com/image/thumb/PurpleSource116/v4/c9/e1/ee/c9e1ee88-313b-ef5f-717c-66c82a7fd054/7d88312e-21eb-4ba9-a7a8-f7c2d1dd5d80_VCP_ASO_SS_5.5_03.jpg/392x696bb.jpg", 
    "https://is1-ssl.mzstatic.com/image/thumb/PurpleSource126/v4/ee/a8/92/eea8927d-f4c6-94ce-8cd6-f06ec38cc48a/966fc2b5-2bd4-4fe5-ba1c-f9121f1ecfaa_VCP_ASO_SS_5.5_04.jpg/392x696bb.jpg", 
    "https://is1-ssl.mzstatic.com/image/thumb/PurpleSource116/v4/74/72/c5/7472c5b0-6343-5b5b-e6bb-133337ee2dd3/f337b9e2-6505-4370-ab79-7c1bf8dc3303_VCP_ASO_SS_5.5_05.jpg/392x696bb.jpg", 
    "https://is1-ssl.mzstatic.com/image/thumb/PurpleSource116/v4/a4/57/d9/a457d97f-52dd-0b96-6995-bdb6d5f9f0cb/2580441d-bc48-4c0a-9fb8-3159bbc5a5a5_VCP_ASO_SS_5.5_06.jpg/392x696bb.jpg", 
    "https://is1-ssl.mzstatic.com/image/thumb/PurpleSource126/v4/3e/d8/d2/3ed8d242-04b6-789a-1f31-a6f1a20182f5/5d48cc56-cdd9-4f00-b1cb-ca359e8066e3_VCP_ASO_SS_5.5_07.jpg/392x696bb.jpg"
    ], 
"icon":"https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/0e/0a/17/0e0a1734-2679-2665-c2f0-b7a7bf998c6c/AppIcon-0-0-1x_U007emarketing-0-7-0-85-220.png/512x512bb.jpg"}
"""
_example_app_reviews = """
[
  {
    "author": "Billy52",
    "date": "2024-11-16T11:43:40-07:00",
    "rating": 5,
    "app_version": "13.1.5",
    "title": "Sacramento Delta Tour (CA)",
    "content": "A very nice tour. We \\"split\\" it into two weekends. We really looked forward to resuming the tour. The driving directions are super clear, once you leave the mall in which it starts. Nice stories and super clear narration.  Driving on the levies is not for the faint of heart (but we were in a tall, wide van, and a smaller, less tall, and narrower vehicle would be better. The river is just beautiful. We went in early November, so the air was crisp and the leaves were changing. Try to start an hour before lunch, so you can eat at Al\u2019s."
  },
  {
    "author": "macronecole",
    "date": "2024-11-09T01:22:50-07:00",
    "rating": 5,
    "app_version": "13.1.5",
    "title": "Excellent audio guide",
    "content": "Clear and concise information coupled with well incorporated directions, the calm narrator\u2019s voice providing insightful info amidst tourist crowds was much appreciated"
  },
  {
    "author": "taal se",
    "date": "2024-11-03T02:24:12-07:00",
    "rating": 4,
    "app_version": "13.1.0",
    "title": "Apple watch is missed opportunity",
    "content": "The app does not integrate with apple maps and therefore you have to keep looking at the screen to know where to go. Integrating with apple maps would provide turn by turn directions and apple watch making for a much better user experience of the app. Fix this please."
  },
  {
    "author": "Lisztener",
    "date": "2024-11-02T10:29:08-07:00",
    "rating": 5,
    "app_version": "13.1.0",
    "title": "Well thought out!",
    "content": "A beautifully narrated and well planned tour. Really excellent"
  },
  {
    "author": "G Nam 1",
    "date": "2024-10-24T12:30:39-07:00",
    "rating": 5,
    "app_version": "13.0.2",
    "title": "Folsom & Sacramento tours by Lynn Momboisse",
    "content": "5 stars. Easy to use, clear audio, informative history. Sometimes our schedule didn\u2019t allow for the full walking tour, so we listened to it as virtual playback. Will do more."
  },
  {
    "author": "IamNannaKate",
    "date": "2024-10-20T10:01:16-07:00",
    "rating": 5,
    "app_version": "13.0.2",
    "title": "Love this app!",
    "content": "We do VoiceMap tours in every city we visit. I am a huge fan!"
  },
  {
    "author": "T888K",
    "date": "2024-10-16T00:36:16-07:00",
    "rating": 5,
    "app_version": "13.0.2",
    "title": "Amazing",
    "content": "I\u2019ve done two voice tours so far ((Heidelberg & Strasbourg) and loved both! Strasbourg was particularly good!"
  },
  {
    "author": "Shadow U",
    "date": "2024-10-03T11:24:24-07:00",
    "rating": 5,
    "app_version": "13.0.2",
    "title": "Worth it",
    "content": "Price is good, the walk was great and learning more about Old San Juan this way was entertaining and educating. Will definitely recommend to others."
  },
  {
    "author": "Chipper putter 72",
    "date": "2024-10-01T13:19:05-07:00",
    "rating": 5,
    "app_version": "13.0.2",
    "title": "Coimbra Portugal",
    "content": "This is an excellent tour. Sara guides you through the city with clear and concise directions and recounts the history and highlights of the city with charm. She has the authenticity of a native but is also attuned to what a tourist will want to know. Thank you Sara. You made my visit to Coimbra a highlight of my trip to Portugal."
  },
  {
    "author": "CaroParo13",
    "date": "2024-09-29T02:55:09-07:00",
    "rating": 5,
    "app_version": "13.0.2",
    "title": "Perfect walking tour!",
    "content": "Found this app through Viator and it was perfect. My husband and I did it together and loved how clear the directions were and the narrator\u2019s just enough info. We\u2019ll use again!"
  }
]
"""

if __name__ == "__main__":
    app_analytics = json.loads(_example_analytics)
    app_info = json.loads(_example_app_info)
    app_reviews = json.loads(_example_app_reviews)
    dirname = os.path.dirname(__file__)
    sensortower_info = {"downloads": "20k", "revenue": "10k$"}
    create_html(app_analytics, app_info, app_reviews, sensortower_info, os.path.join(dirname, "../temp/test_html.html"))