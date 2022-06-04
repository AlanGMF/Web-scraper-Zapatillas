import scrapy
from scrapy.crawler import CrawlerProcess
import csv

zapas= 'stockcenter.csv'

class Spider(scrapy.Spider):

    name='dex'
    
    start_urls = [
        'https://www.stockcenter.com.ar/hombre/calzado/zapatillas',
    ]
    
    lista_de_nombres_no_repetidos=[]

    def parse(self, response):
        
        #Selecciono elementos de la pagina
        precios_producto = response.xpath('//div[@class="price"]//span/span[@class="sales"]//@content').getall()
        nombres_producto = response.xpath('//div[@class="tile-body"]//div[@class="pdp-link"]//a/text()').getall()
        siguiente_pagina= response.xpath('//div[@class="text-center"]//button[@id="next"]/@data-url').get()

        #Se eliminan duplicados
        nombres_de_la_pagina_sin_repetidos=[]
        precios_de_la_pagina_sin_repetidos=[]

        for vuelta_de_ciclo, elemento in enumerate(nombres_producto):
            if elemento not in nombres_de_la_pagina_sin_repetidos and elemento not in self.lista_de_nombres_no_repetidos:

                precios_de_la_pagina_sin_repetidos.append(precios_producto[vuelta_de_ciclo])
                nombres_de_la_pagina_sin_repetidos.append(elemento)
                
            else:
                print("*********ELEMENTO REPETIDO********* => "+elemento)
                
        
        self.lista_de_nombres_no_repetidos.extend(nombres_de_la_pagina_sin_repetidos)


        #Se ordenan dentro de un diccionario
        precios_de_la_pagina_actual=(dict(zip(nombres_de_la_pagina_sin_repetidos,precios_de_la_pagina_sin_repetidos)))
    

        #Se agrega el diccionario de la pagina en el archivo cvs
        with open(zapas,'a',newline='') as archivo:
            writer = csv.writer(archivo,delimiter=',')
            for nombre,precio in precios_de_la_pagina_actual.items():
                writer.writerow([nombre,precio])

        #Saltamos a la siguiente pagina si es que existe
        if siguiente_pagina:
            print("Siguiente pagina")
            yield response.follow(siguiente_pagina,callback=self.parse )

if __name__ == '__main__':

    procesar = CrawlerProcess()
    procesar.crawl(Spider)
    procesar.start()