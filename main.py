import os
from modules.logo import logo
from modules.scraper import scrape
from modules.downloader import download

def check_folders():
    # Define folder paths
    links_folder = "output/links"
    videos_folder = "output/videos"

    # Check if output/links folder exists, if not create it
    if not os.path.exists(links_folder):
        os.makedirs(links_folder)

    # Check if output/videos folder exists, if not create it
    if not os.path.exists(videos_folder):
        os.makedirs(videos_folder)


def main():
    check_folders()
    logo()
    while True:
        print("[1] Scrape episodes")
        print("[2] Download episodes")
        print("[3] Exit")
        option = input("-> ")

        if option == "1":
            scrape()
        elif option == "2":
            download()
        elif option == "3":
            print("Exiting program. Goodbye!")
            break
        else:
            logo()
            print("Invalid choice! Please enter a valid option.")

if __name__ == '__main__':
    main()
