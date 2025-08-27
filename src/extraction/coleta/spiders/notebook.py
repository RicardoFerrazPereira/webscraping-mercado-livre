import scrapy


class NotebookSpider(scrapy.Spider):
    name = "notebook"
    allowed_domains = ["mercadolivre.com.br"]

    # Gerando as 10 primeiras páginas direto
    start_urls = [
        f"https://lista.mercadolivre.com.br/notebook?_From={i}"
        for i in range(1, 501, 50)  # 1, 51, 101, ..., 451
    ]

    def parse(self, response):
        produtos = response.css("div.ui-search-result__wrapper")

        for produto in produtos:
            precos = produto.css("span.andes-money-amount__fraction::text").getall()

            yield {
                "name": produto.css("a.poly-component__title::text").get(),
                "seller": produto.css("span.poly-component__seller::text").get(),
                "reviews_rating": produto.css("span.poly-reviews__rating::text").get(),
                "reviews_total": produto.css("span.poly-reviews__total::text").get(),
                "old_price": precos[0] if len(precos) > 1 else None,
                "new_price": precos[-1] if precos else None,
                "url": produto.css("a.poly-component__title::attr(href)").get(),
            }
