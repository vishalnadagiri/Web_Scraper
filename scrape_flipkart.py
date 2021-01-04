from selenium import webdriver
from bs4  import BeautifulSoup
import pandas as pd

import requests
import os
import re

driver = webdriver.Chrome(r"C:\Users\User\Downloads\Compressed\chromedriver_win32_2\chromedriver.exe")

srch_url="https://www.flipkart.com/womens-dresses/pr?sid=clo%2Codx%2Cmaj%2Cjhy&marketplace=FLIPKART&otracker=product_breadCrumbs_Women%27s+Dresses"

def down_img(url,scd):
    img_data = requests.get(url).content
    if not os.path.exists('downloaded_image'):
        os.makedirs('downloaded_image')
    else:
        img_name=os.getcwd()+'/downloaded_image'+'/image_SC_%s_.jpg'%scd
        with open(img_name, 'wb') as handler:
            handler.write(img_data)
            print(img_name+'  Image downloaded')
        return './downloaded_image'+'/image_SC%s_.jpg'%scd


class scrape_one_prod:
    def __init__(self):
        self.name= list()
        self.price = list()
        self.dis = list()
        self.url = []
        
    def scrape_details(self,srch_url,pg_no):
        driver.get(srch_url+r'&page='+str(pg_no))
        content = driver.page_source
        soup = BeautifulSoup(content)
        products, prices,dis,url = list(),list(),list(),[]
        oth_dic ={}
        for i,a in enumerate(soup.findAll(attrs={'class':'_2B099V'})[0]):
#             print(a.find('div',attrs={'class':'_2pi5LC'}))
            self.name=a.find('a',attrs='IRpwTa')
#             print(self.name.text)
            self.dis=a.find('div',attrs='_3Ay6Sb')
            self.price=a.find('div',attrs='_30jeq3')
            self.url=a.find('a',attrs='IRpwTa')['href']
            products.append(self.name.text)
            prices.append(self.price.text)
            dis.append(self.dis.text)
            url.append('https://www.flipkart.com'+self.url)
#             oth_dic = self.scrape_product(str(url[i]))
            oth_dic.update({'Product_name':products,'Price':prices,'Didcount':dis,'P_URL':url})
        return oth_dic
    
    def scrape_product(self,url_):
#         print(url_)
        driver.get(url_)
        content_=driver.page_source
        soup = BeautifulSoup(content_)
        otdic = dict()
        dec,colr_,col,siz = str(),str(),list(),list()
        #Description
        if soup.find('div',attrs='_1AN87F'):
            dec = soup.find('div',attrs='_1AN87F').text
#             otdic.update({'Description':dec})
#             print('Product Decription found :'+otdic['Description']
        else:
            dec = None
#             otdic.update({'Description':'None'})
            
        #Color    
        if soup.find('li',attrs={'id':re.compile('-color')}):
            for itm in soup.find_all('li','_3V2wfe _31hAvz'):
                if itm.find('a','kmlXmn PP89tw'):
            #         print(itm.find('a','kmlXmn PP89tw')['href'])
            #         print(itm.find('div','_3Oikkn _3_ezix _2KarXJ _31hAvz').text)
                    colr_ = itm.find('div','_3Oikkn _3_ezix _2KarXJ _31hAvz').text
#                     otdic.update({'P_Color':colr_})
#                     print('Product Color :'+otdic['P_Color'])
        else:
            colr_=None
#             otdic.update({'P_Color':'None'})
            
         
        #Available colors
#         col=[]
        if soup.find('li',{'id':re.compile('-color')}):
            for items in soup.find_all('li',{'class':'_3V2wfe _31hAvz','id':re.compile('-color')}):
                col.append(items.find('div','_3Oikkn _3_ezix _2KarXJ _31hAvz').text)
            #     print(items.find('div','_3Oikkn _3_ezix _2KarXJ _31hAvz').text)
#             otdic.update({'Avl_Color':col})
#             print('Available COlors ',end='\t')
#             print(otdic['Avl_Color'])
        else:
            col =[None]
#             otdic.update({'Avl_Color':'None'})
        
        #Available sizes
#         siz = []
        if soup.find('li',{'id':re.compile('-size')}):
            for items in soup.find_all('li',{'class':'_3V2wfe _31hAvz','id':re.compile('-size')}):
                siz.append(items.find('div',attrs={'class':re.compile('_3Oikkn _3_ezix _2KarXJ _31hAvz')}).text)
            #     print(items.find('div','_3Oikkn _3_ezix _2KarXJ _31hAvz').text)            
#             otdic.update({'Avl_Size':siz})
#             print('Available Size ',end='\t')
#             print(otdic['Avl_Size']) 
        else:
            siz = [None]
#             otdic.update({'Avl_Size':'None'})
        
        #Image URL
#         if soup.find('img','_2r_T1I _396QI4'):
        img_url_ = soup.find('img','_2r_T1I _396QI4')['src']
        
        for k,v in zip(soup.find_all('div',attrs=['_2H87wv',]), soup.find_all('div',attrs=['_2vZqPX'])):
#             print(k.text+': '+v.text)
            otdic.update({k.text:v.text})
        im_path = down_img(img_url_,otdic['Style Code'])
        otdic.update({'Description': dec, 'P_Color':colr_ , 'Avl_Color': col, 'Avl_Size':siz ,'Image_path':im_path})
        return otdic
#         pass
        
scrapper = scrape_one_prod()

df = pd.DataFrame()
for i in range(1,6):
    ot_dic = scrapper.scrape_details(srch_url,i)
#     print(srch_url+str(i))
#     dic = {'Product Name':name,'Price':price,'Rating':dis,'url':url}
#     dic.update
    df = df.append(pd.DataFrame(ot_dic),ignore_index=True)
    print('Extracted %d Page products'%i)

