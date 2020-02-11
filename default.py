# Einthusan.com plugin written by humla.

import os
import re
import urllib, urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
from datetime import date

import HTTPInterface
import JSONInterface
import DBInterface
#import urlresolver
import requests

# s = requests.Session()

NUMBER_OF_PAGES = 3

ADDON = xbmcaddon.Addon(id='plugin.video.isaidub')
#username = ADDON.getSetting('username')
#password = ADDON.getSetting('password')

#locationStr = xbmcplugin.getSetting(int(sys.argv[1]), 'location')
#Locations = ['San Francisco', 'Dallas', 'Washington D.C', 'Toronto', 'London', 'Sydney', 'No Preference']

#locationId = int(locationStr)
#if (locationId > len(Locations) - 1):
#    locationId = len(Locations) - 1

#location = Locations[locationId]
BASE_URL='https://myisaidub.co/'
##
# Prints the main categories. Called when id is 0.
##
def main_categories(name, url, language, mode):
    cwd = ADDON.getAddonInfo('path')
    #img_path = cwd + '/images/' 
    img_path = cwd + '/images/' 
    #addDir('Tamil A-Z Dubbed Movies', '', 7, '', '')
    #addDir('Tamil 2019 Dubbed Movies', '', 7, '', '')
    #addDir('Tamil 2018 Dubbed Movies', '', 7, '', '')
    #addDir('Tamil 2017 Dubbed Movies', '', 7, '', '')
    #addDir('Tamil 2016 Dubbed Movies', '', 7, '', '')
    #addDir('Tamil Dubbed Collections', '', 7, '', '')
    addDir('Tamil Yearly Dubbed Movies', '', 9,'', '')
    addDir('Tamil Dubbed Collections', BASE_URL+'/tamil/tamil-dubbed-movies-collections.html', 1, '')
    addDir('Tamil Genres Dubbed Movies', '', 10, '', '')
    #addDir('Tamil HD Dubbed Movies', '', 7, '', '')
    #addDir('Hollywood Movies in (English)', BASE_URL+'/tamil/hollywood-movies-in-english.html', 1, '')
    addDir('Addon Settings', '', 12, img_path + 'settings.png', '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows categories for each language
##
def inner_categories(name, url, language, mode, bluray=False): 
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 

    postData = 'lang=' + language
    if bluray:
        postData = 'lang=' + language + '&bluray=1&'

    #addDir('A-Z', postData, 8, img_path + 'a_z.png', language)
    #addDir('Category By Years', postData, 9, img_path + 'years.png', language)
    addDir('Tamil Dubbed Movies Collections', BASE_URL+'/tamil/tamil-dubbed-movies-collections.html', 1, '')
    #addDir('[COLOR red]Actors[/COLOR]', postData, 10, img_path + 'actors.png', language)
    #addDir('[COLOR red]Director[/COLOR]', postData, 11, img_path + 'director.png', language)
    #addDir('Recent', postData, 3, img_path + 'recent.png', language)
    #addDir('[COLOR red]Top Rated[/COLOR]', postData, 5, img_path + 'top_rated.png', language)
    #if not bluray:
        #addDir('Featured', '', 4, img_path + 'featured_videos.png', language)
        #addDir('[COLOR red]Blu-Ray[/COLOR]', '', 13, img_path + 'Bluray.png', language)
        #addDir('Search', postData, 6, img_path + 'Search_by_title.png', language)
        #addDir('[COLOR red]Music Video[/COLOR]', '' , 14, img_path + 'music_videos.png', language)
        #addDir('Mp3 Music', '', 16, '', language)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
#  Displays the categories for Blu-Ray
#
def display_BluRay_listings(name, url, language, mode):
    inner_categories(name, url, language, mode, True)

##
#  Scrapes a list of movies and music videos from the website. Called when mode is 1.
##
def get_movies_and_music_videos(name, url, language, mode):
    get_movies_and_music_videos_helper(name, url, language, mode, 1)


def get_movies_and_music_videos_helper(name, url, language, mode, page):
    xbmc.log('get movie url is '+url, level=xbmc.LOGNOTICE)
    #referurl = url
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/'
    srcRegex = ' /> <a href="(.+?)">'
    titleRegex = ' title="(.+?)">'
    imgRegex = '<img src="(.+?).gif" alt='
    pagenumRegex = '<a href="(.+?)" title="(.+?)">(.+?)</a> '
    currentpageRegex= '<span class="pagination_current">(.+?)</span> '
    if 'collections' in url:
        nextpageRegex='<a href="(.+?)" class="pagination_next"></a>'
    else:
        nextpageRegex='> <a href="(.+?)" class="pagination_next"></a>'
    prevpageRegex='<a href="(.+?)" class="pagination_prev"></a>'
    html =  requests.get(url).text
    #html =  requests.get('http://isaidubs.net/tamil-2018-dubbed-movies.html').text
    # match = re.compile('<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p').findall(html)
    #match = re.compile('<div class="f">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p.+?<span>Wiki</span>(.+?)</div>').findall(html)
    #match = re.compile(' /> <a href="(.+?)">.<img src="(.+?)" alt=. title="(.+?)">').findall(html)
    moviename=re.compile(titleRegex).findall(html)
    movielink=re.compile( srcRegex ).findall( html )
    imagepath=re.compile( imgRegex ).findall( html )
    pagenum = re.compile( pagenumRegex ).findall( html )
    currentpage = re.compile( currentpageRegex ).findall( html )
    nextpage = re.compile( nextpageRegex ).findall( html )
    prevpage = re.compile( prevpageRegex ).findall( html )
    #xbmc.log('The match is\n '+ str(match), level=xbmc.LOGNOTICE)
    #nextpage=re.findall('data-disabled="([^"]*)" href="(.+?)"', html)[-1]
    src = zip( movielink, moviename)
    match = zip(src,imagepath)


    # Bit of a hack
    #MOVIES_URL = "http://www.einthusan.tv/movies/watch/"
    for (movie, name), image in match:
        xbmc.log('\n movie is '+movie+'-- image is '+BASE_URL+image+'-- name is '+name, level=xbmc.LOGNOTICE)
        #if (mode == 1):
            #image = 'http:' + image
            #movie = str(name)+','+str(movie)+','+lang+','
            #if 'ultrahd' in ishd:
            #    name = name + '[COLOR blue]- Ultra HD[/COLOR]'
            #    movie = movie+'itshd,'+referurl
            #else:
            #    movie = movie+'itsnothd,'+referurl
            #if 'youtube' in trailer: trail = trailer.split('watch?v=')[1].split('">')[0]
            #else: trail=None
        # addDir(name, MOVIES_URL + str(movie)+'/?lang='+lang, 2, image, lang)
        addDir(name,movie,10, (BASE_URL+image) ,'','', isplayable=False)
    
    if len(nextpage)!=0:
        nextPage_Url = BASE_URL+nextpage[0]
        #if (page > NUMBER_OF_PAGES):
        addDir('>>> Next Page >>>', nextPage_Url,1,(img_path+'next.png'),'','', isplayable=False)
    #else:
        #get_movies_and_music_videos_helper(name, nextPage_Url, language, mode, 1)


    """
    if nextpage[0]!='true':
        nextPage_Url = BASE_URL+nextpage[1]
        if (page > NUMBER_OF_PAGES):
            addDir('>>> Next Page >>>', nextPage_Url,1,'','')
        else:
            get_movies_and_music_videos_helper(name, nextPage_Url, language, mode, page+1)
    """
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    # s.close()


def movie_list1(name, url, language, mode):
    xbmc.log('movie list1 url is '+url, level=xbmc.LOGNOTICE)
    #referurl = url
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/'
    srcRegex = ' /> <a href="(.+?)">'
    titleRegex = ' title="(.+?)"> <img'
    imgRegex = '<img src="(.+?).gif" alt='
    pagenumRegex = '<a href="(.+?)" title="(.+?)">(.+?)</a> '
    currentpageRegex= '<span class="pagination_current">(.+?)</span> '
    nextpageRegex='<a href="(.+?)" class="pagination_next"></a>'
    prevpageRegex='<a href="(.+?)" class="pagination_prev"></a>'
    html =  requests.get(url).text
    #html =  requests.get('http://isaidubs.net/tamil-2018-dubbed-movies.html').text
    # match = re.compile('<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p').findall(html)
    #match = re.compile('<div class="f">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p.+?<span>Wiki</span>(.+?)</div>').findall(html)
    #match = re.compile(' /> <a href="(.+?)">.<img src="(.+?).gif" alt=. title="(.+?)"> <img').findall(html)
    #nextpage=re.findall('data-disabled="([^"]*)" href="(.+?)"', html)[-1]
    moviename=re.compile(titleRegex).findall(html)
    movielink=re.compile( srcRegex ).findall( html )
    imagepath=re.compile( imgRegex ).findall( html )
    pagenum = re.compile( pagenumRegex ).findall( html )
    currentpage = re.compile( currentpageRegex ).findall( html )
    nextpage = re.compile( nextpageRegex ).findall( html )
    prevpage = re.compile( prevpageRegex ).findall( html )
    src = zip( movielink, moviename)
    match = zip(src,imagepath)

    # Bit of a hack
    #MOVIES_URL = "http://www.einthusan.tv/movies/watch/"
    for ( movie, name ), image in match:
        xbmc.log('\n movie is '+movie+'-- image is '+image+'-- name is '+name, level=xbmc.LOGNOTICE)
        #if (1):
            #image = BASE_URL + image
            #movie = str(name)+','+str(movie)+','+lang+','
            #if 'ultrahd' in ishd:
            #    name = name + '[COLOR blue]- Ultra HD[/COLOR]'
            #    movie = movie+'itshd,'+referurl
            #else:
            #    movie = movie+'itsnothd,'+referurl
            #if 'youtube' in trailer: trail = trailer.split('watch?v=')[1].split('">')[0]
            #else: trail=None
        # addDir(name, MOVIES_URL + str(movie)+'/?lang='+lang, 2, image, lang)
        addDir(name,movie,11,  image,'','', isplayable=False)

    
    if len(nextpage)!=0:
        nextPage_Url = BASE_URL+nextpage[0]
        #if (page > NUMBER_OF_PAGES):
        addDir('>>> Next Page >>>', nextPage_Url,1,(img_path+'next.png'),'','', isplayable=False)
    #else:
        #get_movies_and_music_videos_helper(name, nextPage_Url, language, mode, 1)
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def movie_list2(name, url, language, mode):
    xbmc.log('movie list2 url is '+url, level=xbmc.LOGNOTICE)
    #referurl = url
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/'
    srcRegex = '/><a href="(.+?)">'
    titleRegex = ' alt="(.+?)" width'
    imgRegex = '<td class="tblimg"><img src="(.+?)" alt'
    html =  requests.get(url).text
    #html =  requests.get('http://isaidubs.net/tamil-2018-dubbed-movies.html').text
    # match = re.compile('<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p').findall(html)
    #match = re.compile('<div class="f">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p.+?<span>Wiki</span>(.+?)</div>').findall(html)
    #match = re.compile(' /> <a href="(.+?)">.<img src="(.+?).gif" alt=. title="(.+?)"> <img').findall(html)
    #nextpage=re.findall('data-disabled="([^"]*)" href="(.+?)"', html)[-1]
    moviename=re.compile(titleRegex).findall(html)
    movielink=re.compile( srcRegex ).findall( html )
    imagepath=re.compile( imgRegex ).findall( html )
    src = zip( movielink, moviename)
    match = zip(src,imagepath)

    # Bit of a hack
    #MOVIES_URL = "http://www.einthusan.tv/movies/watch/"
    if len(match)!=0:
        for ( movie, name ), image in match:
            xbmc.log('\n movie is '+movie+'-- image is '+image+'-- name is '+name, level=xbmc.LOGNOTICE)
            #if (1):
                #image = BASE_URL + image
                #movie = str(name)+','+str(movie)+','+lang+','
                #if 'ultrahd' in ishd:
                #    name = name + '[COLOR blue]- Ultra HD[/COLOR]'
                #    movie = movie+'itshd,'+referurl
                #else:
                #    movie = movie+'itsnothd,'+referurl
                #if 'youtube' in trailer: trail = trailer.split('watch?v=')[1].split('">')[0]
                #else: trail=None
            # addDir(name, MOVIES_URL + str(movie)+'/?lang='+lang, 2, image, lang)
            addDir(name,movie,12, image,'','', isplayable=False)
    else:
        addDir(name,url,10, '','','', isplayable=False)
    """
    if nextpage[0]!='true':
        nextPage_Url = BASE_URL+nextpage[1]
        if (page > NUMBER_OF_PAGES):
            addDir('>>> Next Page >>>', nextPage_Url,1,'','')
        else:
            get_movies_and_music_videos_helper(name, nextPage_Url, language, mode, page+1)
    """
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def movie_list3(name, url, language, mode):
    xbmc.log('movie list3 url is '+url, level=xbmc.LOGNOTICE)
    #referurl = url
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/'
    srcRegex = ' href="(.+?)"><b><'
    #titleRegex = ' alt="(.+?)" width'
    titleRegex = ' title="(.+?).jpg"'
    imgRegex = '<img src="(.+?)" width='
    html =  requests.get(url).text
    #html =  requests.get('http://isaidubs.net/tamil-2018-dubbed-movies.html').text
    # match = re.compile('<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p').findall(html)
    #match = re.compile('<div class="f">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p.+?<span>Wiki</span>(.+?)</div>').findall(html)
    #match = re.compile(' /> <a href="(.+?)">.<img src="(.+?).gif" alt=. title="(.+?)"> <img').findall(html)
    #nextpage=re.findall('data-disabled="([^"]*)" href="(.+?)"', html)[-1]
    moviename=re.compile(titleRegex).findall(html)
    movielink=re.compile( srcRegex ).findall( html )
    imagepath=re.compile( imgRegex ).findall( html )
    src = zip( movielink, moviename)
    match = zip(src,imagepath)

    # Bit of a hack
    #MOVIES_URL = "http://www.einthusan.tv/movies/watch/"
    for ( movie, name ), image in match:
        xbmc.log('final movie is -'+movie+'-- image is '+image+'-- name is '+name, level=xbmc.LOGNOTICE)
        #if (1):
            #image = BASE_URL + image
            #movie = str(name)+','+str(movie)+','+lang+','
            #if 'ultrahd' in ishd:
            #    name = name + '[COLOR blue]- Ultra HD[/COLOR]'
            #    movie = movie+'itshd,'+referurl
            #else:
            #    movie = movie+'itsnothd,'+referurl
            #if 'youtube' in trailer: trail = trailer.split('watch?v=')[1].split('">')[0]
            #else: trail=None
        # addDir(name, MOVIES_URL + str(movie)+'/?lang='+lang, 2, image, lang)
        addDir(name,movie,2, image,'','', isplayable=True)
    """
    if nextpage[0]!='true':
        nextPage_Url = BASE_URL+nextpage[1]
        if (page > NUMBER_OF_PAGES):
            addDir('>>> Next Page >>>', nextPage_Url,1,'','')
        else:
            get_movies_and_music_videos_helper(name, nextPage_Url, language, mode, page+1)
    """
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
##
# Displays the menu for mp3 music..
# Called when id is 16
## 


def movie_final(name, url, language, mode):
    xbmc.log('movie final url is '+url, level=xbmc.LOGNOTICE)
    #referurl = url
    srcRegex = ' /> <a href="(.+?)">'
    titleRegex = ' /> <a href="(.+?)">'
    imgRegex = '<img src="(.+?).gif" alt='
    html =  requests.get(url).text
    #html =  requests.get('http://isaidubs.net/tamil-2018-dubbed-movies.html').text
    # match = re.compile('<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p').findall(html)
    #match = re.compile('<div class="f">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p.+?<span>Wiki</span>(.+?)</div>').findall(html)
    #match = re.compile(' /> <a href="(.+?)">.<img src="(.+?).gif" alt=. title="(.+?)"> <img').findall(html)
    #nextpage=re.findall('data-disabled="([^"]*)" href="(.+?)"', html)[-1]
    moviename=re.compile(titleRegex).findall(html)
    movielink=re.compile( srcRegex ).findall( html )
    imagepath=re.compile( imgRegex ).findall( html )
    src = zip( movielink, moviename)
    match = zip(src,imagepath)

    # Bit of a hack
    #MOVIES_URL = "http://www.einthusan.tv/movies/watch/"
    for ( movie, name ), image in match:
        xbmc.log('\n movie is '+movie+'-- image is '+BASE_URL+image+'-- name is '+name, level=xbmc.LOGNOTICE)
        #if (1):
            #image = BASE_URL + image
            #movie = str(name)+','+str(movie)+','+lang+','
            #if 'ultrahd' in ishd:
            #    name = name + '[COLOR blue]- Ultra HD[/COLOR]'
            #    movie = movie+'itshd,'+referurl
            #else:
            #    movie = movie+'itsnothd,'+referurl
            #if 'youtube' in trailer: trail = trailer.split('watch?v=')[1].split('">')[0]
            #else: trail=None
        # addDir(name, MOVIES_URL + str(movie)+'/?lang='+lang, 2, image, lang)
        addDir(name,movie,2, (BASE_URL + image),'','', isplayable=True)
    """
    if nextpage[0]!='true':
        nextPage_Url = BASE_URL+nextpage[1]
        if (page > NUMBER_OF_PAGES):
            addDir('>>> Next Page >>>', nextPage_Url,1,'','')
        else:
            get_movies_and_music_videos_helper(name, nextPage_Url, language, mode, page+1)
    """
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def mp3_menu(name, url, language, mode):
    #addDir('')
    return 1

##
# Make a post request to the JSON API and list the movies..
# Interacts with the other interfaces..
##
def list_movies_from_JSON_API(name, url, language, mode):
    # HACK: Used "url" to transport postData because we know the API url
    #       and dont need it here.
    postData = url
    response = JSONInterface.apply_filter(postData)

    if ('results' in response):
        movie_ids = response['results']

        bluray = False
        if (url.find('bluray') > -1):
            bluray = True
        add_movies_to_list(movie_ids, bluray)

        max_page = int(response['max_page']) 
        next_page = int(response['page']) + 1

        if (next_page <= max_page):
            cwd = ADDON.getAddonInfo('path')
            img_path = cwd + '/images/next.png' 
            addDir("[B]Next Page[/B] >>>", url + "&page=" + str(next_page), mode, img_path)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def add_movies_to_list(movie_ids, bluray):
    ADDON_USERDATA_FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    DB_FILE = os.path.join(ADDON_USERDATA_FOLDER, 'movie_info_cache.db')

    COVER_BASE_URL = 'http://www.einthusan.com/images/covers/'
    if (bluray):
        BASE_URL = 'http://www.einthusan.com/movies/watch.php?bluray=true&id='
    else:
        BASE_URL = 'http://www.einthusan.com/movies/watch.php?id='
    for m_id in movie_ids:
        movie_info = DBInterface.get_cached_movie_details(DB_FILE, m_id)
        if (movie_info == None):
            _, name, image = JSONInterface.get_movie_detail(m_id)
            if (image == None):
                image = ''
            DBInterface.save_move_details_to_cache(DB_FILE, m_id, name, image)
        else:
            _, name, image = movie_info
        addDir(name, BASE_URL + str(m_id) ,2, COVER_BASE_URL + image)

##
#  Just displays the two recent sections. Called when id is 3.
##
def show_recent_sections(name, url, language, mode):
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 

    postData = 'https://einthusan.tv/movie/results/?'+url + '&find='
    addDir('Recently Posted',  postData + 'Recent', 1, img_path + 'recently_added.png')
    #addDir('[COLOR red]Recently Viewed[/COLOR]', postData + 'RecentlyViewed', 15, img_path + 'recently_viewed.png')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

# Shows the movie in the homepage..
def show_featured_movies(name, url, language, mode):
    page_url = 'https://einthusan.tv/movie/browse/?lang=' + language

    html = requests.get(page_url).text
    matches = re.compile('name="newrelease_tab".+?img src="(.+?)".+?href="(.+?)"><h2>(.+?)</h2>.+?i class=(.+?)</div>').findall(html)

    staffPicks_matches = re.compile('  <i class="(.+?)">.+?</i>.+?</i>Subtitle</p></div><a href="(.+?)"><img src="(.+?)"> </a><a href=".+?" class="title">(.+?)</a>').findall(html)
    staffPicks_matches = staffPicks_matches[:10]

    allmatches = []
    for img, id, name, ishd in matches:
        allmatches.append((img,id,name,ishd))
    for ishd, link, image, name in staffPicks_matches:
        allmatches.append((image, link, name, ishd))

    for img, id, name, ishd in allmatches:
        print id 
        movieid = id.split('/')[3]
        movielang= id.split('lang=')[1]
        movie = name+','+movieid+','+movielang
        if 'ultrahd' in ishd:
            title=name + '[COLOR blue]- Ultra HD[/COLOR]'
            movie = movie+',itshd,'+page_url
        else:
            title=name
            movie = movie+',itsnothd,'+page_url
        link = 'http://www.einthusan.tv'+str(id)
        image = 'http:'+img

        addDir(title, movie, 2, image, language, isplayable=True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    # s.close()

##
# Displays the options for Top Rated. Called when id is 5.
##
def show_top_rated_options(name, url, language, mode):
    cwd = ADDON.getAddonInfo('path')
    img_path = cwd + '/images/' 

    postData = url + '&find=Rating&filtered='
    addDir('Romance', postData + 'Romance', 15, img_path + 'romance.png')
    addDir('Comedy', postData + 'Comedy', 15, img_path + 'comedy.png')
    addDir('Action', postData + 'Action', 15, img_path + 'action.png')
    addDir('Storyline', postData + 'Storyline', 15, img_path + 'storyline.png')
    addDir('Performance', postData + 'Performance', 15, img_path + 'performance.png')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Displays the options for A-Z view. Called when id is 8.
##
def show_A_Z(name, url, language, mode):
    
    azlist = map (chr, range(65,91))
    # postData = 'https://einthusan.tv/movie/results/?'+url + "find=Alphabets&alpha="
    addDir('Numerical', 'https://einthusan.tv/movie/results/?find=Numbers&'+url, 1, '')
    for letter in azlist:
        addDir(letter, 'https://einthusan.tv/movie/results/?alpha='+letter+'&find=Alphabets&'+url, 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
##
# Single method that shows the list of years, actors and directors. 
# Called when id is 9, 10, 11
# 9 : List of Years
# 10: List of Actors
# 11: List of directors
##

def show_list(name, b_url, language, mode):
    if (mode == 9):
        #postData = b_url + '&find=Year&year='
        values = [repr(x) for x in reversed(range(1980, date.today().year + 1))]
        for attr_value in values:
            if (attr_value != None):
                addDir('Tamil '+attr_value+' Year Movies', BASE_URL+'tamil-'+str(attr_value)+'-dubbed-movies.html', 1, '')
    elif (mode == 10):
        #postData = b_url + '&organize=Cast'
        genre_name = ['Horror','Action', 'Thriller', 'Crime', 'Mystery']
        for k in genre_name:
            addDir('Tamil '+k+' Dubbed Movies', BASE_URL+'tamil-'+k.lower()+'-dubbed-movies.html', 1, '')
        #values = JSONInterface.get_actor_list(language)
    elif (mode == 11):
        #postData = b_url + '&organize=Cast'
        addDir(name, b_url, 4, '')
    elif (mode == 12):
        #postData = b_url + '&organize=Cast'
        addDir(name, b_url, 5, '')
    elif (mode == 13):
        #postData = b_url + '&organize=Cast'
        addDir(name, b_url, 6, '')
    else:
        postData = b_url + '&organize=Director'
        values = JSONInterface.get_director_list(language)

    # postData = postData + '&filtered='

    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows the search box for serching. Shown when the id is 6.
##
def show_search_box(name, url, language, mode):
    # search_term = GUIEditExportName("")
    keyb = xbmc.Keyboard('', 'Search for Movies')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search_term = urllib.quote_plus(keyb.getText()) 
        postData = 'https://einthusan.tv/movie/results/?'+url+'&query=' + search_term
        headers={'Origin':'https://einthusan.tv','Referer':'https://einthusan.tv/movie/browse/?'+url,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        html = requests.get(postData, headers=headers).text
        match = re.compile('<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p').findall(html)
        nextpage=re.findall('data-disabled="([^"]*)" href="(.+?)"', html)[-1]

        for movie, lang, image, name, ishd in match:
            image = 'http:' + image
            movie = str(name)+','+str(movie)+','+lang+','
            if 'ultrahd' in ishd:
                name = name + '[COLOR blue]- Ultra HD[/COLOR]'
                movie = movie+'itshd,'+postData
            else:
                movie = movie+'itsnothd,'+postData
            # addDir(name, MOVIES_URL + str(movie)+'/?lang='+lang, 2, image, lang)
            
            addDir(name,movie,2,image,lang, isplayable=True)
        if nextpage[0]!='true':
            addDir('>>> Next Page >>>', BASE_URL+nextpage[1],1,'','')

    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

##
#  Displays a list of music videos
##
def list_music_videos(name, url, language, mode):
    if (url == "" or url == None):
        url = 'http://www.einthusan.com/music/index.php?lang=' + language 
    get_movies_and_music_videos(name, url, language, mode)

def http_request_with_login(url):
    username = xbmcplugin.getSetting(int(sys.argv[1]), 'username')
    password = xbmcplugin.getSetting(int(sys.argv[1]), 'password')

    ADDON_USERDATA_FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    COOKIE_FILE = os.path.join(ADDON_USERDATA_FOLDER, 'cookies')
    return HTTPInterface.http_get(url, COOKIE_FILE,username, password)

def decodeEInth(lnk):
    t=10
    #var t=10,r=e.slice(0,t)+e.slice(e.length-1)+e.slice(t+2,e.length-1)
    r=lnk[0:t]+lnk[-1]+lnk[t+2:-1]
    return r
def encodeEInth(lnk):
    t=10
    #var t=10,r=e.slice(0,t)+e.slice(e.length-1)+e.slice(t+2,e.length-1)
    r=lnk[0:t]+lnk[-1]+lnk[t+2:-1]
    return r
"""
def resolve_url(url):
    duration=7500   
    try:
        stream_url = urlresolver.HostedMediaFile(url=url).resolve()
        # If urlresolver returns false then the video url was not resolved.
        if not stream_url or not isinstance(stream_url, basestring):
            try: msg = stream_url.msg
            except: msg = url
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('URL Resolver',msg, duration, _icon))
            return False
    except Exception as e:
        try: msg = str(e)
        except: msg = url
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('URL Resolver',msg, duration, _icon))
        return False
        
    return stream_url 
"""
##
# Plays the video. Called when the id is 2.
##
def play_video(name, url, language, mode):
    
    s = requests.Session()
    isithd='fake'
    # "Playing: " + name + ", with url:"+ url)
    xbmc.log('Play list video url is '+url, level=xbmc.LOGNOTICE)
    #name,url,lang,isithd,referurl=url.split(',')
    
    if isithd=='itshd':
        dialog = xbmcgui.Dialog()
        ret = dialog.select('Quality Options', ['Play UHD', 'Play HD/SD'])
        
        if ret ==0:
            # isithd = 'itshd'
            headers={'Origin':'https://einthusan.tv','Referer':'https://einthusan.tv/movie/browse/?lang=hindi','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            mainurl='https://einthusan.tv/movie/watch/%s/?lang=%s&uhd=true'%(url,lang)
            mainurlajax='https://einthusan.tv/ajax/movie/watch/%s/?lang=%s&uhd=true'%(url,lang)
            login_info(s, referurl)
            get_movie(s,mainurl,mainurlajax, headers)
        if ret ==1:
            # isithd = 'itsnothd'
            mainurl='https://einthusan.tv/movie/watch/%s/?lang=%s'%(url,lang)
            mainurlajax='https://einthusan.tv/ajax/movie/watch/%s/?lang=%s'%(url,lang)
            headers={'Origin':'https://einthusan.tv','Referer':'https://einthusan.tv/movie/browse/?lang=hindi','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            get_movie(s,mainurl,mainurlajax, headers)
    else:
        #mainurl='https://einthusan.tv/movie/watch/%s/?lang=%s'%(url,lang)
        #mainurlajax='https://einthusan.tv/ajax/movie/watch/%s/?lang=%s'%(url,lang)
        #headers={'Origin':'https://einthusan.tv','Referer':'https://einthusan.tv/movie/browse/?lang=hindi','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        #headers={'Origin':'http://d9.uptofiles.site//','Referer':'http://d9.uptofiles.site//','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        #get_movie(s,mainurl,mainurlajax, headers)
        #get_movie(s,url,url, headers)
        #urlnew=s.get(url).text.encode('utf-8')
        #url2=s.get(url, headers=headers, cookies=s.cookies).text.encode('utf-8')
        #xbmc.log('session url is '+url2, level=xbmc.LOGNOTICE)
        listitem = xbmcgui.ListItem( label = name, iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
        #listitem =xbmcgui.ListItem(path=url)
        listitem.setProperty('IsPlayable', 'true')
        #listitem.setContentLookup(False)
        #stream_url = resolve_url(url)
        #if stream_url:
            #listitem.setPath(stream_url)
        listitem.setPath(path=url.replace(' ', '%20'))
        #listitem.setPath(path="http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")
        #listitem.setPath(path='http://d9.uptofiles.site//files/Tamil%20Dubbed%20Movies/The%20Equalizer%202%20(2018)/The%20Equalizer%202%20(640x360)/The%20Equalizer%202%20HD.mp4')
        #listitem.setMimeType('mime/x-type')
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
        #xbmc.Player().play(item=urlnew, listitem=listitem)
        
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def get_movie(s, mainurl, mainurlajax, headers=None):
    import HTMLParser
    import json
    # htm=getUrl(mainurl,headers=headers,cookieJar=cookieJar)
    
    
    htm=s.get(mainurl, headers=headers, cookies=s.cookies).text.encode('utf-8')
    # htm, level=OTICE)
    lnk=re.findall('data-ejpingables=["\'](.*?)["\']',htm)[0]

    r=decodeEInth(lnk)
    jdata='{"EJOutcomes":"%s","NativeHLS":false}'%lnk

    h = HTMLParser.HTMLParser()
    gid=re.findall('data-pageid=["\'](.*?)["\']',htm)[0]
    
    gid=h.unescape(gid).encode("utf-8") 

    postdata={'xEvent':'UIVideoPlayer.PingOutcome','xJson':jdata,'arcVersion':'3','appVersion':'59','gorilla.csrf.Token':gid}
    
    rdata=s.post(mainurlajax,headers=headers,data=postdata,cookies=s.cookies).text
    
    r=json.loads(rdata)["Data"]["EJLinks"]
    xbmc.log(str(decodeEInth(r).decode("base64")), level=xbmc.LOGNOTICE)
    lnk=json.loads(decodeEInth(r).decode("base64"))["HLSLink"]
	
    lnk = preferred_server(lnk, mainurl)
			
    xbmc.log(lnk, level=xbmc.LOGNOTICE)
      
    urlnew=lnk+('|https://einthusan.tv&Referer=%s&User-Agent=%s'%(mainurl,'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'))
    listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ) )
    
    # listitem =xbmcgui.ListItem(name)
    listitem.setProperty('IsPlayable', 'true')
    listitem.setPath(urlnew)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    
    s.close()
    # xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def preferred_server(lnk, mainurl):
	xbmc.log(location, level=xbmc.LOGNOTICE)
	if location != 'No Preference':
		if location == 'Dallas':
			servers = [23,24,25,29,30,31,35,36,37,38,45]
		elif location == 'Washington D.C':
			servers = [1,2,3,4,5,6,7,8,9,10,11,13,41,44]
		elif location == 'San Francisco':
			servers = [19,20,21,22,46]
		elif location == 'Toronto':
			servers = [26,27]
		elif location == 'London':
			servers = [14,15,16,17,18,32,33,39,40,42]
		else: # location == 'Sydney'
			servers = [28,34,43]
			
		server_n = lnk.split('.einthusan.tv')[0].strip('https://s')
		SERVER_OFFSET = []
		if int(server_n) > 100:
			SERVER_OFFSET.append(100)
		else:
			SERVER_OFFSET.append(0)
		servers.append(int(server_n) - SERVER_OFFSET[0])
		vidpath = lnk.split('.tv/')[1]
		new_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'Referer':mainurl, 'Origin':'https://einthusan.tv'}
		for i in servers:
			urltry = ("https://s" + str(i+SERVER_OFFSET[0]) + ".einthusan.tv/" + vidpath)
			isitworking = requests.get(urltry, headers=new_headers).status_code
			xbmc.log(urltry, level=xbmc.LOGNOTICE)
			xbmc.log(str(isitworking), level=xbmc.LOGNOTICE)
			if isitworking == 200:
				lnk = urltry
				break
	return lnk
	
def login_info(s, referurl):
    
    headers={'Host':'einthusan.tv', 'Origin':'https://einthusan.tv','Referer':referurl,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    
    htm = s.get('https://einthusan.tv/login/?lang=hindi', headers=headers, allow_redirects=False).content
    csrf=re.findall('data-pageid=["\'](.*?)["\']',htm)[0]
    if '&#43;' in csrf: csrf = csrf.replace('&#43;', '+')
    
    body = {'xEvent':'Login','xJson':'{"Email":"'+username+'","Password":"'+password+'"}', 'arcVersion':3, 'appVersion':59,'tabID':csrf+'48','gorilla.csrf.Token':csrf}
    headers['X-Requested-With']='XMLHttpRequest'
    
    
    headers['Referer']='https://einthusan.tv/login/?lang=hindi'
    html2= s.post('https://einthusan.tv/ajax/login/?lang=hindi',headers=headers,cookies=s.cookies, data=body,allow_redirects=False) 
    
    html3=s.get('https://einthusan.tv/account/?flashmessage=success%3A%3A%3AYou+are+now+logged+in.&lang=hindi', headers=headers, cookies=s.cookies)
    
    csrf3 = re.findall('data-pageid=["\'](.*?)["\']',html3.text)[0]
    body4 = {'xEvent':'notify','xJson':'{"Alert":"SUCCESS","Heading":"AWESOME!","Line1":"You+are+now+logged+in.","Buttons":[]}', 'arcVersion':3, 'appVersion':59,'tabID':csrf+'48','gorilla.csrf.Token':csrf3}
    html4 = s.post('https://einthusan.tv/ajax/account/?lang=hindi', headers=headers, cookies=s.cookies, data=body4)
    
    return s
##
# Displays the setting view. Called when mode is 12
##
def display_setting(name, url, language, mode):
    ADDON.openSettings()

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

#########################################################
# Function  : GUIEditExportName                         #
#########################################################
# Parameter :                                           #
#                                                       #
# name        sugested name for export                  #
#                                                       # 
# Returns   :                                           #
#                                                       #
# name        name of export excluding any extension    #
#                                                       #
#########################################################
def GUIEditExportName(name):
    exit = True 
    while (exit):
          kb = xbmc.Keyboard('default', 'heading', True)
          kb.setDefault(name)
          kb.setHeading("Enter the search term")
          kb.setHiddenInput(False)
          kb.doModal()
          if (kb.isConfirmed()):
              name = kb.getText()
              exit = False
          else:
              break
    return(name)
    
def playtrailer( name,url,language,mode ):
    # dialog.notification( addon.get_name(), 'fetching trailer', addon.get_icon(), 4000)
    trail = 'plugin://plugin.video.youtube/play/?videoid='+url
    xbmc.log(trail, level=xbmc.LOGNOTICE)
    # xbmc.log(sys.argv[0], level=xbmc.LOGNOTICE)
    # xbmc.log(sys.argv[1], level=xbmc.LOGNOTICE)
    listitem = xbmcgui.ListItem(name)
    listitem.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    # xbmc.Player().play(url, listitem)
    # sys.exit()

def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok


def addDir(name, url, mode, iconimage, lang='', trail=None, isplayable=False):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&lang="+urllib.quote_plus(lang)
    xbmc.log('add dir url is '+u, level=xbmc.LOGNOTICE)
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('IsPlayable', 'true')
    isfolder=True
    if isplayable:
        isfolder=False
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isfolder)
    return ok

params=get_params()
url=''
name=''
mode=0
language=''

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass

try:
    name=urllib.unquote_plus(params["name"])
except:
    pass

try:
    mode=int(params["mode"])
except:
    pass

try:
    language=urllib.unquote_plus(params["lang"])
except:
    pass

# Modes
# 0: The main Categories Menu. Selection of language
# 1: For scraping the movies from a list of movies in the website
# 2: For playing a video
# 3: The Recent Section
# 4: The top viewed list. like above
# 5: The top rated list. Like above
# 6: Search options
# 7: Sub menu
# 8: A-Z view.
# 9: Yearly view
# 10: Actor view
# 11: Director view
# 12: Show Addon Settings

function_map = {}
function_map[0] = main_categories
function_map[1] = get_movies_and_music_videos
function_map[2] = play_video
function_map[3] = movie_list1
function_map[4] = movie_list2
function_map[5] = movie_list3
function_map[6] = movie_final
function_map[7] = inner_categories
function_map[9] = show_list
function_map[10] = show_list
function_map[11] = show_list
function_map[12] = display_setting
function_map[13] = show_list
"""
function_map[0] = main_categories
function_map[1] = get_movies_and_music_videos
function_map[2] = play_video
function_map[3] = show_recent_sections
function_map[4] = show_featured_movies
function_map[5] = show_top_rated_options
function_map[6] = show_search_box
function_map[7] = inner_categories
function_map[8] = show_A_Z
function_map[9] = show_list
function_map[10] = show_list
function_map[11] = show_list
function_map[12] = display_setting
function_map[13] = display_BluRay_listings
function_map[14] = list_music_videos
function_map[15] = list_movies_from_JSON_API
function_map[16] = mp3_menu
"""
function_map[mode](name, url, language, mode)