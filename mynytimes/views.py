from django.http import HttpResponse
import cookielib, urllib2

def removeNyTimesTracker(host, htmlContent):
	# For every ?hp" found in content, replace with empty string
	returnContent = htmlContent.replace('?hp"', '"')
	
	# Ensure every link directs user to page relative to host server
	returnContent = returnContent.replace('a href="http://', 'a href="http://' + host + '/')
	returnContent = returnContent.replace('href="/', 'href="http://' + host + '/www.nytimes.com/')
	
	return returnContent

def home(request):
	
	response = urllib2.urlopen('http://www.nytimes.com')
	
	origContent = response.read()
	newContent = removeNyTimesTracker(request.get_host(), origContent)
	
	return HttpResponse(newContent)
	
def timesUrl(request, url):
	# We use cookielib because some nytimes pages require cookies
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	httprequest = urllib2.Request('http://' + url)
	response = opener.open(httprequest)
	
	origContent = response.read()
	newContent = removeNyTimesTracker(request.get_host(), origContent)
	
	return HttpResponse(newContent)