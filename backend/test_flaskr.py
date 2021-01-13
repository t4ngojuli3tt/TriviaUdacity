import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from flaskr import create_app
from models import setup_db, Question, Category, db_user, db_password, db_host


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f'postgresql://{db_user}:{db_password}@{db_host}/{self.database_name}'
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_get_questions_with_category(self):
        res = self.client().get('/questions?category=1')
        data = json.loads(res.data)

        category = Category.query.filter_by(id=1).one_or_none()
        self.assertEqual(data['current_category'], category.type)

    def test_delete_question(self):
        question_id = 4
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter_by(id=question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question, None)

    def test_post_question(self):
        res = self.client().post('/questions', json={'question': 'How are things?',
                                                     'answer': 'All good!', 'category': 2, 'difficulty': 5})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], 'How are things?')

    def test_post_existing_question(self):
        question = Question.query.first()
        res = self.client().post('/questions', json={'question': f'{question.question}',
                                                     'answer': f'{question.answer}', 'category': f'{question.category}', 'difficulty': f'{question.difficulty}'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 409)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Already exist")

    def test_search_question(self):

        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'title'})
        data = json.loads(res.data)

        search_result = Question.query.filter(func.lower(Question.question).
                                              contains('title', autoescape=True)).all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), len(search_result))

    def test_get_questions_by_category(self):
        category_id = 1
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions_by_category_404(self):
        category_id = 10
        res = self.client().get(f'/questions/categories/{category_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_post_play(self):
        res = self.client().post(
            '/play', json={'quiz_category': {'id': 1}, 'previous_questions': [20, 21]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['question'],
                         'Hematology is a branch of medicine involving the study of what?')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
