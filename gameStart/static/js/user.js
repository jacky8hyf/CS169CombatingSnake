var UserHandler = (function() {

    // PRIVATE VARIABLES
    var apiUrl = '';
    // PRIVATE METHODS
    var loginForm;
    var signupForm;
    var sessionId;
    var userId;
    var usernameGlobal;

    // Handle room requests
    var createRoomForm;
    var createRoomButton;

    /**
     * HTTP GET request
     * @param  {string}   url       URL path
     * @param  {function} onSuccess   callback method to execute upon request success (200 status)
     * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
     * @return {None}
     */
    var makeGetRequest = function(url, onSuccess, onFailure) {
        $.ajax({
            type: 'GET',
            url: apiUrl + url,
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };

    /**
     * HTTP PUT request
     * @param  {string}   url       URL path
     * @param  {Object}   data      JSON data to send in request body
     * @param  {function} onSuccess   callback method to execute upon request success (200 status)
     * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
     * @return {None}
     */
    var makePutRequest = function(url, data, onSuccess, onFailure) {
        $.ajax({
            type: 'PUT',
            url: apiUrl + url,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };


    /**
     * HTTP POST request
     * @param  {string}   url       URL path
     * @param  {Object}   data      JSON data to send in request body
     * @param  {function} onSuccess   callback method to execute upon request success (200 status)
     * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
     * @return {None}
     */
    var makePostRequest = function(url, data, onSuccess, onFailure) {
        $.ajax({
            type: 'POST',
            url: apiUrl + url,
            headers: {
                'Snake-Session-Id': sessionId,
            },
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };

    var onSuccessLogin = function(data) {
        sessionId = data.sessionId;
        userId = data.userId;
        loginForm.find('div.error div.login_error').text(" ");
        signupForm.find('div.error div.signup_error').text(" ");
        $('div.userInfo').show();
        $('div.usernameInfo').text("Welcome, " + usernameGlobal + " !");
        loginForm.hide();
        signupForm.hide();
        //createRoomForm.show();
    }

    /**
     * Add event handlers for submitting the create form.
     * @return {None}
     */
    var attachLoginHandler = function(e) {
        loginForm.on('click', '.submit-login', function(e) {
            e.preventDefault()
            var errorElem = loginForm.find('div.error div.login_error');
            var username = loginForm.find('div.form_field #login_username').val();
            usernameGlobal = username;
            var password = loginForm.find('div.form_field #login_password').val();
            var user ={'username':username, 'password' : password};

            if (username.length == 0 || password.length == 0) {
                errorElem.text("Username and password must be nonempty.");
                return;
            }

            var onSuccess = function(data) {
                sessionId = data.sessionId;
                userId = data.userId;
                errorElem.text(" ");
            };

            var onFailure = function(response) {
                var data = response.responseJSON;
                errorElem.text(data.msg);
            };
            makePutRequest("/users/login", user, onSuccessLogin, onFailure);
        });

    };

    var attachSignupHandler = function(e) {
        signupForm.on('click', '.submit-signup', function(e) {
            e.preventDefault()
            var errorElem = signupForm.find('div.error div.signup_error');
            var username = signupForm.find('div.form_field #signup_username').val();
            usernameGlobal = username;
            var nickname = signupForm.find('div.form_field #signup_nickname').val();
            var password = signupForm.find('div.form_field #signup_password').val();
            var passwordRetype = signupForm.find('div.form_field #signup_password_retype').val();
            // Error handling
            if (password != passwordRetype) {
                errorElem.text("Pasword does not match.");
                return;
            }

            var user ={'username':username, 'nickname':nickname, 'password' : password};
            // HANDLE RESPONSE FROM SERVER
            var onSuccess = function(data) {
                sessionId = data.sessionId;
                userId = data.userId;
                errorElem.text(" ");
            };
            var onFailure = function(response) {
                var data = response.responseJSON;
                errorElem.text(data.msg);
            }
            makePostRequest("/users/", user, onSuccessLogin, onFailure);
        });
    };

    var attachCreateRoomHandler = function(e) {
        $('body').on('click','.create_button', function(e){
            var room = {};
            var onSuccess = function(data) {
                createRoomForm.find(".room_id").text('Room ' + data.roomId);
                //createRoomForm.find(".player .name").text(data.creator.nickname);
                createRoomForm.find(".player .name").text(usernameGlobal);
                createRoomForm.show();
                createRoomButton.hide();
                $('#cssmenu').hide();
            };
            var onFailure = function(error) {
                console.log(error);
                //console.error('create room fails');
            };
            var url = "/rooms";
            makePostRequest(url, room, onSuccess, onFailure);
        });
    };


    /**
     * Start the app by displaying the most recent smiles and attaching event handlers.
     * @return {None}
     */
    var start = function() {
        loginForm = $("div.login_container");
        signupForm = $("div.signup_container");
        createRoomForm = $(".create_room");
        createRoomButton = $(".create_button");
        createRoomForm.hide();

        attachLoginHandler();
        attachSignupHandler();
        attachCreateRoomHandler();
    };

    // PUBLIC METHODS
    return {
        start: start
    };
})();
