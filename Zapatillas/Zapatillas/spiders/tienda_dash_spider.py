import scrapy
import time
from scrapy.crawler import CrawlerProcess
digitos=("123456789.,")

class td_Spider(scrapy.Spider):#ok
    
    name='td'
    numero_pagina=1
    base = 'https://www.tiendadash.com.ar/buscapagina?fq=C%3a%2f1%2f2%2f&fq=specificationFilter_23%3aHombre&O=OrderByReleaseDateDESC&PS=24&sl=b71bf1eb-efcb-489b-ae99-6837a3c3b14e&cc=1&sm=0&PageNumber={}'
    start_urls = [base.format(str(numero_pagina))]
    
    custom_settings = {
        'FEED_URI':'lista_de_precios_td.json',
        'FEED_FORMAT':'json'
    }

    def parse(self, response):
        
        precio_productos = response.xpath('//span[@class="price"]//a//span[@class="best-price"]/text()').getall() #con espacios
        nombre_producto = response.xpath('//div[@class="product-name"]//@title').getall()
        siguiente_pagina= self.numero_pagina

        """limpiear precio"""
        nuevo_precio=''
        precios_limpios=[]

        for precio in precio_productos:
            for digito in precio:
                if digito in  digitos:
                    nuevo_precio+=digito
            precios_limpios.append(nuevo_precio)
            nuevo_precio=''

        """fin limpieza"""
        dicionario_de_precios= dict(zip(nombre_producto,precios_limpios))

        yield dicionario_de_precios
        
        if siguiente_pagina<=15:

            self.numero_pagina+=1

            a=self.numero_pagina
            a=str(a)

            siguiente_pagina = self.base.format(str(a))

            print("***NEXT PAGE ***")
            time.sleep(3)
            yield response.follow(siguiente_pagina,callback=self.parse)


if __name__ == '__main__':

    procesar = CrawlerProcess()
    procesar.crawl(td_Spider)
    procesar.start()

