import requests
from importlib import reload

def review_search(kw, start=0, pageSize = 10, score_facet=None):    
    reviews = do_query(review_query_dictionary(kw, start=start, pageSize = pageSize, score_facet=score_facet), collection="amazon_reviews")
    return reviews

def review_query_dictionary(kw="", start=0, pageSize = 5, score_facet=None):
    qvalue = "(summary:" + "(" + " OR ".join(kw.split()) + ") OR reviewText:"+ "(" + " OR ".join(kw.split()) + "))"
    if score_facet and score_facet <= 5 and score_facet >= 1:
        qvalue += f" AND overall:{score_facet}"
    return {"q": qvalue, "start": start, "rows":pageSize, "facet.field": "overall", "facet.sort":"index"}


def do_query(params, port="8983", collection="reviews"):
    
    param_arg = "&".join(list(map(lambda p: f"{p[0]}={p[1]}", list(params.items()))))
    query_string = f"http://localhost:{port}/solr/{collection}/select"
    param_arg += "&facet=true"
    print("param_arg ",param_arg)
    
    r = requests.get(query_string, param_arg)
    if (r.status_code == 200):
        return r.json()
    else:
        raise Exception(f"Request Error: {r.status_code}")

def product_search(asin):
    products = do_query(product_query_dictionary(asin), collection="amazon_products")

    if products['response']['numFound'] > 1:
        raise Exception(f"Multiple products found for asin: {asin}")
    elif products['response']['numFound'] == 0:
        return

    return products['response']['docs'][0]


def id_search(id):
    return do_query(id_query_dictionary(id), collection="reviews")

def id_query_dictionary(id):
    return {"q": f"id:{id}"}

def product_query_dictionary(kw=""):
    return {"q": f"asin:{kw}"}

