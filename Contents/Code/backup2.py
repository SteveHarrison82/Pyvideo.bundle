#from requests import session
import urllib2
from BeautifulSoup import BeautifulSoup
import feedparser
from urlparse import urlparse, urlunparse


NAME = 'PyVideo.Org'
TITLE='py'

def Start():
    ObjectContainer.title1 = NAME
    HTTP.CacheTime = CACHE_1HOUR
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:23.0) Gecko/20100101 Firefox/23.0'
##############################################################       
@handler('/video/pyvideos', NAME)
def Main():
    oc = ObjectContainer()
    category_page_video_url={}
    category_page_video_url=my_main()    
    mycategories=category_page_video_url.keys()
    for each_category in mycategories:
        oc.add(DirectoryObject(key=Callback(MainMenu,category_videolinks[each_category][1]),title=each_category))
    return oc
   	
###############################################################
@route('/video/pyvideos/videos', NAME)
def MainMenu(category_links):
    #category_links=[u'http://s3.us.archive.org/nextdayvideo/chicago_djangonauts/may_2013/django_rest_framework_and_angu.mp4', u'http://05d2db1380b6504cc981-8cbed8cf7e3a131cd8f1c3e383d10041.r93.cf2.rackcdn.com/pygotham-2011/492_pygotham-2011-a-practical-guide-to-non-blocking-io-coroutines-and-concurrency.mp4', u'http://s3.us.archive.org/nextdayvideo/chicago_djangonauts/may_2013/upgrading_django.mp4', u'http://s3.us.archive.org/nextdayvideo/chicago_djangonauts/may_2013/django_rest_framework_and_angu.mp4']
    category_links=category_links
    oc = ObjectContainer()
    container = Container.MP4
    #category_links=my_main()
    for each_categorykey in category_links:
        #oc.add(DirectoryObject(key=Callback(CreateVideoClipObject,url=each_categorykey, summary='mypy'),title='asdf'))
        oc.add(CreateVideoClipObject(url=each_categorykey,summary = 'test'))
        Log(each_categorykey)
        Log('I was here')
    return oc                   
###############################
    
@route('/video/pyvideos/createobject')                        
def CreateVideoClipObject(url, summary, title='asdfa', include_container=False):
    videoclip_obj = VideoClipObject(
	    key = Callback(CreateVideoClipObject, url=url, title=title, summary=summary,include_container=True),
	    rating_key = url,
            title='mytest',
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
	Log('RETURN ONE')
	Log(include_container)
	Log(videoclip_obj)
	return ObjectContainer(objects=[videoclip_obj])
    else:
	Log('RETURN TWO')
	return videoclip_obj        
    
###############################################################

def find_all_rss_links(content):
    rss_category_links=[]
    for each_link in content.find_all('a'):
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
        page_urls.append(each_entry['links'][0]['href'])
        #print each_entry['links']
        #get_video_url_for_each_entry()
        if len(each_entry['links'])>1:
            video_urls.append(normalize(each_entry['links'][1]['href']))
        else:
            video_urls.append(check_video_url_in_json())            
        page_video_urls[each_entry['links'][0]['href']]=video_urls[-1]
    return page_urls, video_urls, page_video_urls
###############################################################

def extract_videourl_for_each_category(rss_category_links):
    category_page_video_url={}
    for each_rss_path in rss_category_links:
        resp=feedparser.parse('http://www.pyvideo.org'+each_rss_path)
        page_urls,video_urls,page_video_urls=get_page_video_urls(resp)
        py_category=extract_category_from_rsslinks(each_rss_path)
        category_page_video_url[py_category]=[page_urls,video_urls]
    return category_page_video_url    
###############################################################

def my_main():
    req = urllib2.Request('http://www.pyvideo.org/category')
    response = urllib2.urlopen(req)
    the_page_content=response.read()
    soup=BeautifulSoup(the_page_content)
    rss_category_links=find_all_rss_links(soup)
    category_page_video_url=extract_videourl_for_each_category(rss_category_links)
    return category_page_video_url
    
#if __name__=="__main__":
#    main()
    
        




