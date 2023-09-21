
Step 1 - Go to solr directory and Start solr
bin/solr start

Step 2 - Create the products and reviews collections using the configuration directories. 

Syntax- bin/solr create_collection -c your_collection_name -d /path/to/config

Open terminal and go to solr directory and run following command 
solr create_collection -c products -d products
solr create_collection -c reviews -d reviews

Example - 
bin/solr create_core -c amazon_products -d /Users/sonalidesarda/Documents/CPSC5340_InformationRetrieval/CPSC5340_Project_Work/Assignment2/products 

bin/solr create_core -c amazon_reviews -d /Users/sonalidesarda/Documents/CPSC5340_InformationRetrieval/CPSC5340_Project_Work/Assignment2/reviews 


Step 3 - Run python script to load data in solr collection-
python LoadDataToSolr.py test-products.txt test-reviews.txt 


Step 4 - Start Flask, pointing it at your project directory. 
Windows - 
set FLASK_APP=reviewsite
set FLASK_DEBUG=1
flask run

Bash -
export FLASK_APP=reviewsite
export FLASK_DEBUG=1
flask run