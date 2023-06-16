This project aims at providing a short url like a tiny url/bit url for an original url.
Businesses can use this project to create short urls for their long urls and then give it the users.
Once user clicks on the short url, they would be redirected towards their original URL.

This project is based on
1. Encoding the original urls.
2. Storing the mapping of short and original urls in DB.
3. Using Redis to hold the URL ranges which would further map to the short codes to generate short urls.
4. Using Pandas to store the original url and short url in the file.
5. It also contains a number_of_clicks column to hold the no_of_clicks done by the user on the short url which further redirects to the original url.