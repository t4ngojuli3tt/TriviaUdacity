# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...


All endpoint returns contains keys success and status_code with boolean and int values respectively  (e.g.   {"status_code": 200, "success": true, ...} )

There are 3 error handlers (404,409, 422), all returns json with three key value paris and error code
e.g jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404


GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
- Errors:
    - 404 -  if there is no category


GET '/questions'
- Fetches a list dictionaries of questios in which the keys are names of questions class atributes and the value is the corresponding value of the atribute for a gives question. Fetches also all categories in the same format as GET '/categoires'/
- Request Arguments:  
    -category(int) - optional, None by default -  coresponding to id of category for which we want to get questions
    -page(int) - opitional, 1 by default - page argument for pagination
- Returns: An object with a keys:
    - categories - same as for GET '/categoires'/
    - current_category - name of category for which questions were fatched
        e.g. "current_category": "Science" 
    - questions - list of dictionaries containig question details
        e.g. "questions": [
        {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, ...]
    - total_questions - number of all questions
        e.g. "total_questions": 19
- Errors:
    - 404 - if the idea of category is incorrect or there is no question in selected category 


DELETE '/questions/<int:question_id>'
- Delete question from the database
- Request Arguments:  question_id (int) - id of the question to be deleted 
- Returns: An object with a keys:
    - deleted - id of question that was deleted 
        e.g. "deleted": 1
    - questions and total_questions - same as in GET '/questions'
- Errors:
    - 404 - if question to be deleted wasn't found in the database


POST '/questions'
- Post new question to the database
- Request Arguments:  json object with question, answer, category and difficulty fildes
- Returns: An object with a keys:
    - question - value of this key is a string containg posted question
        e.g. "question": "How are you?"
- Errors:
    - 422 - if body does not contains requiered data
    - 409 - if question is already in the database


POST '/questions/search'
- Fetches a list dictionaries of questions same as GET '\questions', but only with questions which contains search term
- Request Arguments:  
    -searchTerm(string)  -  
- Returns: Similar object to the one return by GET '\questions' by this one does not contain categories key, and the list of question is restricted to the ones which match search term. 


GET '/categories/<int:category_id>/questions'
- Fetches a list dictionaries of questios for a given category.
- Request Arguments:  
    -category(int) - optional, None by default -  coresponding to id of category for which we want to get questions
    -page(int) - opitional, 1 by default - page argument for pagination
- Returns: An object with a keys:
    - questions - same as GET '/questions'
- Errors:
    - 404 - if category_id does not corespond to any category id in the database 

POST '/play'
- Fetches a random question from a given category.
- Request Arguments:  
    - quiz_category (dict) - optional, None by default -  dictionary with two keys id and type
    -previous_questions(list of int) - by default empyt list - list of question to be exlcude from this request
- Returns: An object with a keys:
    - question - dictionary with question, answer, category and difficulty keys
        e.g. "question":
        {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
- Errors:
    - 404 - if category_id does not corespond to any category id in the database 
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```