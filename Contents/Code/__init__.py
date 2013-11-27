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
			try:
				item = child['data']
				video_url = item['url']
				title = item['title']
				if 'search_query' in video_url:
					continue

				video = URLService.MetadataObjectForURL(video_url + '?title=' + title)
				video.title = title
				oc.add(video)
			except:
				pass

	if after:
		next_link = url + '?count=' + str(count) + '&after=' + after
		oc.add(DirectoryObject(
			key=Callback(GetVideos, url=next_link, count=count),
			title='next >>'
		))

	return oc