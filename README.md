# Search Engine Backend

### Step 1. Download solr
1. Use [link](https://solr.apache.org/downloads.html) to download solr version 8.x.x..
2. Untar solr binary into project directory. Run following commands:
```
cd <project_dir>
mkdir solr
tar -xvf <solr_tgz_path> --strip-components=1 -C solr
```

### Step 2. Create python virtual environment and download dependencies
Run following commands:
```
cd <project_dir>
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3. Setup solr and load data
Run following commands to setup solr
```
cd <project_dir>
chmod +x setup_solr.sh
./setup_solr.sh
```

### Step 4. Start flask web server
Run following commands:
```
export FLASK_DEBUG=1
export FLASK_APP=reviewsite
flask run
```

### API Endpoint
Following is the API to get the search results:
```
GET /searchresults?query={query_string}&pageNumber={page_number_int}&pageSize={page_size_int}
```
