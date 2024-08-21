# Project scope
Using the language that you feel most proficient in, create a web crawler using scraping techniques to extract the first 30 entries from https://news.ycombinator.com/. You'll only care about the number, the title, the points, and the number of comments for each entry.

From there, we want it to be able to perform a couple of filtering operations:

Filter all previous entries with more than five words in the title ordered by the number of comments first.

Filter all previous entries with less than or equal to five words in the title ordered by points.

When counting words, consider only the spaced words and exclude any symbols. For instance, the phrase “This is - a self-explained example” should be counted as having 5 words.

The solution should be designed for a web environment. The primary functionality and interaction should be accessible through a web browser.

# Installation 
- The project has been developed using Docker Desktop but it should work using Docker itself

- Download the repository and execute the following:

  -  Build the Docker image:
```docker-compose build```

  - Start the containers:
```docker-compose up```

- Access the Application: 
  - Open your browser and go to http://localhost:8080 to check the application.

# Brief explanation
### Dockerfile and docker-compose.yml
They are responsible of creating the project by declaring the requirements and other configurations.
### scripts/webCrawler.py
It is the main piece of code and it contains al the functions responsible of the data retrieval and filtering. I focused not only on creating the specific filters required by the project scope, but also adding some flexibility to them by using parameters. 

The script uses the BeautifulSoup library for HTML parsing and requests for HTTP requests, ensuring robust and flexible web scraping. Another solid option might have been using Selenium but taking in mind the project scope there was no need to use it. 
### controller/runWebCrawler.php
This controller acts as the backend controller, handling the interaction between the frontend and the Python script. It is in charge of executing the script and receiving all the parameters needed.
### index.html
This file displays the web page and sends the different parameters to the controller through JS. It is a really simple design but since there were no specifications about it I aimed for simplicity and functionality.

 I decided to implement only the required filters by the project scope but this file could be easily modified to use some class of form (maybe using a few selects) and apply custom filters by the user.

``` More information about the code can be found in comments throughout the different files```

# Usage
- Open your browser and go to http://localhost:8080
- Once here you can click on any of the buttons to apply different filters to the scrapped content


![Usage](src/images/usage.JPG?raw=true "Example")

