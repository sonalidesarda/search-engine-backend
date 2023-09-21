#!/usr/bin/env python

import sys
import pysolr
import json
import os
import pickle

def productJSON(filename):
    product_set = set()
    docs = []
    with open(filename) as f:
        for line in f:
            product_details_dict = eval(line)
            filtered_dict = dict()
            keys_to_keep = ["asin", "title"]
            skip_iteration = False
            for key in keys_to_keep:
                if key not in product_details_dict:
                    skip_iteration = True
                    break
                filtered_dict[key] = product_details_dict[key]
            
            if "price" in product_details_dict and (type(product_details_dict["price"]) is not float or product_details_dict["price"] < 0.0):
                skip_iteration = True
            elif "price" in product_details_dict: 
                filtered_dict["price"] = product_details_dict["price"]
            
            if "description" in product_details_dict:
                filtered_dict["description"] = product_details_dict["description"]
    
            if skip_iteration:
                continue
            
            product_set.add(filtered_dict["asin"])
            docs.append(filtered_dict)

    pickle.dump(product_set, open("products_asin.txt", "wb"))
    return docs      
    
def reviewJSON(filename):
    docs = []
    products_asin = pickle.load( open( "products_asin.txt", "rb" ))
    with open(filename) as f:
        for line in f:
            product_details_dict = eval(line)
            filtered_dict = dict()
            keys_to_keep = ["asin", "summary","reviewText"]
            skip_iteration = False
            for key in keys_to_keep:
                if key not in product_details_dict:
                    skip_iteration = True
                    break
                filtered_dict[key] = product_details_dict[key]
            
            if "overall" in product_details_dict and type(product_details_dict["overall"]) is not float:
                skip_iteration = True
            elif "overall" in product_details_dict:
                filtered_dict["overall"] = product_details_dict["overall"]
            
            if filtered_dict["asin"] not in products_asin:
                skip_iteration = True
                
            if skip_iteration:
                continue
            
            docs.append(filtered_dict)
    return docs

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <product_data_file> <review_data_file>")
        return

    product_file = sys.argv[1]
    review_file = sys.argv[2]

    # Load product data and interact with Solr for products
    prod = productJSON(product_file)
    solr_products = pysolr.Solr('http://localhost:8983/solr/amazon_products')
    solr_products.add(prod, commit=True)

    # Load review data and interact with Solr for reviews
    rev = reviewJSON(review_file)
    solr_reviews = pysolr.Solr('http://localhost:8983/solr/amazon_reviews')
    solr_reviews.add(rev, commit=True)

if __name__ == "__main__":
    main()

