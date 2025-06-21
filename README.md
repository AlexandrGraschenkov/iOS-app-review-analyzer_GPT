## App Review Analyzer <img width=24px height=24px src="https://upload.wikimedia.org/wikipedia/commons/6/67/App_Store_%28iOS%29.svg"> / <img width=24px height=24px src="https://upload.wikimedia.org/wikipedia/commons/d/d0/Google_Play_Arrow_logo.svg">


A powerful tool to analyze user reviews from both iOS App Store and Google Play Store using GPT.

<img src="images/analytics_preview.jpg">

### Features:
- **Multi-platform support**: iOS App Store and Google Play Store
- **AI-powered analysis**: Uses OpenAI GPT models to analyze reviews
- **Comprehensive insights**: Identifies pros, cons, improvement suggestions, and popularity factors
- **Beautiful HTML reports**: Generates detailed HTML reports with review data
- **Multi-store support**: Collects reviews from multiple countries/stores

### Usage:
```sh
python3 review_analyzer.py \
  --gpt_api_key=sk-DfS... \
  --app_ids=1454762989,io.instories
```
`app_ids` separate with comma, autodetect `AppStore`/`GooglePlay`

### Parameters:
- `--gpt_api_key`: Your OpenAI API key (required)
- `--gpt_model`: GPT model to use (default: gpt-4o-mini-2024-07-18)
- `--app_ids`: Comma-separated list of app IDs (required)
- `--platform`: Platform to analyze - 'ios' or 'android' (default: ios)
- `--stores`: Comma-separated list of countries/stores (default: us,ca,au,ru,it,in,fr,gb,ua,jp,cn,tw,my,de,kr,br,mx,es,sa,ae,vn,tr)
- `--save_folder`: Directory to save HTML reports (default: ./temp)

### App ID Formats:
- **iOS**: Numeric ID (e.g., 1454762989)
- **Android**: Package name (e.g., io.instories)

### Instalation:
```bash
pip install -r requirements.txt
```
Dependencies:
```
openai
tiktoken
tqdm
requests
google-play-scraper
```
