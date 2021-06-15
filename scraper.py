from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

""" 
    This is how many seconds the program waits after scrolling down, before 
        checking for the bottom of the page and attempting to scroll again.
    Slower internet connections may need a higher SLEEP_TIME 
        value to actually load all the videos.
    Default: 1
"""
SLEEP_TIME = 1

"""
    This is the path/filename where the download queue file will be stored
    TODO: Pick a format for the download queue and make it better? for faster 
          reading, something that's good to store a list in. maybe json? idk
"""
QUEUE_FILENAME = "download_queue"

def fix_yt_video_url(url):
    """If `url` is a valid youtube video url, return `url`.
    Otherwise, assume `url` is the 'v' value and convert it to a valid url.

    TODO: this would break if a url without https or somethin is given
    """
    return (url if url.startswith("https://www.youtube.com/watch?v=") else f"https://www.youtube.com/watch?v={url}")

def append_to_download_queue(urls, filename=QUEUE_FILENAME):
    """ Appends a URL or multiple URLs to the download queue.
    `urls` can be a string containing one URL, 
    or a list of strings containing multiple URLs

    TODO: This is kinda messy i think gonna redo this later probably
    """
    if isinstance(urls, list):
        with open(filename, "a") as download_queue:
            for url in video_elements:
                download_queue.write(f"{fix_yt_video_url(url)}\n")
    
    elif isinstance(urls, str):
        with open(filename, "a") as download_queue:
            download_queue.write(f"{fix_yt_video_url(urls)}\n")

def get_video_list_from_channel_name(channel_name):
    """ 
    """
    # Selenium Setup
    # TODO: maybe change Firefox to PhantomJS, so this runs quietly.
    driver = webdriver.Firefox()
    driver.get(f"https://www.youtube.com/c/{channel_name}/videos")
    print("\nPage loaded!")

    # Check for error (Invalid channel_name)
    if driver.title == "404 Not Found":
        driver.close()
        print("No videos found.")
        return

    # Scroll to bottom of page, until all videos have been loaded
    page_height = -1
    while True:
        prev_page_height = page_height
        page_height = driver.execute_script("return window.pageYOffset + window.innerHeight")

        if prev_page_height < page_height:
            driver.execute_script(f'window.scrollTo(0,({page_height}))')
            sleep(SLEEP_TIME)
        else:
            break
    print("\nMade it to the bottom! :)")

    # Get list of video URLs, add to download_queue file
    video_elements = driver.find_elements(By.ID, "video-title")

    URL_list = []
    for elem in video_elements:
        URL_list.append(elem.get_attribute('href'))
    append_to_download_queue(URL_list)
    
    print(f"\nAdded {len(URL_list)} video URL{'s' if len(URL_list) > 1 else ''} to the download queue.")
    print("\nBye!")
    driver.close()
    return URL_list


# TODO: Write unit tests!!!!!!!!!!!
if __name__ == '__main__':
    # Not a real channel name
    # get_video_list_from_channel_name("djskfhnliause6r4387euryhb")

    # Channel with no videos
    # get_video_list_from_channel_name("UC1ZCDXSgByj_1eg_ubKdCqw")

    # Channel with one video
    # get_video_list_from_channel_name("UC-aGNJj_R35QouVZ_-V8tJw")

    # Channel with many videos (Scroll required)
    get_video_list_from_channel_name("FredrikKnudsen")