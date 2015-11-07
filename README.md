# Combating Snake

This is the Combating Snake repo!

# Trying it out!
Visit the [Combating Snake website](https://combating-snake.herokuapp.com/) to try it out!

## Set it up
1. Clone the repository
2. `virtualenv venv`
3. `source venv/bin/activate`
4. `[sudo] pip install -r requirements.txt`

## Run it "locally"
Simply run `heroku local`! Still, it will use
ws://combating-snake-chat-backend.herokuapp.com as the Websockets backend, which
in turn will actually connect to the deployed Heroku app to look for data. So you
should not expect normal behavior by doing so. Please head on to the
[Combating Snake website](https://combating-snake.herokuapp.com/) to try it out.

# Test it
After setting up the repository, simply `python manage.py test`!
This will run tests on the Django app (a.k.a. this repository). Some of the views
are tested in the [Flask app](/jacky8hyf/CombatingSnakeChatBackend).