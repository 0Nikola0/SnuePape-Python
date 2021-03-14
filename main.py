""" 
Example subreddits:
    r/Wallpaper
    r/Wallpapers
    r/WQHD_Wallpaper
    r/EarthPorn
    r/CityPorn
    r/CarPorn
    r/ExposurePorn
"""
Subreddit = 'r/Wallpapers'

"""
Timespan can be:
    day
    week
    month
    year
    all
"""
Timespan = 'all'


import os
import ctypes
import requests
from fake_useragent import UserAgent


def get_posts(subreddit, timespan):
    '''
    Send request to reddit and parses the json to extract the top posts
    '''
    ua = UserAgent()
    URL = f'https://reddit.com/{subreddit}/top.json?t={timespan}'

    response = requests.get(URL, headers={'User-Agent': ua.chrome})
    response_data = response.json()['data']['children']
    
    print('[>]Looking for today\'s top upvoted post')
    # It checks each post if it's an image and if it's not 18+. If so it adds it to the posts list
    posts = [post['data'] for post in response_data if not post['data']['over_18'] and (post['data']['url'].endswith('.png') or post['data']['url'].endswith('.jpg'))]
    return posts


def download_image(post):
    '''
    Checks if the wallpapers folder exists, if not creates it
    Downloads the image in it'r original file extension
    '''
    # Check if folder exists, if not create it
    cwd = os.getcwd()   # Current Working Directory
    if not os.path.exists(f"{cwd}/Wallpapers"):
        print('[>]Creating wallpapers folder')
        os.mkdir(f"{cwd}/Wallpapers")
    
    print('[>]Downloading image')
    img_file_extension = post['url'].strip()[-4:]
    img_name = post['title'].strip() + img_file_extension
    img_link = post['url']
    with open(f'wallpapers/{img_name}', 'wb') as f:
        f.write(requests.get(img_link).content)
    print('[>]Image successfully downloaded')
    return img_name


def set_wallpaper(img_name):
    '''
    Sets the downloaded image as desktop's wallpaper
    '''
    print('[>]Setting the image as wallpaper')
    cwd = os.getcwd()   # Current Working Directory
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{cwd}\\Wallpapers\\{img_name}" , 0)
    print('[>]Done! \n[>]Check your desktop')


def main():
    try:
        top_post = get_posts(Subreddit, Timespan)[0]
    except IndexError:
        print('[!]Couldn\'t find any image posts \n[!]Please select another subreddit')
        return None
    
    img_name = download_image(top_post)
    set_wallpaper(img_name)


if __name__ == "__main__":
    main()
