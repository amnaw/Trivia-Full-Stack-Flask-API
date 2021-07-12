### Full Stack API Final Project


### Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, and I (Amna) helped them since their API experience is limited and still needs to be built out. [Udacity's project repository](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter).

After my contributions to this project the application now can:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.
6. Use unittest to test flask API application for expected behavior.

### Getting started

#### Backend
The [./backend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/backend/README.md) directory contains  completed Flask and SQLAlchemy server. `__init__.py` define the endpoints and reference models.py for DB and SQLAlchemy setup.

#### 1. Installing Dependencies for the Backend
1. Python - Install the latest version of python following [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
2. Virtual Enviornment - To keeps your dependencies for each project separate and organaized. 
```
python -m virtualenv env
source env/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source env/Scripts/activate
```
3. PIP Dependencies - Install dependencies by naviging to the /backend directory and running:
```
pip install -r requirements.txt
```

#### 2. Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```
psql trivia < trivia.psql
```

#### 3. Running the server
Ensure you are working using your created virtual environment, then execute:
```
flask run --reload
```

#### Frontend

The [./frontend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. 
>View the [README within ./frontend for more details.](./frontend/README.md)

#### 1. Installing Dependencies for the Frontend
1. Installing Node and NPM - Install Node from https://nodejs.com/en/download.

2. Installing project dependencies - NPM Relies on the package.json file located in the frontend directory of this repository. After cloning, open your terminal and run:
```
npm install
```
#### 2. Running the frontend
to run the application's frontend execute:
```
npm start
```
then open http://localhost:3000 to view it in the browser. The page will reload if you make edits.



### Dependencies

1. [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

2. [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

3. [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.


### API Reference

#### 1. Endpoints
#### GET /questions
- Returns a list of all questions, total questions number, a list of the categories, the current category which is "All", and success value.
- Example: `curl http://127.0.0.1:5000/questions`
- Response body:
```
{
    "categories":
    {
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
    },
    "current_category":"All",
    "questions":
    [
        {"answer":"Tom Cruise","category":5,"difficulty":4,"id":4,"question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"},
        
        {"answer":"Maya Angelou","category":4,"difficulty":2,"id":5,"question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},
        
        {"answer":"Edward Scissorhands","category":5,"difficulty":3,"id":6,"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},
        
        {"answer":"Muhammad Ali","category":4,"difficulty":1,"id":9,"question":"What boxer's original name is Cassius Clay?"}
    ],
    "success":true,
    "total_questions":4
}
```

#### DELETE /questions/{question_id}
- Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value.
- Example: `curl -X DELETE http://127.0.0.1:5000/questions/11?page=2`
- Response body:
```
{
    "success": true,
    "deleted": 11
}
```

#### POST /questions
1. 
- Creates a new question using the submitted question text, answer, category and difficulty score. Returns the id of the created question,a list of all questions, total questions number, and a success value.
- Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Can you help me ?", "answer":"Yes", "category":"1", "difficulty":"1" }'`
- Response body:
```
{
    "success": true,
    "question_id": 10,
    "questions": "questions":
    [
        {"answer":"Tom Cruise","category":5,"difficulty":4,"id":4,"question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"},
        
        {"answer":"Maya Angelou","category":4,"difficulty":2,"id":5,"question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},
        
        {"answer":"Edward Scissorhands","category":5,"difficulty":3,"id":6,"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},
        
        {"answer":"Muhammad Ali","category":4,"difficulty":1,"id":9,"question":"What boxer's original name is Cassius Clay?"},

        {"answer":"In 2021","category":1,"difficulty":1,"id":9,"question":"When I will get a job?"}
    ],
    "total_questions": 5
}
```
2. 
- Returns a list of all questions for whom the submitted search term is a substring of each question, success value, total questions number, current category.
- Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"the" }'`
- Response body:
```
{
    "current_category":"All",
    "questions":
    [
        {"answer":"Tom Cruise","category":5,"difficulty":4,"id":4,"question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"},
        
        {"answer":"Maya Angelou","category":4,"difficulty":2,"id":5,"question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},
        
        {"answer":"Edward Scissorhands","category":5,"difficulty":3,"id":6,"question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"},
        
    ],
    "success":true,
    "total_questions":3
}
```

#### GET /categories/{category_id}/questions
- Returns a list of all questions based on the passed category value in the uri, success value, total questions number, current category.
- Example: `curl http://127.0.0.1:5000/categories/4/questions`
- Response body:
```
{
    "currentCategory":"History",
    "questions":
    [
        {"answer":"Maya Angelou","category":4,"difficulty":2,"id":5,"question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"},
        
        {"answer":"Muhammad Ali","category":4,"difficulty":1,"id":9,"question":"What boxer's original name is Cassius Clay?"}
    ],
    "success":true,
    "totalQuestions":2
}
```


#### GET /categories
- Returns a list of categories, success value.
- Example: `curl http://127.0.0.1:5000/categories`
- Response body:
```
{
    "categories":
    {
        "1":"Science",
        "2":"Art","3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports"
    },
     
     "success":true
}
```

#### POST /play
- Returns a question with its id, question text, answer, category, difficulty score, a list of previous questions if exist,  and success value. Returns only a success value is all questions have been displayed.
- Example: `curl http://127.0.0.1:5000/play -X POST -H "Content-Type: application/json" -d '{ "quiz_category": {"id": "4","type": "History"},'previous_questions': [5] }'`
- Response body:
1. 
```
{
    "question": {
          "id": 9,
          "question": "question":"What boxer's original name is Cassius Clay?",
          "answer": "Muhammad Ali", 
          "difficulty": 1,
          "category": 4 
          },

    "previous_questions": [5, 9],
    "success": True}
}
```
2. 
```
{
    "success": True}
}
```

#### 2. Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}
```
The API will return four error types when requests fail:
- 404: Resource Not Found
- 405: Method not Allowed
- 422: Not Processable 
- 500: Server Error
