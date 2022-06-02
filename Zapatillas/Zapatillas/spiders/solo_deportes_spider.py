import scrapy
import time
from scrapy.crawler import CrawlerProcess

class sd_Spider(scrapy.Spider):#ok
    name='sd'
    base = 'https://www.solodeportes.com.ar/hombre/calzado.html?p={}&_=16538649558{}'
    numero1=1
    numero2=16
    
    start_urls = [base.format("1","16")]
    custom_settings = {
        'FEED_URI':'lista_de_precios_sd.json',
        'FEED_FORMAT':'json'
    }   

    def parse(self, response):
        precio_producto = response.xpath('//li[@class="item product product-item"]//div//div//a//div//span[@class="old-price"]//span//span/@content').getall()
        nombre_producto = response.xpath('//li[@class="item product product-item"]//div//div//a/@title').getall()
        siguiente_pagina= self.numero1
    
        dicionario_de_precios= dict(zip(nombre_producto,precio_producto))

        yield dicionario_de_precios
        
        if siguiente_pagina<=32:

            self.numero1+=1
            self.numero2+=1

            a=self.numero1
            a=str(a)
            b=self.numero2
            b=str(b)

            siguiente_pagina = self.base.format(a,b)
            print("***NEXT PAGE ***")
            time.sleep(3)
            yield response.follow(siguiente_pagina,callback=self.parse)

if __name__ == '__main__':

    procesar = CrawlerProcess()
    procesar.crawl(sd_Spider)
    procesar.start()