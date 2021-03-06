from bs4 import BeautifulSoup
import urllib.parse

def google_result(text):
	soup = BeautifulSoup(text, 'html.parser')
	url = soup.find_all('div')
	url = [x for x in url if x.find('h3')]
	urls = []
	for index, item in enumerate(url):
		link = item.find('h3').find('a')
		if not hasattr(link, 'get'):
			continue
		href = link.get('href')

		item_url = href.split('=', 1)[1].split('&')[0]

		if not item_url.startswith('http'):
			continue

		snippets = [x.text for x in item.find_all('span') if x.text]
		if len(snippets) != 0:
			snippet = urllib.parse.unquote(snippets[0])
		else:
			snippet = ''

		name = urllib.parse.unquote(link.text)
		urls.append((urllib.parse.unquote(item_url), name, snippet))
		break
	if not urls:
		return
	else:
		domain = urllib.parse.urlparse(urls[0][0]).netloc
		return {'title': urls[0][1],
			'description': urls[0][2],
			'url': urls[0][0],
			'domain': domain}