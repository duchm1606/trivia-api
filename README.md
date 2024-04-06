# The Trivia Project Introduction - Udacity Fullstack of Web Developer

The Trivia App project, originally developed by Udacity, is a key component of the Fullstack Nanodegree program. This project is introduced in Course 2, focusing on API Development and Documentation. The primary objective of undertaking this project is to provide learners with a practical opportunity to apply their skills in structuring and implementing well-formulated API endpoints. These skills are essential, leveraging a deep understanding of HTTP protocols and API development best practices.

Participants are tasked with the development of the API portion of the app within the backend, encompassing both the implementation and testing phases. This development is crucial for ensuring seamless integration with the frontend, aiming to offer end-users a robust and interactive experience.

By engaging in this project, learners are expected to solidify their grasp on API construction, honing their ability to create efficient, scalable, and well-documented APIs. Ultimately, the successful completion of this project will enable the Trivia app users to enjoy a comprehensive and engaging platform for trivia quizzes, reflecting the effective application of acquired API development skills.

At the end, user of the app should be able to

1. Display questions - both all questions and by category. Questions should show the question, category, and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include the question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Initial Instruction

See [Instruction](https://github.com/itsnot-aduck/trivia-api/blob/main/INSTRUCTION.md) given by Udacity

## Getting Started

### Pre-requisites and Local Development

Developers using this project should have Python3.7, pip and node Installed on the local machine

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

From the frontend folder, run the following commands to start the client:

```
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

### Tests

In order to run tests navigate to the backend folder and run the following commands:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Quick Start

- Base URL: This app can locally run and is not hosted as a base URL. The backend app is hosted at the default `http://127.0.0.1:5000` or `localhost:5000`, which is set as a proxy in the frontend configuration

- Authentication: This version doesn't require authentication or API keys

### Error Handing

An error can be returned as JSON Objects with the format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API can return some error types when request fail

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Method not allowed
- 500: Internal server error

### Endpoints

#### `GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

Example: `curl -X POST -H "Content-Type: application/json" http://127.0.0.1:5000/categories`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### `GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string
  If no page provided, it returns all the questions in the database

Example: `curl -H "Content-Type: application/json" http://127.0.0.1:5000/questions?page=1`

```
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 100,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```

#### `GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string

Example: `curl -H "Content-Type: application/json" http://127.0.0.1:5000/categories/1/questions`

```
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
}
```

#### `DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

Example: `curl -X DELETE -H "Content-Type: application/json" http://127.0.0.1:5000/questions/1`

```
{
  "deleted_id": 1,
}
```

#### `POST '/quizzes'`

Sends a post request in order to get the next question

Example: `curl -X POST -d "{\"previous_questions\": [1, 4, 20, 15], \"quiz_category\": \"Art\"}" -H "Content-Type: application/json" http://127.0.0.1:5000/quizzes`

```
{
  "question": {
    "id": 1,
    "question": "This is a question",
    "answer": "This is an answer",
    "difficulty": 5,
    "category": 4
  }
}
or
{}
```

#### `POST '/questions'`

Sends a post request in order to add a new question

Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "Heres a new question string","answer": "Heres a new answer string","difficulty": 1,"category": 3}'`

```
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```

#### `POST '/questions'`

Sends a post request in order to search for a specific question by search term
Example: `{'searchTerm': 'this is the term the user is looking for'}`

```
{
  "questions": [
    {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 5
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "Entertainment"
}
```

## Author(s)

- [Duc HoangMinh](https://github.com/itsnot-aduck)
- Powered by Udacity

## Acknowledgements

I want to say thank to the team at Udacity for great lessions, also a great gratitude for StackOverFlow :D
