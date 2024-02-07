import re

import requests
import pandas
from lxml import etree
import time
import pandas as pd
from openpyxl import load_workbook
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By

brower = webdriver.Chrome()

def get_data1():

    list_main=[]
    url = "https://hk.centanet.com/findproperty/en/list/buy"
    brower.get(url)
    time.sleep(2)

    # brower.set_page_load_timeout(2)
    # try:
    #     brower.get(url)
    # except Exception:
    #     brower.execute_script('window.stop()')

    # ...

    for i in range(1,418):#24

        strhtml = brower.page_source

        etree_html = etree.HTML(strhtml)

        list_qy = etree_html.xpath("//div[@class='list']")

        if len(list_qy)>0:
            for item_qy in list_qy:

                try:
                    name = item_qy.xpath("string(./a//span[@class='title-lg'])")
                    href = item_qy.xpath("./a/@href")[0]
                    href = "https://hk.centanet.com" + href
                    list_main.append([name,href])
                    print("{} {}".format(name,href))
                except:
                    pass


        try:

            qc = brower.find_element(By.XPATH, "//button[@class='btn-next']")
            #brower.execute_script("arguments[0].click();", qc)
            qc.click()
            time.sleep(1)
            # brower.set_page_load_timeout(2)
            # try:
            #     qc = brower.find_element(By.XPATH,"//button[@class='btn-next']")
            #     brower.execute_script("arguments[0].click();", qc)
            #     time.sleep(1)
            # except Exception:
            #     brower.execute_script('window.stop()')

        except:
                pass


    df1 = pd.DataFrame(list_main, columns=["name_1",'link'])  
    df1.to_excel("links.xlsx", sheet_name='info', index=False)

def get_detail():
    list_main  =[]
    df_main = pd.read_excel("links.xlsx")
    for index,row in df_main.iterrows():
        try:
            href = row["link"]
            name1 = row["name_1"]

            brower.set_page_load_timeout(2)
            try:
                brower.get(href)
            except Exception:
                brower.execute_script('window.stop()')
            strhtml = brower.page_source

            etree_html = etree.HTML(strhtml)
            try:
                sxmc = etree_html.xpath("string(//div[@class='flex-between']//div[1]//p)")
                sxblsd = etree_html.xpath("string(//p[@class='info-address']/span)")
                sszt = etree_html.xpath("string(//div[@class='property-area']/div[contains(string(.),'S.A.')]/p[@class='a-row']/span[@class='txt-place subtxt'])")
                sfwb = etree_html.xpath("string(//div[@class='property-area']/div[contains(string(.),'GFA')]/p[@class='a-row']/span[@class='txt-place subtxt'])")

                list_main.append([href,name1,sxmc,sxblsd,sszt,sfwb])
                print("{} {} {} {}".format(sxmc,sxblsd,sszt,sfwb))

            except:
                list_main.append([href, name1, "", "", "",""])
                pass
        except:
            pass
        df1 = pd.DataFrame(list_main, columns=['link','name_1','name_2','address','S.A.','GFA'])  
        df1.to_excel("outdata.xlsx", sheet_name='info', index=False)

if __name__ == '__main__':

    get_data1()
    #get_detail()
