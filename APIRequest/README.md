# Python API Request Exercise

## From simple to advanced (hopefully) :D

## Exercise 1
Write a Python script that:

Sends a GET request to https://jsonapiplayground.reyesoft.com/v2/authors?page[size]=10
- Parses the JSON response
- Prints a list of dictionaries containing:
  -  Each author’s name in a “name” key
  -  The number of books they have written in a “book_count” key


## Exercise 2
Write a Python script that:
- Pages through the endpoint below
- Extends an author_list variable with each page of author data
- Stops paging when either :
  - There are no more authors
  - 15 pages have been processed
- Tells the user which condition above stopped the loop
- Prints the author_list variable
Starting endpoint: https://jsonapiplayground.reyesoft.com/v2/authors?page[size]=10&page[number]=1




## Exercise 3
Write a Python function that:
- Accepts an author_id parameter
- Sends a GET request to https://jsonapiplayground.reyesoft.com/v2/authors/{author_id}
- Parses the JSON response
- Returns a single dictionary containing:
  - The author name in a “name” key
  - The number of books they have written in a “book_count” key
- Raises a meaningful exception if the author_id is not found