import requests
from bs4 import BeautifulSoup

class Parse:
    def __init__(self, url):
        try:
            response = requests.get(url).text
            self.soup = BeautifulSoup(response, 'html.parser')
        except Exception as e:
            raise e("Error in initializing parser")

    def getUrls(self):
        try:
            links = self.soup.findAll('a', {'href': True})
            hrefs = [link['href'] for link in links]
            return list(dict.fromkeys(hrefs))
        except Exception as e:
            print("Error in getUrls function")
            return []

    def getImgSrcs(self):
        try:
            imgLinks = self.soup.findAll('img', {'src': True})
            return imgLinks
        except Exception as e:
            print("Error in getImgSrcs function")
            return []

    def getTitle(self):
        try:
            title = self.soup.findAll('title')[0].text
            return title
        except Exception as e:
            print("Error in getTitle function")
            return ""

    def getDescription(self):
        try:
            metas = self.soup.findAll('meta', {'name': 'description'})
            return metas[0]['content']
        except Exception as e:
            print("Error in getDescription function")
            return ""

    def getKeywords(self):
        try:
            metas = self.soup.findAll('meta', {'name': 'keywords'})
            return metas[0]['content']
        except Exception as e:
            print("Error in getKeywords function")
            return ""

if(__name__ == "__main__"):
    parser = Parse("http://www.prothomalo.com")
    print(parser.getKeywords())
