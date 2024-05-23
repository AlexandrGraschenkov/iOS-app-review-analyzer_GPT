import json
import webbrowser, os


# HTML content
def _create_html(app_data):
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
                margin: 20px auto;
                display: block;
                border: 1px solid #e0e5eb;
                border-radius: 25%;
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
        </style>
    </head>
    <body>
        <header>
            <h1>{app_data["app_analysis"]["name"]}</h1>
        </header>
        <div class="container">
            <img class="app-icon" src="{app_data["icon"]}" alt="App Icon">
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
        </div>
        <footer>
            <p>&copy; 2024 iOS App Analytics, made by <a href="https://x.com/sharrikk" style="color: white;">Alex Gra 𝕏</a></p>
        </footer>
    </body>
    </html>
    '''
    return html_content

def create_html(app_analysis, app_info, save_to_path, open_html_page=True):
    # Write the HTML content to a file
    app_data = {
        "app_analysis": app_analysis,
        "icon": app_info["icon"],
        "screenshots": app_info["screenshots"]
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
{"screenshots":[
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

if __name__ == "__main__":
    app_analytics = json.loads(_example_analytics)
    app_info = json.loads(_example_app_info)
    dirname = os.path.dirname(__file__)
    create_html(app_analytics, app_info, os.path.join(dirname, "../temp/test_html.html"))