""" 
Subreddit can be changed, but not all work
Working ones that I tested:
    r/Wallpaper
    r/Wallpapers
    r/MinimalWallpaper
    r/WQHD_Wallpaper
    r/EarthPorn
    r/CityPorn
    r/CarPorn
    r/ExposurePorn
"""
subreddit = 'r/Wallpaper'


import os
import ctypes
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def lovely_soup(x):
    ua = UserAgent()
    r = requests.get(x, headers={'User-Agent': ua.chrome})
    return BeautifulSoup(r.text, 'html.parser')


def main():
    global subreddit
    BASE_URL = 'https://old.reddit.com/'
    URL = f'{BASE_URL}{subreddit}/top'

    # Finding top upvoted post
    print('Looking for today\'s top upvoted post')
    soup = lovely_soup(URL)
    try:
        top_post = soup.find_all('a', class_='thumbnail')[0]['href']
    except IndexError:
        print('Something went wrong')
        print('Make sure you chose a subreddit that\'s for images only and is not 18+ restricted')
        return

    # Finding the image link from that post
    print('Extracting url')
    soup = lovely_soup(BASE_URL+top_post)
    try:
        img_parent = soup.find_all('div', class_='media-preview-content')[0]
        img = img_parent.find('a')['href']
        img_name = img[18:]
    except TypeError:
        print('Something went wrong')
        print('Make sure you chose a subreddit that\'s for images only and is not 18+ restricted')
        return

    # Writing the image to disk
    print('Downloading image')
    with open(f'wallpapers/{img_name}', 'wb') as f:
        f.write(requests.get(img).content)

    # Set the image as wallpaper
    print('Setting the image as wallpaper')
    cwd = os.getcwd()
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{cwd}/wallpapers/{img_name}" , 0)
    print('Done! \nCheck your desktop')


if __name__ == "__main__":
    main()
