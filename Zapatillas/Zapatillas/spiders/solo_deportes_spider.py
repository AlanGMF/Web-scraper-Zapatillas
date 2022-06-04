import scrapy
import time
from scrapy.crawler import CrawlerProcess
import csv

zapas= 'solodeportes.csv'

class sd_Spider(scrapy.Spider):
    name='sd'
    base = 'https://www.solodeportes.com.ar/hombre/calzado.html?p={}&_=16538649558{}'
    numero1=1
    numero2=16
    
    start_urls = [base.format("1","16")]
       

    def parse(self, response):

        #Selectores
        precio_producto = response.xpath('//li[@class="item product product-item"]//div//div//a//div//span[@class="old-price"]//span//span/@content').getall()
        nombre_producto = response.xpath('//li[@class="item product product-item"]//div//div//a/@title').getall()
        
        #se ordenan dentro de un diccionario
        dicionario_de_precios= dict(zip(nombre_producto,precio_producto))

        #Se escribe los resultados de la pagina en el archivo cvs
        with open(zapas,'a',newline='') as archivo:
            writer = csv.writer(archivo,delimiter=',')
            for nombre,precio in dicionario_de_precios.items():
                writer.writerow([nombre,precio])
        
        if self.numero1<=32:

            self.numero1+=1
            self.numero2+=1

            siguiente_pagina = self.base.format(str(self.numero1),str(self.numero2))

            print("***NEXT PAGE ***")
            time.sleep(3) #se espera unos segundos para evitar el baneo de ip departe del servidor
            yield response.follow(siguiente_pagina,callback=self.parse)

if __name__ == '__main__':

    procesar = CrawlerProcess()
    procesar.crawl(sd_Spider)
    procesar.start()