import scrapy


#nome progetto.items import il nome della class nella items.py
from cordis_fact_sheet.items import CordisFactSheetItem

from scrapy.loader import ItemLoader

from scrapy.http import request # serve  per il file csv
import pandas as pd # serve  per il file csv
# import re


class SpiderFactSheetSpider(scrapy.Spider):
    name = "spider_fact_sheet"
    #start_urls = ["https://cordis.europa.eu/projects/en"]
    allowed_domains = ["cordis.europa.eu"]

    def start_requests(self):
        #df = pd.read_csv('C:/Users/vasil/Desktop/3_incontro/cordis_incontro3/cordis_incontro3/spiders/list_links.csv')# deve essere nella stessa carella dello spider
        #urls = df['links']
        df=pd.read_excel('C:/Users/vasil/Desktop/finale_scraping/cordis_fact_sheet/cordis_fact_sheet/spiders/links.xlsx')
        urls=df['CORDIS Link']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    ###############################################################à
    
    def parse(self, response):
        item=ItemLoader(item=CordisFactSheetItem(), response=response, selector=response)#response=response,
        
        item.add_xpath("titolo","//h1/text()")
        item.add_value("project_link", response.url)
        #item.add_xpath("project_description_title",'//div[@class="c-factsheet__section"]//h3/text()')
        if response.xpath('//div[@class="c-factsheet__section"]//h2[contains(text(),"Project description")]/../h3/text()'):
            item.add_xpath("project_description_title",'//div[@class="c-factsheet__section"]//h2[contains(text(),"Project description")]/../h3/text()')
            item.add_xpath("description",'//h2[contains(text(),"Project description")]/../p[contains(@class,"text")]/text()')
        else:
            item.add_value("project_description_title","NO_project_description_title")
            item.add_value("description","no_description")

        item.add_xpath("project_objective",'//h2[contains(text(),"Objective")]/../p//text()')
        
        box_fields_science=response.xpath('//ul[@aria-labelledby="fieldofscience2"]/li')

        for field in box_fields_science:
            single_field_list=[]
            single_field_list.append(field.xpath('./span/a/text()').getall())
            item.add_value('fields_science', single_field_list)
        
        item.add_xpath("keyword_project",'//h3[@id="keywords"]/../ul/li/a/text()')
        item.add_xpath("programme_s",'//h3[@id="fundedunderprogrammes"]/../ul/li//a/text()')
        item.add_xpath("programme_s_links",'//h3[@id="fundedunderprogrammes"]/../ul/li//a/@href')
        item.add_xpath("topic_s",'//h3[@id="topicslist"]/../ul/li//a/text()')
        item.add_xpath("topic_s_links",'//h3[@id="topicslist"]/../ul/li//a/@href')
        item.add_xpath("call_forproposal",'//h3[contains(text(),"Call for proposal")]/../p/a/text()')
        item.add_xpath("call_forproposal_links",'//h3[contains(text(),"Call for proposal")]/../p/a/@href')

        if response.xpath('//h3[contains(text(),"Sub call")]/../p[span]/span/text()'):
            item.add_xpath("sub_call",'//h3[contains(text(),"Sub call")]/../p[span]/span/text()')
        else:
            item.add_value("sub_call","no_subcall")
            
        item.add_xpath("funding_scheme",'//h3[contains(text(),"Funding Scheme")]/..//a/text()')
        item.add_xpath("funding_scheme_links",'//h3[contains(text(),"Funding Scheme")]/..//a/@href')
        item.add_xpath("coordinator",'//h3[contains(text(),"Coordinator")]/..//div[@class="c-part-info__title"]/text()')
        item.add_xpath("coordinator_adress",'(//div[@class="c-part-info__content"])[1]/text()[normalize-space()]')
        item.add_xpath("net_eu_contribution",'(//div[@class="c-part-info__content "])[1]/text()')
        item.add_xpath("other_funding",'(//div[@class="c-part-info__content "])[2]/text()')
        try:
            item.add_xpath("region",'(//h3[contains(text(),"Coordinator")]/..//div[contains(text(),"Region")])[1]/following-sibling::div//text()[normalize-space()]')
        except:
            item.add_value("region",["non", "ha","region"])

        item.add_xpath("activity_type",'(//h3[contains(text(),"Coordinator")]/..//div[@class="c-part-info__content"])[2]//text()')
        item.add_xpath("acronym",'//div[@class="c-project-info__acronym"]/text()')
        item.add_xpath("project_id",'//div[@class="c-project-info__id"]/text()')
        item.add_xpath("doi",'(//span[@class="c-project-info__label"])[1]/../a/text()')

        
        item.add_xpath("start_date",'(//span[@class="c-project-info__label"])[2]/following-sibling::text()[1]')
        item.add_xpath("end_date",'(//span[@class="c-project-info__label"])[3]/following-sibling::text()[1]')
        item.add_xpath("progress",'(//div[@class="c-project-info__percentage"])/@style')
        item.add_xpath("funded_under",'//div[@class="c-project-info__fund"]//ul//li/text()')
        item.add_xpath("overall_budget",'//div[@class="c-project-info__overall"]/span/following-sibling::text()[1]')
        item.add_xpath("eu_contribution",'//div[@class="c-project-info__eu"]/span/following-sibling::text()[1]')
        item.add_xpath("coordinated_by",'//p[@class="coordinated coordinated-name"]/text()[1]')
        item.add_xpath("coordinated_by_nationality",'//p[@class="coordinated coordinated-name"]/span/following-sibling::text()[1]')
        
        box_links= response.xpath('(//div[contains(text(),"Links")]/following-sibling::div)[1]/*')# non metto perchè è il box .getall()
        links={} #non è il metodo più efficiente ed elegante, provare altre soluzioni anche se non so quali 
        for link in box_links:
            page_name=link.xpath(".//a/text()").get()
            page_name=page_name.strip()
            links[page_name] = link.xpath(".//a/@href").get()
            
        item.add_value('links_coordinator', links) 
        
        
        box_partecipanti=response.xpath('//h3[contains(text(),"Participants")]')
        if box_partecipanti: #is not None: # se esiste questo nodo allora fai le seguenti cose
            partecipanti=response.xpath('//h3[contains(text(),"Participants")]/..//div[@class="row org-list"]/div') #.getall() non serve perche voglio tutto per fare xpath dopo
            for partecipante in partecipanti:
                #item.selector = partecipante 
                # item.add_xpath("nome_participante",'.//div[@class="c-part-info__title"]//text()')
                # item.add_xpath("nazione_partecipante",'.//div[contains(@class, "country")]/span/following-sibling::text()[1]')
                nome_participante=partecipante.xpath('.//div[contains(@class,"c-part-info__title")]/text()[normalize-space()]').get()
                nazione_partecipante=partecipante.xpath('.//div[contains(@class, "country")]/span/following-sibling::text()[1]').get()
                net_eu_contribution=partecipante.xpath('.//div[contains(text(), "EU")]/following-sibling::div[1]/text()').get()

                if net_eu_contribution: #se la variabile sopra esiste allora sarò pari a se stessa, altrimenti sarà pari a 0
                    net_eu_contribution=net_eu_contribution 
                else:
                    net_eu_contribution="0"
                
                other_funding=partecipante.xpath('.//div[contains(text(), "funding")]/following-sibling::div[1]/text()').get()
                if other_funding:
                    other_funding=other_funding
                else:
                    other_funding='0'
                
                if partecipante.xpath('.//div[contains(text(), "SME")]/div/span/text()'):
                    sme_participante=partecipante.xpath('.//div[contains(text(), "SME")]/div/span/text()').get()
                else:
                    sme_participante="no_info_on_SME"





                
                address_part=partecipante.xpath('.//div[contains(text(), "Address")]/following-sibling::div[1]//text()[normalize-space()]').getall()
                address_part=list(map(str.strip, address_part)) # èuna lista
                address_part=" ".join(str(x) for x in address_part) # è una stringa

                if partecipante.xpath('.//div[contains(text(), "Region")]/following-sibling::div[1]//text()[normalize-space()]'):
                    region_part=partecipante.xpath('.//div[contains(text(), "Region")]/following-sibling::div[1]//text()[normalize-space()]').getall()
                    region_part=list(map(str.strip, region_part)) # èuna lista
                    region_part=" ".join(str(x) for x in region_part) # è una stringa
                else:
                    region_part="no_info_region"

                
                activity_type_part=partecipante.xpath('.//div[contains(text(), "Activity")]/following-sibling::div[1]//text()').get()

                links_part={}
                print(".......................@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                print("...........----------------------------####################")
                nome_participante=nome_participante.strip().replace('\n','').replace('\t','')
                links_part["nome_participante"]=nome_participante

                # partecipanti=response.xpath    ('//h3[contains(text(),"Participants")]/..//div[@class="row org-list"]/div')
                box_links_part=partecipante.xpath('.//div[contains(text(), "Links")]/following-sibling::div[1]/*')
                for link in box_links_part:
                    page_name=link.xpath(".//a/text()").get()
                    page_name=page_name.strip()
                    links_part[page_name] = link.xpath(".//a/@href").get()


                
                item.add_value("patecipanti",{'nome_participante':nome_participante,
                                "nazione_partecipante": nazione_partecipante,
                                "net_eu_contribution":net_eu_contribution,
                                "other_funding":other_funding,
                                "address_part":address_part,
                                "sme_participante":sme_participante,
                                "region_part":region_part,
                                "activity_type_part":activity_type_part  })
                
                item.add_value("links_part",links_part)
        else:
            """
            no_participanti="no participanti"
            no_links_part="no_links_part"

            item.add_value("patecipanti",{"no_participanti":no_participanti})
            item.add_value("links_part",{"no_links_part":no_links_part}) 
            """
            item.add_value("patecipanti",{'nome_participante':"no_nome_participante",
                                "nazione_partecipante": "no_nazione_partecipante",
                                "net_eu_contribution":"no_net_eu_contribution",
                                "other_funding":"no_other_funding",
                                "address_part":"no_address_part",
                                "sme_participante":"no_info_on_SME",
                                "region_part":"no_region_part",
                                "activity_type_part":"no_activity_type_part"})
            item.add_value("links_part",{"no_links_part":"no_links_part"})
            
        
        
        # Partners (2)
        box_partners=response.xpath('//h3[contains(text(),"Partners")]')
        if box_partners: #is not None: # se esiste questo nodo allora fai le seguenti cose
            partners=response.xpath('//h3[contains(text(),"Partners")] /..//div[@class="row org-list"]/div') #.getall() non serve perche voglio tutto per fare xpath dopo
            for partner in partners:
                nome_partner=partner.xpath('.//div[contains(@class,"c-part-info__title")]/text()[normalize-space()]').get()
                nazione_partner=partner.xpath('.//div[contains(@class, "country")]/span/following-sibling::text()[1]').get()
                net_eu_contribution_partner=partner.xpath('.//div[contains(text(), "EU")]/following-sibling::div[1]/text()').get()

                if net_eu_contribution_partner: #se la variabile sopra esiste allora sarò pari a se stessa, altrimenti sarà pari a 0
                    net_eu_contribution_partner=net_eu_contribution_partner 
                else:
                    net_eu_contribution_partner="0"
                
                other_funding_partner=partner.xpath('.//div[contains(text(), "funding")]/following-sibling::div[1]/text()').get()
                if other_funding_partner:
                    other_funding_partner=other_funding_partner
                else:
                    other_funding_partner='0'
                
                if partner.xpath('.//div[contains(text(), "SME")]/div/span/text()'):
                    sme_partner=partner.xpath('.//div[contains(text(), "SME")]/div/span/text()').get()
                else:
                    sme_partner="no_info_on_SME"
                

                
                address_partner=partner.xpath('.//div[contains(text(), "Address")]/following-sibling::div[1]//text()[normalize-space()]').getall()
                address_partner=list(map(str.strip, address_partner)) # èuna lista
                address_partner=" ".join(str(x) for x in address_partner) # è una stringa

                if partner.xpath('.//div[contains(text(), "Region")]/following-sibling::div[1]//text()[normalize-space()]'):
                    region_partner=partner.xpath('.//div[contains(text(), "Region")]/following-sibling::div[1]//text()[normalize-space()]').getall()
                    region_partner=list(map(str.strip, region_partner)) # èuna lista
                    region_partner=" ".join(str(x) for x in region_partner) # è una stringa
                else:
                    region_partner="no_info_region"

                
                activity_type_partner=partner.xpath('.//div[contains(text(), "Activity")]/following-sibling::div[1]//text()').get()

                links_partner={}
                nome_partner=nome_partner.strip().replace('\n','').replace('\t','')
                links_partner["nome_participante"]=nome_partner


                # partecipanti=response.xpath    ('//h3[contains(text(),"Participants")]/..//div[@class="row org-list"]/div')
                box_links_partner=partner.xpath('.//div[contains(text(), "Links")]/following-sibling::div[1]/*')
                for link in box_links_partner:
                    page_name_partner=link.xpath(".//a/text()").get()
                    page_name_partner=page_name_partner.strip()
                    links_partner[page_name_partner] = link.xpath(".//a/@href").get()
                
                item.add_value("partners",{'nome_partner':nome_partner,
                                "nazione_partner": nazione_partner,
                                "net_eu_contribution_partner":net_eu_contribution_partner,
                                "other_funding_partner":other_funding_partner,
                                "address_partner":address_partner,
                                "sme_partner":sme_partner,
                                "region_partner":region_partner,
                                "activity_type_partner":activity_type_partner  })
                
                item.add_value("links_partner",links_partner)

        else:
            item.add_value("partners",{'nome_partner':'no_nome_partner',
                                "nazione_partner": "no_nazione_partner",
                                "net_eu_contribution_partner":"no_net_eu_contribution_partner",
                                "other_funding_partner":"no_other_funding_partner",
                                "address_partner":"no_address_partner",
                                "sme_partner":"no_sme_partner",
                                "region_partner":"no_region_partner",
                                "activity_type_partner":"no_activity_type_partner"  })
                
            item.add_value("links_partner",{"no_links_partner":"no_links_partner"})
            
            
        
        yield item.load_item()

            

        
        
