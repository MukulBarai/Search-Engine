from ..models import Page, Image

def ifUrlExists(url):
    try:
        urls = Page.objects.filter(url = url)
        return len(urls) != 0
    except Exception as e:
        print("Error in ifUrlExists function")
        return 1

def ifImgSrcExists(url, imgSrc):
    try:
        srcs = Image.objects.filter(url = url, src = imgSrc)
        return len(srcs) != 0
    except Exception as e:
        print("Error in ifImgSrcExists function")
        return 1

def insertUrl(title, url, description, keywords):
    try:
        Page.objects.create(title=title, url=url, description=description)
    except Exception as e:
        raise e("Error in insertUrl function")

def insertSrc(url, src, title, alt):
    try:
        Image.objects.create(url=url, src=src, title=title, alt=alt)
    except Exception as e:
        raise e("Error in insertSrc function")

def getUrl():
    try:
        row = Page.objects.order_by('crawled').first()
        inCrawled(row.id)
        return row.url
    except Exception as e:
        raise e("Error in getting url")

def inCrawled(id):
    try:
        urlItem = Page.objects.get(pk=id)
        urlItem.crawled += 1
        urlItem.save()
    except Exception as e:
        print("Error in inCrawled function")
