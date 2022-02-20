import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""



    ##########################################################################
    # - Config
    ##########################################################################


    def setUp(self):
        """Define test variables and initialize app."""
        user = 'postgres'
        password = 'subwoofer67'   
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(user, password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    

    def tearDown(self):
        """Executed after reach test"""
        pass



    ##########################################################################
    # - Tests
    ##########################################################################

    # - Test /categories endpoint
    def test_retrieve_categories(self):

        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_405_post_category(self):

        response = self.client().post('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not allowed')


    # - Test /questions GET endpoint
    def test_retrieve_paginated_questions(self):
        response = self.client().get("/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])

    def test_404_retrieve_paginated_questions(self):
        response = self.client().get("/books?page=1000", json={"rating": 1})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    # - Test /category/<int:category_id>/questions GET endpoint
    def test_retrieve_categorized_questions(self):
        response = self.client().get("/categories/1/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])

    def test_405_retrieve_categorized_questions(self):
        response = self.client().post("/categories/1/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "not allowed")

    # - Test /question/<int:question_id> DELETE endpoint
    def test_delete_question(self):
         question_id = 5
         response = self.client().delete(f'/questions/{question_id}')
         data = json.loads(response.data)

         question = Question.query.filter(Question.id == question_id).one_or_none()

         self.assertEqual(response.status_code, 200)
         self.assertEqual(data['success'], True)
         self.assertEqual(data['question_id'], question_id)
         self.assertEqual(question, None)

    def test_404_delete_question(self):
        response = self.client().delete("/questions/1000")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    # - Test /quizzes POST endpoint
    def test_quizzes(self):
        response = self.client().post('/quizzes', json={'previous_questions': 
                                                            [1, 4, 20, 15], 
                                                        'quiz_category': 
                                                            {'type': 'click', 
                                                            'id': 0}})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
    
    def test_405_quizzes(self):
        response = self.client().patch('/quizzes', json={'previous_questions':
                                                            [1, 4, 20, 15], 
                                                        'quiz_category': 
                                                            {'type': 'click',
                                                            'id': 0}})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["success"], False)


    # - Test /questions POST endpoint
    def test_search_questions(self):
        response = self.client().post('/questions', json={'searchTerm': 
                                                                    'with'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_post_question(self):
        response = self.client().post('/questions', json={
                                                "question": "What means lol?",
                                                "answer": "laughing out loud",
                                                "difficulty": 1,
                                                "category": 5
                                                })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_questions(self):
        response = self.client().post('/questions', json = {})

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()