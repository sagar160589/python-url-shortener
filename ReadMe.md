This project aims at providing a short url like a tiny url/bit url for an original url.
Businesses can use this project to create short urls for their long urls and then give it the users.
Once user clicks on the short url, they would be redirected towards their original URL.

This project is based on
1. Encoding the original urls.
2. Storing the mapping of short and original urls in DB.
3. Using Redis to hold the URL ranges which would further map to the short codes to generate short urls.
4. Using Pandas to store the original url and short url in the file.
5. It also contains a number_of_clicks column to hold the no_of_clicks done by the user on the short url which further redirects to the original url.

Further enhancement done:
1. Added Elastic Search which is helpful in searching any details w.r.t to URL in a superfast way.
2. Used Kibana to visualize the data inserted into Elastic Search.
3. Elastic search is installed locally - Download it from **https://www.elastic.co/downloads/elasticsearch** and then later install it for Python using pip install elasticsearch.
   Run the ES locally using **./elasticsearch -E xpack.security.enabled=false**  as we don't need ssl enable on localhost. Create an instance of ES inside main.py appcontext and test if it runs or not as below
   es = Elasticsearch([{'host':'localhost','port':9200, 'scheme':'http'}])
   **if es.ping():  
       print("Connected")
   else:
       print("Not connected")**
4. Data that is inserted into Elastic Search is :
    a. Once the short url is created the request details like the browser agent etc. then the short url and the date when it is created is inserted in an index named
       'short_urls' inside ES.(Elastic Search)
    b. When any user hits the short url to redirect to its original url, the details like the browser agent etc. then the short url, date when it was created and the number of clicks
       is inserted into another index named 'short_urls_click' inside ES. (Elastic Search)
5. Download Kibana on local from - **https://www.elastic.co/downloads/kibana** and run the kibana.bat for windows inside the bin folder.
6. Kibana runs on **http://localhost:5601/** . Use **https://www.elastic.co/guide/en/kibana/current/data-views.html** which will guide to create a data view inside Kibana and then you will be able to
   visualize the Elastic search data inside it.
