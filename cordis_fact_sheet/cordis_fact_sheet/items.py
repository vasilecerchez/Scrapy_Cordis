import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join, Identity
from w3lib.html import remove_tags
from w3lib.html import replace_escape_chars # serve eliminare \n\t all'interno della stringa project_id

def pulizia_partecipanti_in(dizz):
    new_dizz = {key: value.strip() for key, value in dizz.items()}
    return new_dizz

def pulizia_id(valore):
    valore=valore.replace('Grant agreement ID:','')
    return valore


class CordisFactSheetItem(scrapy.Item):
    titolo=scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
            # metto take first perchè altrimenti mette tutto in una lista, una lista di un solo elemento
    project_link=scrapy.Field(input_processor=Identity(),output_processor=TakeFirst())

    project_description_title=scrapy.Field(input_processor=MapCompose(remove_tags), output_processor=TakeFirst()) 

    description=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip), output_processor=TakeFirst())


    project_objective=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=Join(" "))
    fields_science=scrapy.Field()
    keyword_project=scrapy.Field(input_processor=MapCompose(remove_tags))
    programme_s=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    programme_s_links=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    topic_s=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    topic_s_links=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    call_forproposal=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    call_forproposal_links=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    funding_scheme=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    funding_scheme_links=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    coordinator=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=TakeFirst())
    coordinator_adress=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=Join(" "))
    net_eu_contribution=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=TakeFirst())
    other_funding=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=TakeFirst())
    region=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=Join(" "))
    activity_type=scrapy.Field(input_processor=MapCompose(remove_tags),output_processor=TakeFirst())
    acronym=scrapy.Field(input_processor=MapCompose(remove_tags),output_processor=TakeFirst())
    project_id=scrapy.Field(input_processor=MapCompose(remove_tags,replace_escape_chars,pulizia_id),output_processor=TakeFirst())
    doi=scrapy.Field(input_processor=MapCompose(remove_tags),output_processor=TakeFirst())
    sub_call=scrapy.Field()


    start_date=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=TakeFirst())
    end_date=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=TakeFirst())
    progress=scrapy.Field(input_processor=MapCompose(remove_tags),output_processor=TakeFirst())
    funded_under=scrapy.Field(input_processor=MapCompose(remove_tags),output_processor=TakeFirst())
    overall_budget=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip,replace_escape_chars),output_processor=TakeFirst())
    eu_contribution=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip,replace_escape_chars),output_processor=TakeFirst())
    coordinated_by=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=Join())
    coordinated_by_nationality=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip),output_processor=TakeFirst())

    links_coordinator=scrapy.Field(output_processor=TakeFirst()) # da vedere se si può utilizzare solo output_processo senza input processor
    # non da errore = buon segno anche se forse non si può utilizzare 
    

    
    #lista_partecip=scrapy.Field()
    #nome_participante=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    #nazione_partecipante=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))

    patecipanti=scrapy.Field(input_processor=MapCompose(pulizia_partecipanti_in))
    links_part=scrapy.Field()

    partners=scrapy.Field(input_processor=MapCompose(pulizia_partecipanti_in))
    links_partner=scrapy.Field()






    ## secondo modo salvare i partecipanti
    """    
    nome_participante=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    nazione_partecipante=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    net_eu_contribution=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    other_funding=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    address_part=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    region_part=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    activity_type_part=scrapy.Field(input_processor=MapCompose(remove_tags,str.strip))
    links_part=scrapy.Field()"""








