var UserHandler = (function() {

    // PRIVATE VARIABLES
    var apiUrl = '';
    // PRIVATE METHODS
    var loginForm;
    var signupForm;
    var sessionId;
    var userId;
    var usernameGlobal;
    var userInfo;
    var roomsAction;
    var actionMenu;

    // Handle room requests
    var createRoomForm;
    var createRoomButton;

    var joinRoomButton;
    var roomSize = 8;
    var players;    //list of players inside the room
    var playerHtmlTemplate;

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
                'X-Snake-Session-Id': sessionId,
            },
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };

    var makeDeleteRequest = function(url, onSuccess, onFailure) {
        $.ajax({
            type: 'DELETE',
            url: apiUrl + url,
            headers: {
                'Snake-Session-Id': sessionId,
            },
            //data: JSON.stringify(data),
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

        $('div.form_field #signup_username').val("");
        $('div.form_field #signup_nickname').val("");
        $('div.form_field #signup_password').val("");
        $('div.form_field #signup_password_retype').val("");

        $('div.form_field #login_username').val("");
        $('div.form_field #login_password').val("");

        loginForm.hide();
        signupForm.hide();
        roomsAction.show();
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
            var onFailure = function(response) {
                var data = response.responseJSON;
                errorElem.text(data.msg);
            };
            makePutRequest("/users/login", user, onSuccessLogin, onFailure);
        });
    };

    var attachLogoutHandler = function(e) {
        $('div.userInfo').on('click', '.logout', function(e) {
            e.preventDefault()

            var onSuccess = function(data) {
                loginForm.show();
                userInfo.hide();
                actionMenu.show();
                createRoomForm.hide();
            };

            var onFailure = function(response) {
                var data = response.responseJSON;
                errorElem.text(data.msg);
            };
            makeDeleteRequest("/users/login", onSuccess, onFailure);
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
            var onFailure = function(response) {
                var data = response.responseJSON;
                errorElem.text(data.msg);
            }
            makePostRequest("/users/", user, onSuccessLogin, onFailure);
        });
    };

    var attachCreateRoomHandler = function(e) {
        $('body').on('click','.create_button', function(e){
			e.preventDefault();
            var room = {};
            var onSuccess = function(data) {
                var player = $(playerHtmlTemplate);
                //player.find('.ready').val(1);
                player.find('.name').text(usernameGlobal);
                players.append(player);
                createRoomForm.find(".room_id").text('Room ' + data.roomId);
                //createRoomForm.find(".player .name").text(data.creator.nickname);
                createRoomForm.find(".player .name").text(usernameGlobal);
                createRoomForm.show();
                actionMenu.hide();
                roomsAction.hide();
            };
            var onFailure = function(error) {
                console.log(error);
            };
            var url = "/rooms";
            makePostRequest(url, room, onSuccess, onFailure);
        });
    };

    var attachJoinRoomHandler = function(e) {
        $('body').on('click','.submit-roomjoin', function(e){
            e.preventDefault()
            var onSuccess = function(data) {
                /* loop through room list to find the first available room and 
                assign it to the user, then make a post request to inform the server
                size-1 for creator
                */
                console.log("enter onSuccess");
                var available_room;
                for (room in data.rooms){
                    if(!room.hasOwnProperty("members")){
                        available_room = data.rooms[room];
                        break;
                    }
                    else if((room.members).length < roomSize-1){
                        available_room = data.rooms[room];
                        break;
                    }
                }
                //if find available room
                if(available_room != null){
                    var url = "/rooms/" + available_room.roomId + "/members/" + userId;
                    console.log("find available_room");
                    var onFinalSuccess = function(e){
                        createRoomForm.find('.room_id').text("Room " + available_room.roomId);

                        var player1 = $(playerHtmlTemplate);
                        player1.find('.name').text(available_room.creator.userId);
                        //player1.find('.ready').val(1);
                        players.append(player1);
                        
                        
                        if(available_room.hasOwnProperty("members")){
                            for(i=0; i< available_room.members.length; i++){
                                var player = $(playerHtmlTemplate);
                                player.find('.name').text(data.members[i].userId);
                                player.find('.ready').val(1);
                                players.append(player);
                            }
                        }
                        else{
                            var player2 = $(playerHtmlTemplate);
                            player2.find('.name').text(usernameGlobal);
                            //player2.find('.ready').val(1);
                            players.append(player2);

                        }
                        createRoomForm.show();
                        joinRoomButton.hide();
                        createRoomButton.hide();
                        console.log("join ok");
                             
                    };

                    var onFinalFailure = function(e){
                        console.log(e);
                    }
                    var room={};
                    makePutRequest(url, room, onFinalSuccess, onFinalFailure);
                   
                    $('#cssmenu').hide();
                }
            };
            var onFailure = function(error) {
                console.log(error);
            };
            var url = "/rooms";
            makeGetRequest(url, onSuccess, onFailure);
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
        userInfo = $('div.userInfo');
        roomsAction = $('.roomcreate_container');
        actionMenu = $('#cssmenu');

        joinRoomButton = $(".submit-roomjoin");
        playerHtmlTemplate = $(".players .player")[0].outerHTML;
        players = $(".players");
        players.html('');
        createRoomForm.hide();

        attachLoginHandler();
        attachLogoutHandler();
        attachSignupHandler();
        attachCreateRoomHandler();
        attachJoinRoomHandler();
    };

    // PUBLIC METHODS
    return {
        start: start
    };
})();
