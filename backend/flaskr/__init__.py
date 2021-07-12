import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from collections import ChainMap
from functools import reduce
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    Set up CORS. Allow '*' for origins. # CORS(app) basic
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    The after_request dec set Access-Control-Allow  # CORS response headers
    '''
    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')

        return response

    '''
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories')
    def all_categories():
        categoriesTup = Category.query.order_by(Category.id).all()
        categories_list = [categorie.format() for categorie in categoriesTup]
        categories = {x['id']: x['type'] for x in categories_list}

        if len(categoriesTup) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'categories': categories
        })

    def paginate_qes(request, selection):  
        # this function is inspired from Udacity's excercise solution
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions
    '''
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
    '''
    @app.route('/questions')
    def all_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_qes(request, selection)

        categoriesTup = Category.query.order_by(Category.id).all()
        categories_list = [categorie.format() for categorie in categoriesTup]
        categories = {x['id']: x['type'] for x in categories_list}

        values_view = categories.values()
        value_iterator = iter(values_view)
        current_category = next(value_iterator)
        
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(Question.query.all()),
          'categories': categories,
          'current_category': "All"
        })

    '''
    Create an endpoint to DELETE question using a question ID.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            q = Question.query.filter(Question.id == question_id).one_or_none()
            question = q

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
              'success': True,
              'deleted': question_id
            })

        except:
            abort(422)

    '''
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        searchTerm = body.get('searchTerm', None)

        try:
            if searchTerm:  
                # in case of searching, there will be posted searchTerm
                selection = Question.query.order_by(Question.id).filter(
                  Question.question.ilike('%{}%'.format(searchTerm)))
                current_questions = paginate_qes(request, selection)

                categoriesTup = Category.query.order_by(Category.id).all()
                c_l = [categorie.format() for categorie in categoriesTup]
                categories_list = c_l
                categories = {x['id']: x['type'] for x in categories_list}

                values_view = categories.values()
                value_iterator = iter(values_view)
                current_category = next(value_iterator)
                return jsonify({
                  'success': True,
                  'questions': current_questions,
                  'total_questions': len(Question.query.all()),
                  'current_category': current_category
                })

            else: 
                # in case of insert new Q, there 'll be posted Q's data
                question = Question(
                  question=question, 
                  answer=answer, 
                  category=category, 
                  difficulty=difficulty)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_qes(request, selection)

                return jsonify({
                  'success': True,
                  'question_id': question.id,
                  'questions': current_questions,
                  'total_questions': len(Question.query.all())

                })
        
        except:
            abort(422)

    '''
    Create a GET endpoint to get questions based on category. 
    '''
    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id):
        category = Category.query.get(category_id)
        selection = Question.query.filter(Question.category == category_id)
        questions = paginate_qes(request, selection)

        if len(questions) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'questions': questions,
          'totalQuestions': 1,
          'currentCategory': category.type 
          })

    '''
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random question. 
    '''
    @app.route('/play', methods=['POST'])
    def quizzes():
        body = request.get_json()
        # list of int
        previous_questions = body.get('previous_questions')

        quiz_category = body.get('quiz_category', None)
        quiz_category = quiz_category.get('id')
        category = Category.query.get(quiz_category)
        flag = False
        
        if category:
            while flag is False:
                question = random.choice(Question.query.filter(
                  Question.category == category.id).all())
                if (question.id not in previous_questions):
                    flag = True
                    return jsonify({
                      'question': {
                        'id': question.id,
                        'question': question.question,
                        'answer': question.answer, 
                        'difficulty': question.difficulty,
                        'category': question.category}, 

                      'previous_questions': 
                      previous_questions.append(question.id),
                      'success': True})
                if (question.id in previous_questions):
                    flag = False
                else: 
                    # in case questions are < questionsPerPlay=5,
                    # and we diplayed them all in the game, 
                    # so rturn json without "question" dic to set forceEnd True
                    return jsonify({'success': True})

        else:
            while flag is False:
                question = random.choice(Question.query.all())
                q_i = question.id
                if (question.id not in previous_questions):
                    flag = True
                    return jsonify({
                      'question': {
                        'id': question.id,
                        'question': question.question,
                        'answer': question.answer, 
                        'difficulty': question.difficulty,
                        'category': question.category},

                      'previous_questions': previous_questions.append(q_i),
                      'success': True})
                if (question.id in previous_questions):
                    flag = False
                else: 
                    return jsonify({'success': True})

    '''
    Create error handlers for all expected errors  
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Resource not Found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable"
            }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad Request"  
            }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "Method not Allowed"   
            }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Server Error"   
            }), 500

    return app

    