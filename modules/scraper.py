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

def logo_print(message):
    logo()
    print(message)

def get_browser_driver(headless=True):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # Run in headless mode (no browser window)
    chrome_options.add_argument("--log-level=3")
    driver_path = "drivers/chromedriver.exe"  # Set the file path to your chromedriver executable
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_episodes_page_url(url):
    logo_print("Scraping episodes page URL..")
    try:
        driver = get_browser_driver()
        driver.get(url)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[3]/div/article/section[2]/header/div/h2/a'))
        )
        href = element.get_attribute('href')
        episodes_page_url = href
        logo_print("Episodes page URL scraped!")
        return episodes_page_url
    except Exception as e:
        logo_print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()

def get_episodes_api_url(url):
    logo_print("Scraping episodes API URL..")
    try:
        driver = get_browser_driver()
        driver.get(url)
        time.sleep(10)  # Wait for some time to let the page load and requests to be captured
        episodes_api_url = None
        for request in driver.requests:
            if request.response:
                if request.url.startswith('https://feed.entertainment.tv.theplatform.eu/f/PR1GhC/mediaset-prod-all-programs-v2'):
                    range_match = re.search(r'&range=(\d+-\d+)', request.url)
                    if range_match:
                        range_part = range_match.group(1)
                        episodes_api_url = request.url.replace(range_part, '0-10000')
                    break
        if episodes_api_url:
            logo_print("Episodes API URL scraped!")
        else:
            logo_print("Failed to retrieve episodes API URL.")
        return episodes_api_url
    except Exception as e:
        logo_print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()

def save_episodes_links(data, title):
    logo_print("Saving episodes links..")
    try:
        output_folder = "output/links"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        filename = os.path.join(output_folder, title + '.json')
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logo_print("Episodes links saved!")
        return filename
    except Exception as e:
        logo_print(f"An error occurred: {e}")
        return None

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
        print(video_links[0])
        return video_links[0] if video_links else None
    elif "This video is drm protected" in result.stderr:
        print("DRM-protected content: Unable to retrieve video link.")
    elif "This content is not available in your location" in result.stderr:
        print("Content not available in your location.")
    else:
        print("An error occurred while retrieving video link.")
    return None

def scrape():
    logo_print("Scraping started...")
    input_url = input("Enter the URL: ")
    episodes_page_url = get_episodes_page_url(input_url)
    if episodes_page_url:
        episodes_api_url = get_episodes_api_url(episodes_page_url)
        if episodes_api_url:
            response = requests.get(episodes_api_url)
            if response.ok:
                data = response.json()
                title = data['entries'][0]['mediasetprogram$tvLinearSeasonTitle'].replace(' ', '_')
                episodes_info = []
                for entry in data['entries']:
                    episode_info = {
                        "episode": entry['tvSeasonEpisodeNumber'],
                        "type": entry['mediasetprogram$editorialType'],
                        "link": "https:" + entry['mediasetprogram$videoPageUrl']
                    }
                    episodes_info.append(episode_info)
                tv_linear_season_info = {
                    "title": title,
                    "episodes": len(episodes_info),
                    "links": episodes_info
                }
                filename = save_episodes_links(tv_linear_season_info, title)
                if filename:
                    logo_print("Scraping video links...")
                    with open(filename, "r") as json_file:
                        data = json.load(json_file)
                    for episode in data["links"]:
                        video_link = get_video_link(episode["link"])
                        if video_link:
                            episode["video_link"] = video_link
                    with open(filename, "w") as json_file:
                        json.dump(data, json_file, indent=4)
                    print("Video links scraped and saved successfully.")
            else:
                logo_print("Failed to fetch data from the URL.")
        else:
            logo_print("Failed to retrieve episodes API URL.")
    else:
        logo_print("Failed to retrieve episodes page URL.")
