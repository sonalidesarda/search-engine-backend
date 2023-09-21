#!/bin/bash

# Start Solr
solr/bin/solr start

# Create cores
solr/bin/solr create_core -c amazon_products -d products
solr/bin/solr create_core -c amazon_reviews -d reviews
python LoadDataToSolr.py test-products.txt test-reviews.txt
