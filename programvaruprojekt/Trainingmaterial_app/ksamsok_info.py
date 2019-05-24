import math
import random
import requests
import abc
import itertools

"""[summary]
This file handles the logic for getting picture information from K-samsok.
Info such as item id,service organization,thumbnail,item type and kringla link
Author: Daniel Persson 2019-05-21
Sources: Some code is taken/based on Abbe98 code on github link:
https://gist.github.com/Abbe98/882a374350d20b980190c3148f787f5a
"""

# (This comment is from Abbe98) K-samsök supports JSON if given the following Accept header
headers = {
    'Accept': 'application/json'
}

def random_ksamsok_pics(num_of_req,item_type,service_organizations):
    """[summary]
    This method takes all our created functions and outputs a generator with dictonaries from random startrecords.
    The dictonaries contains the following info:item id,service organization,thumbnail,item type and kringla link.
    Args:
        num_of_req ([INT]): [This is how many requests we want to do. This decides how many random pictures we want]
        item_type ([STR]): [This is what type of item we want from request]
        service_organization ([STR]): [The org we want pictures from]
    """
    #Splits our requests in to a number in two and rounds it upwards, this to get the correct amount of images.
    num_of_req = math.ceil(num_of_req/2)
    list_org = service_org_list(service_organizations)
    result_final = []
    for org in list_org:
        #We request two from the query because one does not return anything
        req_url,query = concat_url(2,item_type,org)
        total_results = get_totalt_result(req_url)
        result = loop_throught_req(req_url,num_of_req,total_results,"random_pics")
        result_final = itertools.chain(result_final,result)
    result_final = add_kringla_link(result_final,query)
    return result_final

def ksamsok_pics(num_of_pics,num_of_req,item_type,service_organizations):
    """[summary]
    This method takes all our created functions and outputs a generator with dictonaries from one to number of pictures as startrecords.
    The dictonaries contains the following info:item id,service organization,thumbnail,item type and kringla link.
    Args:
        num_of_pics ([INT]): [This is how many pictures we want from K-samsok. Max is 500 pictures due to API]
        item_type ([STR]): [This is what type of item we want from request]
        service_organization ([STR]): [The org we want pictures from]
    """
    list_org = service_org_list(service_organizations)
    result_final = []
    num_of_pics = default_to_500_pics(num_of_pics)
    for org in list_org:
        req_url,query = concat_url(num_of_pics,item_type,org)
        total_results = get_totalt_result(req_url)
        result = loop_throught_req(req_url,num_of_req,total_results,"pics")
        result_final = itertools.chain(result_final,result)
    result_final = add_kringla_link(result_final,query)
    return result_final

def default_to_500_pics(num_of_pics):
    """[summary]
    This defaults our user input always to 500 pictures
    Args:
        num_of_pics ([INT]): [How many pictures wanted]
    """
    if(num_of_pics > 500):
        return 500
    else:
        return num_of_pics

def service_org_list(service_organizations):
    """[summary]
    Takes all our inputed orgs and splits them into a list
    Args:
        service_organization ([STR]): [The org we want pictures from]
    """
    if(service_organizations == "all"):
        service_organizations ='s-vlm,kbg,enk,smvk-mm,shm,hallwylska museet,aero,vgm,osmu,smvk-om,smm-mm,bhm,socken,lsh,vm,nomu,jm,Kortnamn,arkm,blm,skoklosters slott,pm,s-tek,s-hm,rsms,shfa,jlm,slm,mili,imvg,heo,smm-sm,mm,s-fv,tum,s-om,soc,livrustkammaren,smm-vm,smvk-em,kulturen,jfl,vax,gnm,hem,vbg,tes,upmu,smha,gfm,dramawebben,smvk-vkm,sm,sk,dfh,litografiska,s-xlm,raä,arme,ajtte,wws,ablm,fmb,s-fbm,gsm,s-olm'
        return service_organizations.split(',')
    else:
        return service_organizations.split(',')

def add_kringla_link(result,ksamsok_query):
    """[summary]
    Methods creates and inputs the kringla link in to each dictonary in the generator
    Args:
        result ([GENERATOR]): [All our dictonaries in a generator]
        ksamsok_query ([type]): [Our query we searched for]
    """
    kringlaLink = "http://www.kringla.nu/kringla/objekt?referens="
    for item in result:
        ref = item["itemId"]
        full_link = kringlaLink+ref.replace("http://kulturarvsdata.se/","")
        item["kringlaLink"] = full_link
        yield item

def get_totalt_result(req_url):
    """[summary]
    This gets all the results in INT from the specified query
    Args:
        req_url ([STR]): [The request query that decides the data]
    """
    r = requests.get(req_url, headers=headers)
    json = r.json()
    return json['result']['totalHits']


def concat_url(num_of_pics,item_type,org):
    """[summary]
    This concats our full API url
    Args:
        num_of_pics ([INT]): [How many pictures wanted, the hitsPerPage in our case]
        item_type ([STR]): [This is what type of item we want from request]
        org ([STR]): [The org we want pictures from]
    """
    endpoint = 'http://www.kulturarvsdata.se/ksamsok/api'
    fields = 'serviceOrganization,thumbnail,itemType'
    endpoint_fields = F'?&x-api=test&method=search&hitsPerPage={num_of_pics}&recordSchema=xml'
    
    #All the "OR NOT" in the query is photos that resembles objects something we dont want when item_type is photo
    query = F'thumbnailExists="j" AND itemType="{item_type}" AND serviceOrganization="{org}" OR NOT itemSpecification="Dokumentationsbild" OR NOT itemSpecification="ID-bild" OR NOT itemSpecification="Placeringsbild" OR NOT itemSpecification="Presentationsbild" OR NOT itemName="föremålsbild"'
    req_url = F'{endpoint}{endpoint_fields}&query={query}&fields={fields}&startRecord='
    return req_url,query

def loop_throught_req(req_url,required_requests,total_results,kind_startrecord):
    """[summary]
    This method loop throught the results we got from K-samsok and puts it in a dict.
    It returns the dict so we cant loop throught the results and get out the data.
    Args:
        req_url ([STR]): [Full url of the query wanted]
        required_requests ([INT]): [Number of requested wanted that need to run]
        total_results ([INT]): [The amount of requests from the full query]
        kind_startrecord ([INT]): [Start record is were our loop starts gaterhing from the total result in K-samsok]
    """
    count = 0
    #If collections is empty print and skip rest
    if total_results <= 1:
        print("Error: Collection is empty\n")
    else:
        #Makes an array of unique random numbers
        try:
            startrecord_unique = random.sample(range(0,total_results), required_requests)
        except:
            print("Collection less than requested download what i can from collection")
            startrecord_unique = random.sample(range(0,total_results), total_results)
        while len(startrecord_unique) != count:
            #Gets our randomed startrecord
            if kind_startrecord == "random_pics":
                startrecord = startrecord_unique[count]
            else:
                startrecord = count * 500

            count += 1
            r = requests.get(req_url + str(startrecord), headers=headers)
            response_data = r.json()
            #Give sometimes the following error "TypeError: string indices must be integers"
            try:
                for record in response_data['result']['records']['record']:
                    #(This comment is from Abbe98) sometimes there are empty records and those has no fields :-(
                    if not len(record) == 2:
                        continue
                    item_to_yield = {}
                    #(This comment is from Abbe98) some fields can appear multiply times
                    #(This comment is from Abbe98) therefor we need to merge those to lists if needed
                    for field in record['field']:
                        #(This comment is from Abbe98) if the field is already a list 
                        if isinstance(item_to_yield.get(field['name'], False), list):
                            item_to_yield[field['name']].append(field['content'])
                        #(This comment is from Abbe98) if it's not yet a list but we found the same field name/key again
                        elif item_to_yield.get(field['name'], False):
                            item_to_yield[field['name']] = list([item_to_yield[field['name']], field['content']])
                        #(This comment is from Abbe98) default to just a regular value
                        else:
                            item_to_yield[field['name']] = field['content']
                    yield item_to_yield
            except TypeError:
                print("Error: Incorrect type, download what I can from current query\n")