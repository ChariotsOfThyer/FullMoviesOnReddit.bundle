NAME = "Full Movies on Reddit"
ART = 'art-default.jpg'
ICON = 'icon-default.png'
BASE_URL = 'http://www.reddit.com/user/rdjdnd/m/redditvideos.json'

def Start():
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = NAME
    DirectoryObject.thumb = R(ICON)
    NextPageObject.thumb = R(ICON)
    VideoClipObject.thumb = R(ICON)


@handler('/video/fullmoviesonreddit', NAME, thumb=ICON, art=ART)
def MainMenu():
    return GetVideos()

@route('/video/fullmoviesonreddit/getvideos')
def GetVideos(url=BASE_URL, count=0, limit=25):
    oc = ObjectContainer(title2=NAME)
    data = JSON.ObjectFromURL(url, cacheTime=0)
    after = data['data'].get('after')
    before = data['data'].get('before')
    count = int(count) + 25

    if before:
        prev_count = count - 24
        prev_link = url + '?count=' + str(prev_count) + '&before=' + before
        oc.add(DirectoryObject(
            key=Callback(GetVideos, url=prev_link, count=count),
            title='<< previous'
        ))

    children = data['data']['children']
    if children:
        for child in children:
            data = child['data']
            if 'media' in data:            
                if data['media'] != None:
                    video = data['media']['oembed']
                else:
                    video = data                
                
                if 'url' not in video:
                    video['url'] = data['url']               
                
                if 'description' not in video:
                    video['description'] = ''
                    
                if 'thumbnail_url' not in video:
                    video['thumbnail_url'] = ''                
                   
                if URLService.ServiceIdentifierForURL(video['url']) is not None:
                    oc.add(VideoClipObject(
                        url = video['url'],
                        title = video['title'],
                        summary = video['description'],
                        thumb = video['thumbnail_url'] 
                    ))

    if after:
        next_link = url + '?count=' + str(count) + '&after=' + after
        oc.add(DirectoryObject(
            key=Callback(GetVideos, url=next_link, count=count),
            title='next >>'
        ))

    return oc