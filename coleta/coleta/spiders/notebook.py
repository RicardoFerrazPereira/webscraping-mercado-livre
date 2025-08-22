import scrapy


class NotebookSpider(scrapy.Spider):
    name = "notebook"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebook#D[A:notebook]"]

    def parse(self, response):

        produtos = response.css("div.ui-search-result__wrapper")

        for produto in produtos:

            yield {
                "seller": produto.css("span.poly-component__seller::text").get(),
                "name": produto.css("a.poly-component__title::text").get(),
            }
