## API Reference

### Getting Started
- First the database_path in backend/models.py has to be set to connect to the local database
- Secondly the READMEs in the frontend and backend folder should be read carefully to install neccessary packages and set relevant dependencies as well as to fill the database.
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Not Allowed
- 422: Not Processable 

### Endpoints 
#### GET /categories
- General:
    - Returns the content of the category object, success value, and total number of categories
- Sample: `curl http://127.0.0.1:5000/categories`

    ```
    {
    "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
    }, 
    "success": true, 
    "total_categories": 6
    }
    ```

#### GET /questions
- General:
    - Returns the content of the category object, the current category, a list of question objects, success value, and total number of questions
    - Question results are paginated in groups of 10. Include an optional request argument to choose page number, starting from 1 (default = 1). 
- Sample: `curl http://127.0.0.1:5000/questions?page=2`

    ```
    {
    "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
    }, 
    "currentCategory": "Geography", 
    "questions": [
        {
        "answer": "Agra", 
        "category": 3, 
        "difficulty": 2, 
        "id": 15, 
        "question": "The Taj Mahal is located in which Indian city?"
        }, 
        {
        "answer": "Escher", 
        "category": 2, 
        "difficulty": 1, 
        "id": 16, 
        "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        }, 
        ...,
        ...,
        ...
    ], 
    "success": true, 
    "totalQuestions": 19
    }
    ```

#### GET /categories/{category_id}/questions
- General:
    - Returns the current category, a list of question objects from the respective category, success value, and total number of questions
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

    ```
    {
    "current_category": "Science", 
    "questions": [
        {
        "answer": "The Liver", 
        "category": 1, 
        "difficulty": 4, 
        "id": 20, 
        "question": "What is the heaviest organ in the human body?"
        }, 
        {
        "answer": "Alexander Fleming", 
        "category": 1, 
        "difficulty": 3, 
        "id": 21, 
        "question": "Who discovered penicillin?"
        }, 
        {
        "answer": "Blood", 
        "category": 1, 
        "difficulty": 4, 
        "id": 22, 
        "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ], 
    "success": true, 
    "totalQuestions": 19
    }
    ```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question and the success value. 
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/9`

    ```
    {
    "question_id": 9, 
    "success": true
    }
    ```

#### POST /quizzes
- General:
    - A list of previous questions (which might be empty) and the current category have to be provided.
    - Returns a random question from the current category which ist not in the list of previous questions and the success value.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 4, 20, 15], "quiz_category": {"type": "Art", "id": "2"}}'`

    ```
    {
    "question": {
        "answer": "Escher", 
        "category": 2, 
        "difficulty": 1, 
        "id": 16, 
        "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    "success": true
    }
    ```

#### POST /questions (Add question)
- General:
    - Creates a new question using the submitted title, author and rating. Returns the success value. 
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "What means lol?", "answer": "laughing out loud", "difficulty": 1, "category": 5}'`

    ```
    {
    "success": true
    }
    ```

#### POST /questions (Search questions)
- General:
    - Returns a list of question objects whose questions match the (case insensitive) search term content as well as the current category, the success value and the number of total questions.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "who}'`

    ```
    {
    "current_category": "History", 
    "questions": [
        {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }, 
        {
        "answer": "George Washington Carver", 
        "category": 4, 
        "difficulty": 2, 
        "id": 12, 
        "question": "Who invented Peanut Butter?"
        }, 
        {
        "answer": "Alexander Fleming", 
        "category": 1, 
        "difficulty": 3, 
        "id": 21, 
        "question": "Who discovered penicillin?"
        }
    ], 
    "success": true, 
    "totalQuestions": 19
    }
    ```