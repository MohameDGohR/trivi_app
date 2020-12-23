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

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the  
  value is the tyoe of category
  
- Request Arguments: None
- Returns: categories key with value  object dictionary of key and value 
  pairs which key is the 
  category id and value is     
  categoy type and return success of operation if it sucessed return sucess key  with 
  value true if else returnsuccess key with value false . 
  {
    'categories': {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"}
    'success':True
  }


POST '/questions'
-add new question or fetch questions objects 
 that match search words
-Request Arguments : propertise of  
 question   object such as question,
 answer , deficulty , category   or searchterm words that  used in search for specific question  
- returns  in case of  search 
  {
    "currentCategory": {
        "4": "sports"
    },
    "questions": [
        {
            "answer": "FC",
            "category": "4",
            "difficulty": 3,
            "id": 13,
            "question": "what is the best 
              team you like"
        }
    ],
    "success": true,
    "totalQuestions": 1
  }
  or return in add case 
  {
    "created": 17,
    "success": true
  }


GET '/categories/2/questions'
  -fetch or get all question whichbelong to   speciified category
  -Request Arguments : id  of  category 
  -Returns 
    {
    "currentCategory": {
        "2": "science"
    },
    "questions": [
        {
            "answer": "H2O",
            "category": "2",
            "difficulty": 2,
            "id": 12,
            "question": "what the chemical 
              name of water?"
        }
    ],
    "totalQuestions": 1
   }
 
POST '/quizzes'
  - fetch questions  for user from api  which belong to specific category  to
    check the user knowledge  in specific category.
  - Request Arguments :  
      previous_questions -> object of question had been sent in specific category 
      quize_category -> "quiz_category":{"id":3, "type":"arts"} 
  - returns :
      {
       "question": {
        "answer": "what is the best team you like",
        "category": "3",
        "difficulty": 3,
        "id": 17,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
              },
        "success": true
    }
GET  '/questions'
  - fetch / get all questions and return in chuncks  each chunck consists of 
    10 questions .
  - Required Arguments :send  Page number or non .
  - returns :
       {
        "categories": {
         "1": "historic",
         "2": "science",
         "3": "arts",
         "4": "sports"
       },
        "currentCategory": "all",
        "questions": [
          {
            "answer": "H",
            "category": O"2",
            "difficulty": 2,
            "id": 12,
            "question": "what the chemical name of water?"
          },
          {
            "answer": "FC",
            "category": "4",
            "difficulty": 3,
            "id": 13,
            "question": "what is the best team you like"
          },
        
          {
            "answer": "Justice League Dark ",
            "category": "3",
            "difficulty": 4,
            "id": 16,
            "question": " what had the best film you seen ? "
          },
          {
            "answer": "what is the best team you like",
            "category": "3",
            "difficulty": 3,
            "id": 17,
            "question": "What movie earned Tom Hanks his third straight Oscar 
             nomination, in 1996?"
          }
          ],
          "success": true,
          "totalQuestions": 5
        } 
DELETE /questions/5'
  - delete question from database  which its id  is 5 
  - Required Arguments : id of question .
  - returns :
      {
       "id": 12,
       "success": true
      }


```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```