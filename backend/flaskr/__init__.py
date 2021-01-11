import os
from flask import Flask, request, abort, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, not_ 
from sqlalchemy.util.langhelpers import NoneType
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route('/categories')
    def get_categories():
        selection = Category.query.all()

        if len(selection) == 0:
            abort(404)

        categories = {category.id: category.type for category in selection}

        return jsonify({
            'success': True,
            'status_code': 200,
            'categories': categories,
        })
    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
    @app.route('/questions')
    def get_questions():
        category_id = request.args.get('category', None, type=int)
        if type(category_id) is int:
            category = Category.query.filter_by(id=category_id).one_or_none()
            if category is None:
                abort(404)
            current_category = category.type
        else:
            current_category = None

        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)

        selection = Category.query.all()
        categories = {category.id: category.type for category in selection}

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'status_code': 200,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': current_category,
            'categories': categories
        })
    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    @app.route('/questions/<int:book_id>', methods=['DELETE'])
    def delete_questions(book_id):
        question = Question.query.filter_by(id=book_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()
        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'status_code': 200,
            'deleted': book_id,
            'total_questions': len(questions),
            'questions': current_questions
        })

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    @app.route('/questions', methods=['POST'])
    def post_questions():
        body = request.get_json()

        try:
          question = body.get('question')
          answer = body.get('answer')
          category = body.get('category')
          difficulty = body.get('difficulty')

        except:
          abort(404)

        is_new_question = Question.query.filter_by(question = question).one_or_none()
        
        if is_new_question is None:
          question_obj = Question(question=question, answer = answer, category = category, difficulty =difficulty)
          question_obj.insert()

        else:
          abort(409)

        return jsonify({
            'success': True,
            'status_code': 200,
            'question': question,
        })


    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm')
        search_result = Question.query.filter(func.lower(Question.question).\
        contains(search_term.lower(), autoescape=True)).all()
        questions = [question.format() for question in search_result] 
        return jsonify({
            'success': True,
            'status_code': 200,
            'questions': questions,
            'total_questions': len(questions),
            'current_category': None
        })
    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        if Category.query.filter_by(id= category_id).one_or_none() is None:
          print(category_id)
          abort(404)
        questions = Question.query.filter_by(category= category_id).all()
        #category_questions = [question.format() for question in questions]
        category_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'status_code': 200,
            'questions': category_questions
        })
    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
    @app.route('/play', methods=['POST'])
    def post_play():
        body = request.get_json()
        category_id = body.get('quiz_category')['id'] 
        previous_questions = body.get('previous_questions')

        if category_id is None:
            question_selection = Question.query.filter(not_(Question.id.in_(previous_questions))).all()
        elif Category.query.filter_by(id= category_id).one_or_none() is None:
            print(category_id)
            abort(404)
        else:
            question_selection = Question.query.filter_by(category = category_id)\
                .filter(not_(Question.id.in_(previous_questions))).all()
        
        #questions = [question.format() for question in question_selection]
        question = random.choice(question_selection).format()
        return jsonify({
            'success': True,
            'status_code': 200,
            'question': question,
        })

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(409)
    def already_exist(error):
        return jsonify({
            "success": False,
            "error": 409,
            "message": "Already exist"
        }), 409

    return app
