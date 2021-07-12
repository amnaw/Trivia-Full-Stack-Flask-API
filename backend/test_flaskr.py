import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'postgres:Aa123456@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Define Test variables
        self.new_question = {
            'question': 'When I will get a job ?',
            'answer': 'in 2021', 
            'difficulty': 1,
            'category': '1'
        }
        self.searchTerm = {'searchTerm': 'the'}
        self.searchTerm_txt = "the"
        self.play_with_category = {'quiz_category': {
            'id': '1',
            'type': 'Science'},
            
            'previous_questions': []
            }
        self.play = {'quiz_category': {
            'id': '0',
            'type': ' '},
            'previous_questions': [11, 12, 13]
            }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Tests for GET all questions
    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        # gets the json of the response body
        data = json.loads(response.data)  

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        # there are actual questions
        self.assertTrue(len(data['questions'])) 
        self.assertTrue(len(data['categories']))

    def test_404_request_non_existing_page(self):
        response = self.client().get('/questions?page=999')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not Found') 
    
    # Tests for POST a new question
    def test_create_question(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_405_question_creation_not_allowed(self):
        response = self.client().post('/questions/77', json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not Allowed')
    
    # Tests for DELETE a question
    def test_delete_question(self):
        response = self.client().delete('/questions/5')
        data = json.loads(response.data)

        question = Question.query.get(5)  # delete from db

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertEqual(question, None)
    
    def test_422_question_not_exist(self):
        response = self.client().delete('/questions/999')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_405_deletion_not_allowed(self):
        response = self.client().delete('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not Allowed')
    
    # Tests for GET categories
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data) 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
  
    def test_405_add_categories_not_allowed(self):
        response = self.client().post('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not Allowed') 
    
    # Tests for POST searchTerm and get questions
    def test_search_questions(self):
        response = self.client().post('/questions', json=self.searchTerm)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    
    def test_500_search_server_error(self):
        response = self.client().post('/questions', json=self.searchTerm_txt)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Server Error') 

    def test_405_search_not_allowed(self):
        response = self.client().post('/questions/88', json=self.searchTerm)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not Allowed') 
    
    # Tests for GET all questions per Category
    def test_get_category_questions(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data) 

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])
        self.assertTrue(len(data['questions']))

    def test_404_non_existing_category(self):
        response = self.client().get('/categories/999/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not Found') 
    
    # Tests for POST to Play Quiz
    def test_get_first_question(self):
        # 1st ques with category
        response = self.client().post('/play', json=self.play_with_category) 
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_next_question(self):
        # next ques without category
        response = self.client().post('/play', json=self.play) 
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_405_play_not_allowed(self):
        response = self.client().get('/play')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not Allowed')
    
    def test_500_play_error(self):
        response = self.client().post('/play') 
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Server Error')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()