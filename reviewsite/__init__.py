import os
from flask import request, Flask, jsonify, render_template,redirect, url_for
import reviewsite.solrinterface as solr
from reviewsite.forms import ReviewSearchForm
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)  # Add this line to enable CORS for your app

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    ###################################
    ## Application code begins
    @app.route('/', methods=['GET'])
    def index():
        review_count = solr.do_query({"q": "*:*", "rows": 0}, collection="amazon_reviews").get("response", dict()).get(
            "numFound", -1)
        product_count = solr.do_query({"q": "*:*", "rows": 0}, collection="amazon_products").get("response", dict()).get(
            "numFound", -1)
        return render_template('index.html', reviewcount=review_count, productcount=product_count)

    
    @app.route('/search', methods=['GET', 'POST'])
    def searchForm():
        form = ReviewSearchForm()
        if request.method == 'GET':
            return render_template('reviewsearch.html', form=form)
        elif not form.validate():
            return render_template('reviewsearch.html', form=form)
        else:
            return redirect(url_for('searchResults', query=form.keywords.data, page_number=0))

    @app.route('/searchresults', methods=['GET'])
    def searchResults():
        query = request.args.get('query')
        pageSize = request.args.get('pageSize', type=int)
        pageNumber = request.args.get('pageNumber', type=int)
        score_facet = request.args.get('score', type=int)
        
        start = 0
        if pageSize and pageNumber:
            start = pageNumber * pageSize

        reviews = solr.review_search(query, start, pageSize, score_facet)

        review_search_result = list()
        end = None
        next_url = None
        prev_url = None
        if reviews['response']['numFound'] == 0:
            review_search_result = None
            count = 0
        else:
            # Search Product for given review.
            for review in reviews['response']['docs']:
                product = solr.product_search(review['asin'])
                review_search_entry = dict()
                review_search_entry['reviewSummary'] = review['summary']
                review_search_entry['productName'] = product['title'] if product else "PRODUCT_NOT_FOUND"
                review_search_entry['asin'] = review['asin']
                review_search_entry['reviewScore'] = review['overall']
                review_search_entry['id'] = review['id']

                review_search_result.append(review_search_entry)

        count=reviews['response']['numFound']

        # Create a response dictionary
        response_data = {
            'review_search_result': review_search_result,
            'end': end,
            'next_url': next_url,
            'prev_url': prev_url,
            'count':count,
            'pageSize':pageSize,
            'facet':reviews['facet_counts']
        }
        # Return the response as JSON
        return jsonify(response_data)
    
    @app.route('/idlookup/<reviewid>', methods=['GET'])
    def idLookup(reviewid):
        # idDetail = solr.test_id_search('2c7cf845-cb08-4afe-bbba-2f46b467e99c')
        idDetail = solr.id_search(reviewid)
        doc = idDetail['response']['docs'][0]
        id = doc['id']
        product = solr.product_search(idDetail['response']['docs'][0]['asin'])
        doc['productName'] = product['title'] if product else "PRODUCT_NOT_FOUND"
        return render_template('reviewdetail.html', id=id, doc=doc)

    @app.route('/asinlookup/<asin>', methods=['GET'])
    def asinLookup(asin):
        product = solr.product_search(asin)
        if 'price' in product:
            product['price'] = "${:,.2f}".format(product['price'])

        return render_template("productdetail.html", asin=asin, product=product)

    ## Application code ends
    ##############################
    return app
