import json
from openai import OpenAI
import tiktoken
from tqdm.auto import tqdm

# only this models supprot json response
gpt_models = {
	"gpt-4-1106-preview": 128000,
	"gpt-3.5-turbo-1106": 16385,
    "gpt-4o-2024-05-13": 128000
}

class GPTWrapper:
    def __init__(self, api_key, model, temperature = 0.2, max_input_token_count = None):
        if model not in gpt_models:
            print(f"Can't find {model} in list available models")
            return None
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.enc = tiktoken.encoding_for_model("gpt-4")
        self.max_input_token_count = max_input_token_count if max_input_token_count else gpt_models[model]
        self.total_in_tokens = 0
        self.total_out_tokens = 0

    
    def process_reviews(self, app_info: dict, reviews: list):
        prompt = self.__generate_promp()
        data = {"app": app_info, "reviews": reviews}
        result = self.__process_json_internal(prompt, data)
        return result
    
    def get_debug_analysis(self):
        return {
            "app_analysis": {
                "name": "Liquid Player",
                "pros": [
                "Developer responsiveness to user feedback",
                "Quality and convenience of the app",
                "No advertisements",
                "Continuous improvement based on user reviews",
                "Ability to watch videos through the app",
                "Easy to use interface",
                "Local server support",
                "Full screen support"
                ],
                "cons": [
                "Bugs reported with Google Translate modal",
                "Crashes on iPhone 5s after update",
                "Discoverability of the app could be improved",
                "Chromecast compatibility issues on iPhone XR",
                "Does not remember video progress",
                "Limited functionality and translator options",
                "Does not support offline dictionary overlays"
                ],
                "suggest_what_improve": "Fix the Google Translate modal bug, improve app stability on older iPhone models, enhance discoverability, add Chromecast support for iPhone XR, remember last used subtitles and video progress, expand functionality and translator options, and consider offline dictionary integration.",
                "why_app_popular": "The app seems to be popular due to its user-friendly interface, absence of ads, and the developer's active engagement with the community to continuously improve the app based on user feedback."
            }
            }

    def __generate_promp(self, summarize=False):
        prompt = ""
        if summarize:
            prompt = "Summarize pros and cons."
        else:
            prompt = "Help find pros and cons with given description, title, update info. During response give more attention to user review. App description for better context. Fields 'usefull' and 'useless' has number of people votes for this review (not exist if value equal 0)."
        out_format = """{"app_analysis": {"name": "app_name","pros": ["pros_1","pros_2", "..."],"cons": ["cons_1", "cons_2", "..."],"suggest_what_improve": "#1 fix, improve option","why_app_popular": "give you thought why this app popular"}}"""

        prompt = f"You are assistant for product manager of mobile apps. Please help analyze user reviews of the app. {prompt} Input will be in JSON format from user. Please give output of result in JSON format. Use english language for output. Template output format:\n{out_format}"
        return prompt

    def __process_json_internal(self, prompt, json_input):
        message = json.dumps(json_input, ensure_ascii=False, separators=(',', ':'))
        response = self.client.chat.completions.create(
            model = self.model,
            temperature = self.temperature,
            response_format = { "type": "json_object" },
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ]
        )
        output_text = response.choices[0].message.content
        # print("Output Tokens:", len(enc.encode(output_text)))
        self.total_out_tokens += len(self.enc.encode(output_text))
        return json.loads(output_text)