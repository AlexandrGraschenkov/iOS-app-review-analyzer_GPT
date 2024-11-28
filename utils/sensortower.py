import requests, os
from bs4 import BeautifulSoup

def get_revenue_and_downloads(app_id: str):
    url = f'https://app.sensortower.com/overview/{app_id}?country=US'
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        revenue, downloads = _get_revenue_and_downloads(response.text)
        if not revenue: revenue = "-"
        if not downloads: downloads = "-"
        return  {"downloads": downloads, "revenue": revenue}
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return {"downloads":"-", "revenue": "-"}

def _get_revenue_and_downloads(html: str):
    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')
    
    # Find the relevant meta description content
    meta_description = soup.find('meta', {'name': 'description'})
    if meta_description:
        content = meta_description.get('content', '')
        
        # Look for the specific phrases in the content
        if 'downloads' in content and 'revenue' in content:
            try:
                downloads = content.split('downloads')[-2].split()[-1]
                revenue = content.split('revenue')[-2].split()[-2:]
                if revenue[0] == "<":
                    revenue = "".join(revenue)
                else:
                    revenue = revenue[1]

                if revenue == "app's": revenue = "???"
                return revenue, downloads
            except IndexError:
                pass  # If parsing fails, return None
    return None, None

if __name__ == "__main__":
    # URL of the HTML page
    url = 'https://app.sensortower.com/overview/284876795?country=US'

    # Send GET request to fetch the HTML content
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the content to a file
        dirname = os.path.dirname(__file__)
        filepath = os.path.join(dirname, "../temp/test_sensortower_4.html")
        print(_get_revenue_and_downloads(response.text))
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(response.text)
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")