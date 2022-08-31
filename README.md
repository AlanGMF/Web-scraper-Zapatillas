# Web Scraper

Extrae el nombre y precio de zapatillas desde distintas páginas argentinas creando un archivo CSV por cada página.

![image](https://user-images.githubusercontent.com/96092963/171971531-c5f67412-0318-404b-b809-acf3a11ba529.png)


## Guia de uso

- 1  Clonar repositorio


- 2 Crear y abrir entorno virtual

    ###### ~Mac/unix
      
    `python3 -m venv venv`

    `source venv/bin/activate`
 
     ###### ~Windows
     
    `py -m venv venv`
    
    `venv\Scripts\activate`
      
- 3 instalar scrapy

      
      pip install scrapy
      
- 4 desde ~**\Web-scraper-Zapatillas\Zapatillas\Zapatillas\spiders** puede ejecutar el spider que desee

      py dexter.py
      py moov.py
      py solo_deportes_spider.py
      py stockcenter.py
      py tienda_dash_spider.py
