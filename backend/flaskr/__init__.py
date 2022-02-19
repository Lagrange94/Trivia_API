import os
from werkzeug.exceptions import HTTPException
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


##############################################################################
# - Helper functions
############################################################################## 


QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    questions_formatted = questions[start:end]

    return questions_formatted

# - Return unformatted questions formatted
def format_questions(questions_unformatted):
    return [question.format() for question in questions_unformatted]

# - Iterate over categories objects and format them in new object
def format_categories(categories_unformatted):
    categories_formatted = {}
    for category in categories_unformatted:
        categories_formatted[category.id] = category.type
    return categories_formatted


def create_app(test_config=None):



    ##########################################################################
    # - Config
    ##########################################################################   
    

    # - Create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # - Activate CORS   
    CORS(app)
    #CORS(app, resources={r"/api/*": {"origins": "*"}})

    # - Configure CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
 


    ##########################################################################
    # - Endpoints
    ##########################################################################


    # - GET endpoint to '/categories': Returns jsonified (key: value) pairs of
    # - categories
    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        
        # - Try to query, format and return the requested data
        try:
            # - Query and format the categories
            categories_formatted = format_categories(Category.query.all())

            # - If the categories_formatted object is emtpy throw an error
            if(len(categories_formatted) == 0):
                abort(404)
            
            # - Return jsonified data
            return jsonify({
                'success': True,
                'categories': categories_formatted,
                'total_categories': len(categories_formatted)
                })

        # - For an inner error catch the error type, if nonexisten raise 400
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(400)


    # - GET endpoint to '/questions?page=${integer}': Returns jsonified 
    # - question objects and further information 
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        
        # - Try to query, format and return the requested data
        try:            
            # - Query the requested data
            selection = Question.query.order_by(Question.id).all()
            questions_formatted = paginate_questions(request, selection)

            # - If the current_questions object is emtpy throw an error
            if(len(questions_formatted) == 0):
                abort(404)
            
            # - Query and format the categories
            categories_formatted = format_categories(Category.query.all())
            
            # - If the categories_formatted object is emtpy throw an error
            if(len(categories_formatted) == 0):
                abort(404)

            # - Return jsonified data
            return jsonify({
                'success': True,
                'questions': questions_formatted,
                'totalQuestions': len(Question.query.all()),
                'categories': categories_formatted,
                'currentCategory': (categories_formatted[questions_formatted[0]
                                                         ['category']])
                })

        # - For an inner error catch the error type, if nonexisten raise 400
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(400)


    # - GET endpoint to '/categories/<int:category_id>/questions': Returns 
    # - jsonified question objects and further information 
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_by_category(category_id):
        
        # - Try to query, format and return the requested data
        try:            
            # - Query the requested data by category_id and format it
            questions_unformatted = (Question.query
                                       .filter(Question.category == category_id)
                                       .order_by(Question.id).all())
            questions_formatted = format_questions(questions_unformatted)

            # - If the current_questions object is emtpy throw an error
            if(len(questions_formatted) == 0):
                abort(404)
            
            # - Query and format the categories
            categories_formatted = format_categories(Category.query.all())
            

            # - If the categories_formatted object is emtpy throw an error
            if(len(categories_formatted) == 0):
                abort(404)
            
            # - Return jsonified data
            return jsonify({
                'success': True,
                'questions': questions_formatted,
                'totalQuestions': len(Question.query.all()),
                'current_category': categories_formatted[category_id]
                })

        # - For an inner error catch the error type, if nonexisten raise 400
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(400)


    # - DELETE endpoint to '/questions/<int:question_id>': Returns jsonified 
    # - status response
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            # - Query the requested question
            question = (Question.query.filter(Question.id == question_id)
                                      .one_or_none())
            
            # - If the queried question does not exist throw an error
            if question is None:
                abort(404)

            # - Delete the queried question
            question.delete()

            # - Return jsonified data
            return jsonify({
                'success': True,
                'question_id': question_id
                })

        # - For an inner error catch the error type, if nonexisten raise 422
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(422)


    # - POST endpoint to '/quizzes': Returns jsonified question object
    @app.route("/quizzes", methods=["POST"])
    def next_question():
        try:
            # - Fetch the request body
            body = request.get_json()

            # - Query questions, excluding previous questions, chosing one 
            # - randomly
            previous_questions = body.get('previous_questions')
            possible_next_questions = (Question.query.filter(
                                        Question.id.notin_(previous_questions)
                                        ).all())
            next_question = random.choice(possible_next_questions).format()

            # - Return jsonified data
            return jsonify({
                    "success": True,
                    "question": next_question
                    })

        # - For an inner error catch the error type, if nonexisten raise 400
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(400)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    ##########################################################################
    # - Error handlers
    ##########################################################################


    # - 400: Bad request
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False, 
                "error": 400, 
                "message": "bad request"
            }), 400
        )

    # - 404: Not found
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                "success": False, 
                "error": 404, 
                "message": "resource not found"
            }),
            404,
        )

    # - 422: Unprocessable
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }),
            422,
        )

    return app

