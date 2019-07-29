from .models import Page, Image
from django.shortcuts import render, redirect
from .classes import Crawler, dbHandler, urlParser
from threading import Thread
import math

def index(request): 
    return render(request, 'index.html')

def search(request):
    try:
        term = request.GET['term']
    except Exception as e:
        return redirect('index')
    try:
        type = request.GET['type']
    except Exception as e:
        type = "sites"
    try:
        pageNo = int(request.GET['page'])
    except Exception as e:
        pageNo = int(1)

    if(type == 'sites'):
        perPage = int(20)
        startIndex = (pageNo - 1) * perPage
        resultNum = Page.objects.all().count()
        endIndex = startIndex + perPage
        if(endIndex > resultNum): 
            endIndex = resultNum
            startIndex = endIndex - perPage
        if startIndex < 0: startIndex = 0
        pageNum = math.ceil(resultNum / perPage)
        try:
            allPages = Page.objects.filter(title__icontains=term)[startIndex: endIndex]
        except Exception as e:
            allPages = []
        numbers = [num for num in range(1, pageNum+1)]
        context = {
            'allPages': allPages, 
            'resultNum': len(allPages), 
            'term': term, 
            'type': type, 
            'ifSites': True,
            'pageNum': pageNo,
            'numbers': numbers
        }
        return render(request, 'search.html', context)

    elif(type == 'images'):
        perPage = int(30)
        startIndex = (pageNo - 1) * perPage
        resultNum = Image.objects.filter(src__icontains=term).count()
        endIndex = startIndex + perPage + 1
        if(endIndex >= resultNum):
            endIndex = resultNum
            startIndex = (endIndex - perPage)
        if(startIndex < 0):
            startIndex = 0
        #endif
        pageNum = math.ceil(resultNum / perPage)
        try:
            allImgs = Image.objects.filter(src__icontains=term)[startIndex: endIndex]
        except Exception as e:
            allImgs = []
        #endtry
        numbers = [num for num in pageNum+1]
        context = {
            'allImgs': allImgs, 
            'term': term, 
            'type': type, 
            'ifSites': False,
            'numbers': numbers
        }
        return render(request, 'search.html', context)

def crawler(request):
    return render(request, 'crawler.html')

def crawl(request):
    Crawler.Crawl()
    return render(request, 'crawler.html')

class storeUrl(Thread):
    def __init__(self, request):
        Thread.__init__(self)
        self.request = request

    def run(self):
        url = self.request.POST['url']
        try:
            parser = urlParser.Parse(url)
            title = parser.getTitle()
            description = parser.getDescription()
            keywords = parser.getKeywords()
        except Exception as e:
            print(e)
        if(not(dbHandler.ifUrlExists(url))):
            try:
                dbHandler.insertUrl(title, url, description, keywords)
                print("url inserted: " + url)
            except Exception as e:
                print(e)

def addUrl(request):
    stores = storeUrl(request)
    stores.start()
    return render(request, 'crawler.html')


