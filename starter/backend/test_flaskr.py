import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:1234@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            self.new_question = {
            'question': "'Whose autobiography is entitled 'I Know Why the Caged Bird Sings ?",
            'answer': 'Maya Angelou',
            'category': "2",
            'difficulty':2}
            self.wrong_question={
                'question':None,
                'answer': None,
                'acategory': None,
                'difficulty': "hello"

            }
            

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        pass

    def test_error422_create_new_question(self):
            rs = self.client().post('/questions', json=self.wrong_question)
            data = json.loads(rs.data)
            self.assertEqual(rs.status_code, 422)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'unprocessable')

            pass
   
    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': "'Whose autobiography is entitled 'I Know Why the Caged Bird Sings ?"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
   
    def test_error422_search_question(self):
        res = self.client().post('/questions', json={'searchTerm': ""})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    def test_get_questions_in_specific_category(self):
        res = self.client().get('/categories/2/questions', json={'searchTerm': ""})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_error422_get_questions_in_specific_category(self):
        res = self.client().get('/categories/10/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertEqual(data['success'], True)
       
    def test_quizes_play(self):
        res = self.client().post('/quizzes', json={ "quiz_category":{"id":2, "type":"Art"}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['success'], True)

    def test_error404_quizes_play(self):
        res = self.client().post('/quizzes', json={ 'previous_questions':[], 'quiz_category':{'id':10,'type':'Imagination'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_delete_question(self):
         res = self.client().delete('/questions/15')
         data = json.loads(res.data)
         self.assertEqual(res.status_code, 200)
         self.assertEqual(data['success'], True)

    def test_error422_delete_question(self):
         res = self.client().delete('/questions/50')
         data = json.loads(res.data)
         self.assertEqual(res.status_code, 422)
         self.assertEqual(data['success'], False)
         self.assertEqual(data['message'], 'unprocessable')

    def test_get_pagination_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['currentCategory'])


    def test_error404_get_pagination_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
        



        
if __name__ == "__main__":
    unittest.main()