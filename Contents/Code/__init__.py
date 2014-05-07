#from requests import session
#A channel for Plex
import urllib2
from BeautifulSoup import BeautifulSoup
import feedparser
from urlparse import urlparse, urlunparse
#cateogry_page_video_url

NAME = 'PyVideo.Org'
TITLE='py'

#Dict=my_main()
#Dict.Save()
def Start():
    ObjectContainer.title1 = NAME
    HTTP.CacheTime = CACHE_1HOUR
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0'
##############################################################
@handler('/video/pyvideos', NAME)
def Main(offset=0):
    oc = ObjectContainer()
    my_dict=my_main()
    mycategories=my_dict.keys()
    #mycategories=['category1','category2']
    #count=2
    for each_category in mycategories[offset:offset+10]:
        #Log(each_category)
        oc.add(DirectoryObject(key=Callback(MainMenu,each_category=each_category),title=each_category))
        #if offset < len(mycategories):
            #oc.add(NextPageObject(key=Callback(Main, offset=offset+2), title='Moree'))
        #Log('------------------')
    if offset < len(mycategories):
        oc.add(NextPageObject(key=Callback(Main, offset=offset+10), title='Moree'))
        #oc.add(NextPageObject(key=Callback(MainMenu,each_category=each_category), title='More'))
    return oc

###############################################################
@route('/video/pyvideos/videos', NAME)
def MainMenu(each_category):
    my_dict=my_main()
    video_links=my_dict[each_category][0]
    #Log(Dict[each_category])
    oc = ObjectContainer()
    container = Container.MP4
    #category_links=my_main()
    for each_video_url in video_links:
        test=URLTest(each_video_url)
        if test=='true':
            oc.add(VideoClipObject(url=each_video_url,title='youtube',summary = 'test'))
        elif each_video_url.startswith('http'):
            oc.add(CreateVideoClipObject(url=each_video_url,summary = 'test'))
        #Log(each_video_url)
        #Log('I was here')
    return oc
###############################################################
@route('/video/pyvideos/urltest')
def URLTest(url):
  if URLService.ServiceIdentifierForURL(url) is not None:
    url_good = 'true'
  else:
    url_good = 'false'
  return url_good

###############################################################
@route('/video/pyvideos/createobject')
def CreateVideoClipObject(url, summary, title='asdfa', include_container=False):
    videoclip_obj = VideoClipObject(
	    key = Callback(CreateVideoClipObject, url=url, title=title, summary=summary,include_container=True),
	    rating_key = url,
            title='not_youtube',
	    summary = summary,
	    items = [
		    MediaObject(
			    parts = [
				    PartObject(key=url)
			    ],
			    container = Container.MP4,
			    video_codec = VideoCodec.H264,
			    video_resolution = '544',
			    audio_codec = AudioCodec.AAC,
			    audio_channels = 2,
			    optimized_for_streaming = True
		    )
	    ]
    )

    if include_container:
	return ObjectContainer(objects=[videoclip_obj])
    else:
	return videoclip_obj

###############################################################

def find_all_rss_links(content):
    rss_category_links=[]
    for each_link in content.findAll('a'):
        if each_link is not None:
            each_link_in_categorypage=str(each_link.get('href'))
            if each_link_in_categorypage.endswith('rss'):
                rss_category_links.append(each_link_in_categorypage)
    return rss_category_links
###############################################################

def normalize(url):
    """Normalize url by stripping any query and fragment parts; also,
    if original url was of the form `www.foo.com', convert this to
    `http://www.foo.com'.
    """
    (scheme, netloc, path, _, _, frag) = urlparse(url, "http")
    if not netloc and path:
        return urlunparse((scheme, path, "", "", "", ""))
    else:
        return urlunparse((scheme, netloc, path, "", "", ""))
###############################################################

def check_video_url_in_json():
    a=''
    '''need to do more for empty video_url'''
    return a
###############################################################

def extract_category_from_rsslinks(each_rss_path):
    py_category=each_rss_path.split('/')[3].replace('-', ' ')
    return py_category
###############################################################

def get_page_video_urls(resp):
    page=resp
    page_urls=[]
    video_urls=[]
    page_video_urls={}
    for each_entry in page['entries']:
        if len(each_entry['links'])>1:
            video_urls.append(each_entry['links'][1]['href'])
        else:
            video_urls.append(check_video_url_in_json())
    return video_urls
###############################################################
def extract_videourl_for_each_category(rss_category_links):
    category_page_video_url={}
    for each_rss_path in rss_category_links:
        resp=RSS.FeedFromURL('http://www.pyvideo.org'+each_rss_path)
        video_urls=get_page_video_urls(resp)
        py_category=extract_category_from_rsslinks(each_rss_path)
        category_page_video_url[py_category]=[video_urls]
    return category_page_video_url
###############################################################

def my_main():
    url='http://www.pyvideo.org/category'
    the_page_content=HTTP.Request(url).content
    Log(the_page_content)
    soup=BeautifulSoup(the_page_content)
    rss_category_links=find_all_rss_links(soup)
    category_page_video_url=extract_videourl_for_each_category(rss_category_links)
    return category_page_video_url



#if __name__=="__main__":
#    main()