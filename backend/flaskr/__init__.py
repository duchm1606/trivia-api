import os
from flask import Flask, request, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

# Get categories type
def get_categories_type(category_id):
    selection = Category.query.filter(Category.id == category_id).one_or_none()
    if not selection:  
        return 'all'
    else:
        return f'{selection.type}'

# Create pagination
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    # Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    # Create an endpoint to handle GET requests for all available categories.
    @app.route('/categories', methods = ['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)
        
        # Setup a dict to store result
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type
        
        # Return a response code
        return jsonify({
            "categories": categories_dict,
        })

    """
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    # Create endpoint to handle GET requests for questions
    @app.route('/questions', methods = ["GET"])
    def get_questions(category = "all"):
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        print(f'Question get: {len(current_questions)}')

        if len(current_questions) == 0:
            abort(404)
        
        return jsonify({
            "questions": current_questions,
            "totalQuestions": len(selection),
            "currentCategory": category,
            "categories": get_categories().json["categories"]
        }), 200

    """
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        print(question)
        if question is None:
            print("Not found")
            abort(404)
        else:
            try:
                db.session.delete(question)
                db.session.commit()
                return jsonify({
                    "deleted": question_id
                }), 200
            except:
                db.session.rollback()
                db.session.close()
                abort(422)    
    """
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=["POST"])
    def create_or_search_questions():
        body = request.get_json()
        if not body:
            abort(400)
        try: 
            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_category = body.get("category", None)
            new_difficulty = body.get("difficulty", None)
            search = body.get("searchTerm", None)
            # Check for 2 case: find or create 
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike(f'%{search}%')
                ).all()

                print(selection)

                if len(selection) == 0:
                    abort(404)
                else:
                    #paginate 
                    current_questions = paginate_questions(request, selection)
                    # Dump current_category
                    current_category = 'Entertainment'
                    questions = []
                    for question in current_questions:
                        questions.append({
                            "id": question["id"],
                            "question": question["question"],
                            "answer": question["answer"],
                            "difficulty": question["difficulty"],
                            "category": question["category"]
                        })
                    # Dump current category
                    return jsonify({
                        "questions": questions,
                        "totalQuestions": len(selection),
                        "currentCategory": current_category
                    }), 200
            
            else:
                # Check for valid question or answer
                if len(new_question) == 0 or len(new_answer) == 0 or new_category == 0 or new_difficulty is None:
                    abort(422)

                question = Question(new_question, new_answer, new_category, new_difficulty)
                db.session.add(question)
                db.session.commit()
                
                # Return nothing
                return jsonify({}), 200
        except:
            db.session.rollback()
            db.session.close()
            abort(422)



    """
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        try:
            selection = Question.query.filter(Question.category == str(category_id)).all()
            current_questions = paginate_questions(request,selection)
            if len(current_questions) == 0:
                abort(404)
            category = Category.query.filter(Category.id == category_id).one_or_none()
            currentCategory = None
            if category is not None:
                currentCategory = category.type
            else:  
                abort(404)
            questions = []
            for question in current_questions:
                questions.append({
                    "id": question["id"],
                    "question": question["question"],
                    "answer": question["answer"],
                    "difficulty": question["difficulty"],
                    "category": question["category"]
                })
            return jsonify({
                "questions": questions,
                "totalQuestions": len(current_questions),
                "currentCategory": currentCategory
            }), 200
        except:
            abort(404)
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
    @app.route("/quizzes", methods = ["POST"])
    def quizz_questions():
        try:
            # Get previous questions
            previous_questions = request.json.get('previous_questions')
            quiz_category = request.json.get('quiz_category')
            print(quiz_category)
            print(previous_questions)

            # Get available questions
            if quiz_category != 0:
                questions = Question.query.filter_by(category = quiz_category).all()
            else:
                questions = Question.query.all()

            # Get chosen one
            chosen_question = random.choice(questions)
            while(chosen_question.id in previous_questions):
                chosen_question = random.choice(questions)
            print(chosen_question.id)

            # Export the deserved item
            question_data = {
                "id": chosen_question.id,
                "question": chosen_question.question,
                "answer": chosen_question.answer,
                "difficulty": chosen_question.difficulty,
                "category": chosen_question.category
            }
            return jsonify({
                "question": question_data
            })
        except:
            abort(404)
    """
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Internal server error"}), 500,
        )

    return app

