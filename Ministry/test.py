import scrapy
from scrapy import FormRequest
import re

class GovernSpider(scrapy.Spider):
    name = 'govern'
    start_urls = ['https://pib.gov.in/allRel.aspx']

    def txt_cleaner(self,txt):

        cleaned_string = txt.strip()

        cleaned_string = cleaned_string.replace('\r', ' ').replace('\n', ' ')

        cleaned_string = re.sub(' +', ' ', cleaned_string)

        return cleaned_string

    def parse(self,response):
        data = {
            'ctl00$Bar1$ddlregion': '3',
            'ctl00$Bar1$ddlLang': '1',
            'ctl00$ContentPlaceHolder1$hydregionid': '3',
            'ctl00$ContentPlaceHolder1$hydLangid': '1',
            'ctl00$ContentPlaceHolder1$ddlMinistry': '0', #means all ministries
            'ctl00$ContentPlaceHolder1$ddlday': '0', #means all days
            'ctl00$ContentPlaceHolder1$ddlMonth': '7', #5 means may if you want to extract data for Aug put 8 for example 
            'ctl00$ContentPlaceHolder1$ddlYear': '2024', #year
        }

        yield FormRequest.from_response(response, formdata= data, callback=self.parse_urls)

    def parse_urls(self,response):

        hrefs = response.css('ul.leftul li a::attr(href)').getall()
        
        base_url = 'https://pib.gov.in'
        all_urls_to_scrape = [base_url + href for href in hrefs]

        for url in all_urls_to_scrape:

            yield response.follow(url,callback= self.parse_article)

    def parse_article(self,response):

        all_text = response.css('.innner-page-main-about-us-content-right-part *::text').getall()
        combined_text = ' '.join(all_text).strip()

        main_content_div = response.css('div.innner-page-main-about-us-content-right-part')
        img_src = main_content_div.css('img::attr(src)').getall()
        iframe_src = main_content_div.css('iframe::attr(src)').getall()
        all_image_src = img_src + iframe_src

        if len(all_image_src) == 0:
            all_image_src = "there is no image for this article"


        info = {
            'title': self.txt_cleaner(response.css("div h2::text").get()),
            'date_posted': self.txt_cleaner(response.css('div.ReleaseDateSubHeaddateTime::text').get()),
            'content': self.txt_cleaner(combined_text),
            'images': all_image_src
        }


        yield info

