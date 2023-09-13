#my RSS podcast downloader
#Eric Larsen 2023
#gets the latest podcast episodes without apps or subscriptions

import os
import datetime
#regex to remove HTML markups from descriptions
import re
import feedparser as RSS
#primary download method:
import urllib.request as DOWNLOAD
#alt download method:
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

PODCASTS = [('Mega64','https://mega64.com/feed/podcast/mega64podcast'),
            ('We Hate Movies','https://www.omnycontent.com/d/playlist/77bedd50-a734-42aa-9c08-ad86013ca0f9/9013bb9b-3638-4ddc-b8ac-ad8d016220ef/48cb4b4f-9aed-4bea-8c52-ad8d0162210b/podcast.rss'),
            ('TWiEVO','http://twievo.libsyn.com/rss'),
            ('TWiM','http://feeds.feedburner.com/twim'),
            ('TWiV','http://twiv.microbeworld.libsynpro.com/twiv'),
            ('TWiN','https://twin1.libsyn.com/rss'),
            ('Planetary Radio','https://www.omnycontent.com/d/playlist/d95da206-8ee8-4ba5-ba8d-ad1200b4e5a4/cf13d5f5-6040-458d-ab5a-ad200189747d/b75c9f7f-4a63-438e-b506-ad2001897499/podcast.rss'),]

#regex for HTML markup
PARAGRAPH_MARK_REGEX = r'<p>(.*?)<\/p>'
GENERAL_MARKUP_REGEX = r'<[^>]+>|&[^>]+;'

for SHOW in PODCASTS:
    SHOW_NAME = SHOW[0]
    #make folder for the show if it doesn't already exist
    if not os.path.isdir(f'Downloads\\{SHOW_NAME}'):
        os.makedirs(f'Downloads\\{SHOW_NAME}')
    
    RSS_URL = SHOW[1]
    FEED_READ = RSS.parse(RSS_URL)
    #get latest episode
    LATEST = FEED_READ.entries[0]

    #get latest episode meta data
    EPISODE_TITLE = LATEST.title
    print(f'{SHOW_NAME} - {EPISODE_TITLE}')
    #REMOVE UNWANTED CHARACTERS FROM TITLE for valid, simple filename
    SEMI_COLON_DETECT = EPISODE_TITLE.find(':')
    DASH_DETECT = EPISODE_TITLE.find('-')
    if DASH_DETECT != -1 and SEMI_COLON_DETECT==-1:
        FILE_TITLE = EPISODE_TITLE[0:DASH_DETECT]
    if SEMI_COLON_DETECT != -1 and DASH_DETECT==-1:
        FILE_TITLE = EPISODE_TITLE[0:SEMI_COLON_DETECT]
    if DASH_DETECT != -1 and SEMI_COLON_DETECT != -1:
        CLIP_TITLE = min(DASH_DETECT,SEMI_COLON_DETECT)
        FILE_TITLE = EPISODE_TITLE[0:CLIP_TITLE]
    
    EPISODE_DATE = LATEST.published
    #convert to datetime obj
    PUBLISH_DATE = datetime.datetime.strptime(EPISODE_DATE[0:16],'%a, %d %b %Y')
    print(f'{PUBLISH_DATE}\n================')

    EPISODE_SUMMARY = LATEST.summary
    #remove HTML markups, ads, and other junk with regex
    #rebuild paragraphs
    para_text = re.split(PARAGRAPH_MARK_REGEX, EPISODE_SUMMARY)
    #remove remaining HTML markups
    clean_text = ''
    for paragraph in para_text:
        clean_paragraph = re.sub(GENERAL_MARKUP_REGEX,'',paragraph)+'\n'
        if len(clean_paragraph)>1:
            clean_text+=clean_paragraph
    print(f'{clean_text}\n***************')
    #working 9/11/23

    #download latest episode mp3
    LATEST_URL = LATEST.links
    #scan for mp3 address
    MP3_found = 0
    Fresh_download = 0
    for LINK in LATEST.links:
        URL = LINK['href']
        if URL.find('.mp3')!=-1:
            MP3_link = URL
            file_address = f'Downloads\\{SHOW_NAME}\\{FILE_TITLE}.mp3'
            if not os.path.exists(file_address):
                print('Downloading mp3....')
                try:
                    DOWNLOAD.urlretrieve(MP3_link, file_address)
                except:
                    with open(file_address, 'wb') as f_out:
                        r = requests.get(MP3_link, headers=headers, stream=True)
                        print(r)
                        for chunk in r.iter_content(chunk_size=512):
                            if chunk:
                                f_out.write(chunk)
                print('DOWNLOAD COMPLETE!\n')
                MP3_found = 1
                Fresh_download = 1
            else:
                print('Latest Episode Already Downloaded')
                MP3_found = 1

    if MP3_found==1 & Fresh_download==1:
        print('Coming soon - mp3 tagging\n')
        #TO DO - tagging MP3 with data if needed
    if SHOW is not PODCASTS[-1]:
        print('------------------------\n')
        print('Load next show...\n')
    else:
        print('\n****\nLatest episodes all downloaded. Enjoy!')
#end of show loop for getting latest episodes

