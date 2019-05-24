import math
import requests

# (This comment is from Abbe98) K-samsök supports JSON if given the following Accept header
headers = {
    'Accept': 'application/json'
}

def ksamsok_info(item_type,service_organization):
    """[summary]
    This method takes all our created functions and outputs a generator with dictonaries from one to number of pictures as startrecords.
    The dictonaries contains the following info:item id,service organization,thumbnail,item type and kringla link.
    Args:
        item_type ([STR]): [This is what type of item we want from request]
        service_organization ([STR]): [The org we want pictures from]
    """
    req_url,query = concat_url(500,item_type,service_organization)
    total_results = get_totalt_result(req_url)
    required_n_requests = math.ceil(total_results / 500)
    result = loop_throught_req(req_url,required_n_requests,total_results)
    final_result = add_kringla_link(result,query)
    return final_result

def add_kringla_link(result,ksamsok_query):
    """[summary]
    Methods creates and inputs the kringla link in to each dictonary in the generator
    Args:
        result ([GENERATOR]): [All our dictonaries in a generator]
        ksamsok_query ([STR]): [Our query we searched for]
    """
    ksamsok_query = ksamsok_query.replace(" AND ","&")
    ksamsok_query = ksamsok_query.replace('"',"")
    kringlaLink = F"http://www.kringla.nu/kringla/objekt?referens="
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

def loop_throught_req(req_url,required_requests,total_results):
    """[summary]
    This method loop throught the results we got from K-samsok and puts it in a dict.
    It returns the dict so we cant loop throught the results and get out the data.
    Args:
        req_url ([STR]): [Full url of the query wanted]
        required_requests ([INT]): [Number of requested wanted that need to run]
        total_results ([INT]): [The amount of requests from the full query]
    """
    count = 0
    #If collections is empty print and skip rest
    if total_results <= 1:
        print("Error: Collection is empty\n")
    else:
        while required_requests >= count:
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

