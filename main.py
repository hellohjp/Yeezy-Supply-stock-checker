import requests
import json
from bs4 import BeautifulSoup as bs
from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

s = requests.Session()
requests.packages.urllib3.disable_warnings()

url = "https://www.yeezysupply.com"

def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

headers1 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
    }
print(Fore.GREEN + "Scraping new products from yeezy home page")

r = s.get(url,headers=headers1,verify=False)

soup = bs(r.text, 'lxml')

new_arrivals = soup.find('script', {'id': 'js-new-arrivals-json'})
new_arrivals = json.loads(new_arrivals.text)
index = 0
products = []

for i in new_arrivals['products']:
    if i['available'] == True:
        print i['title']
        print "In stock : {}".format(i['available'])
        print "Price {} - Index {}".format(i['price'],index)
        url = "https://www.yeezysupply.com{}".format(i['url'])
        print "\n"
        index += 1
        products.append(url)

indexchoice = raw_input("which index do you want to get cart details for? (examaple 12 or 25) : ")
#
producturl = products[int(indexchoice)]

r = s.get(producturl,headers=headers1,verify=False)

data = find_between (r.text,'"variants":','},"page')

data = json.loads(data)
sizes =  {option['public_title']: option['id'] for option in data}

for size, ID in sizes.items():
    print '{}: {} '.format(size, ID),
    print "\n"
print "\n"
productidselection = raw_input("Which size do you want top add to cart? (example S or XS): ").upper()
productid = sizes[productidselection]
#
carturl = "https://yeezysupply.com/cart/{}:1".format(productid)


r = s.get(carturl,headers=headers1,verify=False)
if 'Return to cart' not in r.text:
    print (Fore.RED +"!! FAILED TO ADD TO CART !!")
else:
    print (Fore.GREEN +"** ADDED TO CART **")
    print  "use this url and your product will be in cart {} ".format(r.url)
