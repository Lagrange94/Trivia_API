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

# - Paginate the questions
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

            # - If the questions_formatted object is emtpy throw an error
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
            current_category = body.get('quiz_category', None)['id']

            # - If category 'all' was chosen filter previous questions
            if(current_category == 0):
                possible_next_questions = (Question.query.filter(
                                                Question.id.notin_(
                                                previous_questions)).all())

                # - Choose a random from the remaining questions
                next_question = random.choice(possible_next_questions).format()

            # - If a specific category was chosen, filter previous questions
            # - and for respective category
            else: 
                possible_next_questions = (Question.query.filter(
                                                Question.id.notin_(
                                                previous_questions),
                                                Question.category ==
                                                current_category)
                                                .all())

                # - Choose a random from the remaining questions
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


    # - POST endpoint to '/questions': Adds a new question to the database
    # - returns a response wether the action was successfull
    @app.route("/questions", methods=["POST"])
    def create_question():

        # - Fetch the request body
        body = request.get_json()

        # - Check if the body contains a search term
        search_term = body.get('searchTerm', None)

        # - Assign the values for a new question record
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        # - If the body doesnt contain a search term create a new question
        if(search_term is None and new_question is not None):

            # - Try to create a new question record and add it to the database
            try:
                question = Question(question = new_question, 
                                    answer = new_answer, 
                                    difficulty = new_difficulty, 
                                    category = new_category
                                    )
                question.insert()

                # - Return a response in case of success
                return jsonify(
                    {
                        "success": True
                    }
                )

            # - For an inner error catch the error type, if nonexisten raise 422
            except Exception as e:
                if isinstance(e, HTTPException):
                    abort(e.code)
                else:
                    abort(422)

        # - If the body does contain a search term search questions
        elif(search_term is not None):
            try:
                # - Search questions like the search term and format the result
                questions_unformatted = Question.query.filter(Question.question
                                            .ilike(f'%{search_term}%')).all()                            
                questions_formatted = format_questions(questions_unformatted)

                # - If the questions_formatted object is emtpy throw an error
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
                    'current_category': (categories_formatted[
                                            questions_formatted[0]['category']
                                            ])
                    })

            # - For an inner error catch the error type, if nonexisten raise 422
            except Exception as e:
                if isinstance(e, HTTPException):
                    abort(e.code)
                else:
                    abort(422)
        
        else:
            abort(400)

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
    
    # - 405: Not allowed
    @app.errorhandler(405)
    def unprocessable(error):
        return (
            jsonify({
                "success": False,
                "error": 405,
                "message": "not allowed"
            }),
            405,
        )

    return app

