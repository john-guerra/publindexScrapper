import urlparse

import scrapy


URL = "http://publindex.colciencias.gov.co:8084/publindex/busqueda/buscar.do?tpo_busqueda=REV&txt_nme_titulo=&nro_issn=&txt_titulo_articulo=&txt_autor=&txt_palabra_clave=&maxRows=100&Toda_Revista_Data_tr_=true&Toda_Revista_Data_p_=%d&Toda_Revista_Data_mr_=100"

class PublindexSpider(scrapy.Spider):
  name = 'Publindex'
  start_urls = [URL%(1)]

  rate = 1

  def __init__(self):
    scrapy.Spider.__init__(self)
    self.download_delay = 1/float(self.rate)

  def parse(self, response):


    # Is there next page?
    if response.css("#Toda_Revista_Data .toolbar table tr td:nth-child(3) img::attr(src)").extract()[0] != "/publindex/images/table/nextPageDisabled.gif":
      #load next page

      next_url = URL%(int(urlparse.parse_qs(response.url)["Toda_Revista_Data_p_"][0])+1)
      print "Requesting next page", int(urlparse.parse_qs(response.url)["Toda_Revista_Data_p_"][0])+1, next_url
      # if (int(urlparse.parse_qs(response.url)["Toda_Revista_Data_p_"][0])+1 ) <= 2:
      yield scrapy.Request(response.urljoin(next_url), self.parse)

    # yield self.parse_magazines(response)
    print "**Parse magazine"
    for magazine in response.css('#Toda_Revista_Data tbody:nth-child(2) tr'):
      yield {"year": magazine.css("td:nth-child(2)::text").extract(),
        "issn":magazine.css("td:nth-child(3)::text").extract(),
        "name":magazine.css("td:nth-child(4)::text").extract()
      }

    # yield scrapy.Request(response.url, self.parse_magazines)


  # def parse_magazines(self, response):
  #   print "**Parse magazine"
  #   for magazine in response.css('#Toda_Revista_Data tbody:nth-child(2) tr'):
  #     yield {"year": magazine.css("td:nth-child(2)::text").extract(),
  #       "issn":magazine.css("td:nth-child(3)::text").extract(),
  #       "name":magazine.css("td:nth-child(4)::text").extract()
  #     }

