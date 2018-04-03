# #importing libraries
# import urllib.request
# from bs4 import BeautifulSoup
#
# #specify url
# quote_page = 'http://pickup-lines.net/'
#
# #query the website and return the html to the variable 'page'
# page = urllib.request.urlopen(quote_page)
# print(page)
#
# #parse the html using BeautifulSoup and store in variable 'soup'
# soup = BeautifulSoup(page,'html.parser')
#
# #Take the <div> of the name and get its value
# name_box = soup.find('span', attrs = {'class': 'loop-entry-line'})
#
# name = name_box.text.strip() #strip() is used to remove starting and trailing
# print(name)


# """Attempt from stackoverflow"""
# from urllib.request import Request, urlopen
#
# req = Request('http://pickup-lines.net/')
# webpage = urlopen(req).read()

"""second attempt from stackoverflow"""
import urllib.request
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
response = opener.open('http://pickup-lines.net/')
