#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Rename videos and subtitle, also write content.md '''

import os, re, shutil, sys
import save
from colorama import *

def assign_folder(folder):
    ''' return folder path '''
    os.chdir(folder)
    path = os.getcwd()
    return path   

def vid_srt_to_chapter(url, course_folder):
    ''' move videos and subtitles to correct chapter folder '''

    soup = save.create_soup(url)

    chapters = soup.find_all("h4", class_="ga")
    ul_video = soup.find_all('ul', class_="row toc-items")

    chapter_count = 0
    video_count = 0

    total_videos = save.total_videos(url) 
    print('\nVideos downloaded: ' + str(total_videos) +'\n')
        
    for li in ul_video:
        chapter_name = chapters[chapter_count].text
        
        if chapter_name[1] == '.':
            chapter_name = str(chapter_count).zfill(2) + '. ' + chapter_name[3:]
        elif chapter_name[2] == '.':
            chapter_name = str(chapter_count).zfill(2) + '. ' + chapter_name[4:]
        else:
            chapter_name = str(chapter_count).zfill(2) + '. ' + chapter_name
        chapter_name = re.sub('[,:?><"/\\|*]', ' ', chapter_name)
        chapter_name = chapter_name.strip()
        
        chapter_count += 1

        os.chdir(course_folder)

        group = li.find_all('a', class_='video-name')
        
        # decide the correct zfill value to result in proper file moving
        digit = 1
        if total_videos > 9:
            digit = 2
        if total_videos > 99:
            digit = 3

        print('🔰  Moving files inside: ' + str(chapter_name))
        for video in group:
            video_count += 1
            
            video_name = str(video_count).zfill(digit) + ' - ' + video.text.strip()
            video_name = video_name.split("\n").pop(0) + '.mp4'
            video_name = re.sub('[?]', '', video_name)
            video_name = re.sub('[/]', '_', video_name)
            video_name = re.sub('["]', '\'', video_name)
            video_name = re.sub('[:><\\|*]', ' -', video_name)
            
            subtitle_name = str(video_count).zfill(digit) + ' - ' + video.text.strip()
            subtitle_name = subtitle_name.split("\n").pop(0) + '.en.srt'
            subtitle_name = re.sub('[?]', '', subtitle_name)
            subtitle_name = re.sub('[/]', '_', subtitle_name)
            subtitle_name = re.sub('["]', '\'', subtitle_name)
            subtitle_name = re.sub('[:><\\|*]', ' -', subtitle_name)

            try:
                shutil.move(video_name, chapter_name)
            except:
                try:
                    print('🤕  File not found: ' + str(video_name))
                except UnicodeEncodeError:
                    print('🤕  File not found: ' + (video_name).encode('utf-8'))

            try:
                shutil.move(subtitle_name, chapter_name)
            except:
                pass

    print('\n🥂  videos/subtitles moved to appropriate chapters successfully.')

def hms_string(sec_elapsed):
    ''' format elapsed time '''
    hour = int(sec_elapsed / (60 * 60))
    minutes = int((sec_elapsed % (60 * 60)) / 60)
    seconds = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(hour, minutes, seconds)
