# Combating Snake

This is the Combating Snake repo!

# Trying it out!
Visit the [Combating Snake website](https://combating-snake.herokuapp.com/) to try it out!

## Set it up
1. Clone the repository
2. `virtualenv venv`
3. `source venv/bin/activate`
4. `[sudo] pip install -r requirements.txt`

## Run it locally
1. Under the root of this repository, run `[CHAT_BACKEND_BASE_URL="ws://localhost:8081"] [PORT=8080] heroku local`
    1. The stuff in brackets are optional. But don't type the brackets themselves even if you add these options.
    2. `CHAT_BACKEND_BASE_URL` indicates which WebSocket server should the client JavaScript code connect to
    3. `PORT` indicates on which port should this Django app run on.
2. Clone [the chat backend repository](/jacky8hyf/CombatingSnakeChatBackend).
3. Under the root of the chat backend repository, run `[REST_HOST="http://localhost:8080"] PORT=8081 heroku local`
    1. The stuff in brackets are optional. But don't type the brackets themselves even if you add these options.
    2. `REST_HOST` indicates which RESTful API server should this app connect to
    3. `PORT` indicates on which port should this Flask app run on.
4. When you run these apps, make sure the port matches.
5. Open `http://localhost:8080` (for example) to see.

## Test it
After setting up the repository, simply `python manage.py test`!
This will run tests on the Django app (a.k.a. this repository). Some of the views
are tested in the [Flask app](/jacky8hyf/CombatingSnakeChatBackend).