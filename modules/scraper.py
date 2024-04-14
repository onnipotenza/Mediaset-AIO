import os
import re
import time
import json
import requests
import subprocess
from modules.logo import logo
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_episodes_page_url(url):
    logo()
    print("Scraping episodes page URL..")
    try:
        # Set up Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
        chrome_options.add_argument("--log-level=3")
        driver_path = "drivers/chromedriver.exe"  # Set the file path to your chromedriver executable
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Go to the input URL
        driver.get(url)

        # Find the element containing the URL
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[3]/div/article/section[2]/header/div/h2/a'))
        )
        # Extract the href attribute value
        href = element.get_attribute('href')

        # Close the browser
        driver.quit()

        # No need to concatenate with the base URL
        episodes_page_url = href
        logo()
        print("Episodes page URL scraped!")
        return episodes_page_url

    except Exception as e:
        logo()
        print("An error occurred:", e)
        return None

def get_episodes_api_url(url):
    logo()
    print("Scraping episodes API URL..")
    try:
        # Create the Chrome driver with headless option
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        # Go to the specified URL
        driver.get(url)

        time.sleep(10)  # Wait for some time to let the page load and requests to be captured

        episodes_api_url = None

        # Access requests list via the `requests` attribute
        for request in driver.requests:
            if request.response:
                if request.url.startswith('https://feed.entertainment.tv.theplatform.eu/f/PR1GhC/mediaset-prod-all-programs-v2'):
                    # Extract the range part from the original URL
                    range_match = re.search(r'&range=(\d+-\d+)', request.url)
                    if range_match:
                        range_part = range_match.group(1)
                        # Replace the range part with '0-10000'
                        episodes_api_url = request.url.replace(range_part, '0-10000')
                    break

        driver.quit()

        if episodes_api_url:
            logo()
            print("Episodes API URL scraped!")
        else:
            logo()
            print("Failed to retrieve episodes API URL.")
        return episodes_api_url

    except Exception as e:
        logo()
        print("An error occurred:", e)
        return None

def save_tv_linear_season_info(url):
    logo()
    print("Saving episodes links..")
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            # Extract tvLinearSeasonTitle from the first object
            tv_linear_season_title = data['entries'][0]['mediasetprogram$tvLinearSeasonTitle']
            title = tv_linear_season_title.replace(' ', '_')

            episodes_info = []

            # Extract information for each episode
            for entry in data['entries']:
                episode_info = {
                    "episode": entry['tvSeasonEpisodeNumber'],
                    "type": entry['mediasetprogram$editorialType'],
                    "link": "https:" + entry['mediasetprogram$videoPageUrl']
                }
                episodes_info.append(episode_info)

            # Create the JSON structure
            tv_linear_season_info = {
                "title": title,
                "episodes": len(episodes_info),
                "links": episodes_info
            }

            # Save the information to a JSON file
            output_folder = "output/links"
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filename = os.path.join(output_folder, title + '.json')
            with open(filename, 'w') as json_file:
                json.dump(tv_linear_season_info, json_file, indent=4)
            logo()
            print("Episodes links saved!")
            return filename
        else:
            logo()
            print("Failed to fetch data from the URL.")
            
    except Exception as e:
            logo()
            print("An error occurred:", e)

def get_video_link(link):
    command = [
        'drivers/yt-dlp.exe',
        '--get-url',
        '--no-playlist',
        link
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        video_links = result.stdout.strip().split('\n')
        # Take only the first link
        return video_links[0]
    elif "This video is drm protected" in result.stderr:
        print("DRM-protected content: Unable to retrieve video link.")
        return None
    elif "This content is not available in your location" in result.stderr:
        print("Content not available in your location.")
        return None
    else:
        return None

def scrape():
    logo()
    input_url = input("Enter the URL: ")
    episodes_page_url = get_episodes_page_url(input_url)
    if episodes_page_url:
        episodes_api_url = get_episodes_api_url(episodes_page_url)
        if episodes_api_url:
            filename = save_tv_linear_season_info(episodes_api_url)
            if filename:
                logo()
                print("Scraping video links...")

                with open(filename, "r") as json_file:
                    data = json.load(json_file)
                for episode in data["links"]:
                    video_link = get_video_link(episode["link"])
                    if video_link:
                        episode["video_link"] = video_link

                with open(filename, "w") as json_file:
                    json.dump(data, json_file, indent=4)
                logo()
                print("Video links scraped and saved successfully. Press enter to continue!")
                input()
    
        else:
            logo()
            print("Failed to retrieve episodes API URL.")
    else:
        logo()
        print("Failed to retrieve episodes page URL.")