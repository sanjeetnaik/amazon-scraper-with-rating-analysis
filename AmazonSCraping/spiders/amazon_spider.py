import scrapy
from ..items import  AmazonscrapingItem


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon' #name of the crawler
    page_number=2
    #start_urls is the url to scrape will be changed later down in the pagination code

    start_urls = [
        'https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&qid=1618578208&rnid=1250225011&ref=lp_1000_nr_p_n_publication_date_0'
    ]

    def parse(self, response):
        items=AmazonscrapingItem()

        #gets the details of the products we want and stores them in the variables
        product_name=response.css('.a-color-base.a-text-normal::text').extract()
        product_author=response.css('.a-color-secondary .a-size-base.a-link-normal').css('::text').extract()
        product_price=response.css('.a-spacing-top-small .a-price-whole').css('::text').extract()
        product_imagelink = response.css('.s-image::attr(src)').extract()
        product_review = response.css('.aok-align-bottom').css('::text').extract()

        #stores them in the items which is an instance of AmazonscrapingItem in items.py
        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_imagelink'] = product_imagelink
        items['product_review'] = product_review
        yield items # like a return statement gives items to AmazonscrapingItem in items.py

        #this is paginaton code which will keep moving to the other page till it passes the constraints
        next_page='https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&page='+str(AmazonSpiderSpider.page_number)+'&qid=1618992056&rnid=1250225011&ref=sr_pg_2'
        if AmazonSpiderSpider.page_number<=16: #setting the limit
            AmazonSpiderSpider.page_number+=1
            yield response.follow(next_page, callback=self.parse) #goes to the next page according to the paginaton code and calls the callback function