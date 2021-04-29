import scrapy
from ..items import  AmazonscrapingItem


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    page_number=2
    start_urls = [
        'https://www.amazon.com/s?bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&qid=1618578208&rnid=1250225011&ref=lp_1000_nr_p_n_publication_date_0'
    ]

    def parse(self, response):
        items=AmazonscrapingItem()

        product_name=response.css('.a-color-base.a-text-normal::text').extract()
        product_author=response.css('.a-color-secondary .a-size-base.a-link-normal').css('::text').extract()
        product_price=response.css('.a-spacing-top-small .a-price-whole').css('::text').extract()
        product_imagelink = response.css('.s-image::attr(src)').extract()
        product_review = response.css('.aok-align-bottom').css('::text').extract()

        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_imagelink'] = product_imagelink
        items['product_review'] = product_review
        yield items

        next_page='https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&dc&page='+str(AmazonSpiderSpider.page_number)+'&qid=1618992056&rnid=1250225011&ref=sr_pg_2'
        if AmazonSpiderSpider.page_number<=16:
            AmazonSpiderSpider.page_number+=1
            yield response.follow(next_page, callback=self.parse)