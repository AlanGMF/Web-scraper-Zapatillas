import scrapy
from scrapy.crawler import CrawlerProcess

class dex_Spider(scrapy.Spider):#ok
    name='dex'
    start_urls = [
        'https://www.dexter.com.ar/hombre/calzado/zapatillas',
        'https://www.stockcenter.com.ar/hombre/calzado/zapatillas',
        'https://www.moov.com.ar/hombre/calzado/zapatillas',
    ]
    custom_settings = {
        'FEED_URI':'lista_de_precios_dex.json',
        'FEED_FORMAT':'json'
    }

    def parse(self, response):
        
        precio_producto = response.xpath('//div[@class="price"]//span/span[@class="sales"]//@content').getall()
        nombre_producto = response.xpath('//div[@class="tile-body"]//div[@class="pdp-link"]//a/text()').getall()
        siguiente_pagina= response.xpath('//div[@class="text-center"]//button[@id="next"]/@data-url').get()
    
        dicionario_de_precios= dict(zip(nombre_producto,precio_producto))

        yield dicionario_de_precios
        
        if siguiente_pagina:
    
            yield response.follow(siguiente_pagina,callback=self.parse )

if __name__ == '__main__':

    procesar = CrawlerProcess()
    procesar.crawl(dex_Spider)
    procesar.start()