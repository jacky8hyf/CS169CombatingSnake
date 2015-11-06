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
    var roomId;

    // Handle room requests
    var createRoomForm;
    var createRoomButton;

    var joinRoomButton;
    var roomSize = 8;
    var players;    // list of players inside the room
    var playerHtmlTemplate;

    // Handle player color
    var color_lookup = ['white', 'red', 'blue', 'orange', 'black']

    // Handle gameboard
    var nRows = 21;
    var nCols = 38;
    var old_snakes_state = {};   // list of the positions of all old snakes

    // WebSocket logics
    var inbox = null;
    var gameStarted = false;

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
                'X-Snake-Session-Id': sessionId,
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
                'X-Snake-Session-Id': sessionId,
            },
            //data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };

    var onSuccessLogin = function(data) {
        is_login = true;
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
                is_login = false;
                loginForm.show();
                userInfo.hide();
                actionMenu.show();
                createRoomForm.hide();
                roomsAction.hide();
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

    var attachLeaveRoomHandler = function(e) {
        $('div.game-start-leave').on('click','.submit-leave', function(e){
            e.preventDefault()
            var onSuccess = function(data) {
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

                createRoomForm.hide();
                loginForm.hide();
                signupForm.hide();
                roomsAction.show();
                actionMenu.show();
                $('.logout').show();
                players.html('');
            };
            var onFailure = function(error) {
                console.log(error);
            };
            //DELETE /rooms/:roomId/members/:memberId
            var url = "/rooms/" + roomId + "/members/" + userId;
            makeDeleteRequest(url, onSuccess, onFailure);
        });
    };


    var attachCreateRoomHandler = function(e) {
        $('body').on('click','.create_button', function(e){
			e.preventDefault();
            var room = {};
            var onSuccess = function(data) {
                setBoard();
                createRoomForm.find(".room_id").text('Room ' + data.roomId);
                createRoomForm.show();
                actionMenu.hide();
                roomsAction.hide();
                $('.logout').hide();

                roomId = data.roomId;
                //create a socket connection to server here and remove polling block
                var urlstr = "wss://combating-snake-chat-backend.herokuapp.com/rooms/" + roomId;
                var inbox = new ReconnectingWebSocket(urlstr);
                var ts = Date.now();
                var hashStr = sessionId + ":" + userId + ":" + ts;
                var auth = sha256(hashStr);
                var msg = "join " + JSON.stringify({userId:userId, ts:ts, auth:auth});
                inbox.onopen = function(e){
                    inbox.send(msg);
                }

                inbox.onmessage = function(message) {
                    console.log(message.data);
                    var roominfo = JSON.parse(message.data.substring(message.data.indexOf(" ")));

                    players.html('');   //clear players list
                    var player = $(playerHtmlTemplate);
                    player.find('.name').text(roominfo.creator.nickname);
                    players.append(player);
                    player.addClass(color_lookup[players.size()]);

                    for(i = 0; i < roominfo.members.length, i < 7; i++){
                        var player = $(playerHtmlTemplate);
                        player.find('.name').text(roominfo.members[i].nickname);
                        players.append(player);
                    }
                }
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
            e.preventDefault();
            var onSuccess = function(data) {
                //find available room for joining
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
                if(available_room != null){
                    var urlstr = "wss://combating-snake-chat-backend.herokuapp.com/rooms/" + available_room.roomId;
                    var inbox = new ReconnectingWebSocket(urlstr);
                    var ts = Date.now();
                    var hashStr = sessionId + ":" + userId + ":" + ts;
                    var auth = sha256(hashStr);
                    var msg = "join " + JSON.stringify({userId:userId, ts:ts, auth:auth});
                    //send hello message
                    inbox.onopen = function(e){
                        inbox.send(msg);
                    }

                    inbox.onmessage = function(message) {
                        console.log(message.data);
                        var roominfo = JSON.parse(message.data.substring(message.data.indexOf(" ")));

                        if(roominfo.members.length > roomSize-1){
                            return ;
                        }

                        createRoomForm.find('.room_id').text("Room " + available_room.roomId);
                        var player = $(playerHtmlTemplate);
                        player.find('.name').text(available_room.creator.nickname);
                        player.addClass(color_lookup[1]);
                        players.append(player);

                        //add room_members
                        for(i=0; i< roominfo.members.length, i < roomSize - 1; i++){
                            var player = $(playerHtmlTemplate);
                            player.find('.name').text(roominfo.members[i].nickname);
                            player.addClass(color_lookup[i+2]);
                            players.append(player);
                        }
                    }
                }

                $('#cssmenu').hide();
                actionMenu.show();
            };
            var onFailure = function(error) {
                console.log(error);
            };
            var url = "/rooms?creator-profile=true&members=true&member-profile=true";
            makeGetRequest(url, onSuccess, onFailure);
        });
    };

    // Send "start" to webSocket when user hit "StartGame"
    var attachStartGame = function(e) {
        $('body').on('click','.submit-start', function(e){
            e.preventDefault();
            if (inbox != null) {
                inbox.send("start");
            }
            // Place holder for getting the snakes' positions from the server
            var snakes = {1: [[1,2], [1,3], [1, 4]], 2: [[3,4], [4,4], [5,4]]};
            drawSnakes(snakes);     // draw out all snakes
        });
    }

    var sendKeyStroke = function(e) {
        if (inbox != null && gameStarted) {
            var msg;
            switch(e.keyCode) {
                case 38:      // UP: 38
                    msg = "u";
                    break;
                case 40:      // DOWN: 40
                    msg = "d";
                    break;
                case 39:      // LEFT: 37
                    msg = "l";
                    break;
                case 37:      // RIGHT: 39
                    msg = "r";
                    break;
            }
            inbox.send(msg);
        }
    }

    var drawSnakes = function(snakes) {
        removeSnakes();
        for (var key in snakes){
            var snake_body = snakes[key];
            for (var i = 0; i < snake_body.length; i++) {
                id = "r" + snake_body[i][0] + "c" + snake_body[i][1];
                $("#" + id).toggleClass(color_lookup[key]);
            }
        }
        old_snakes_state = snakes;
    };

    var removeSnakes = function() {
        for (var key in old_snakes_state){
            var snake_body = old_snakes_state[key];
            for (var i = 0; i < snake_body.length; i++) {
                id = "r" + snake_body[i][0] + "c" + snake_body[i][1];
                $("#" + id).toggleClass(color_lookup[key]);
            }
        }
    };

    var setBoard = function() {
        var table = "<table>";
        for(var i=0; i < nRows; i ++) {
            table += "<tr>";
            for(var j=0; j < nCols; j ++) {
                var cellClass = "cell";
                id = "r" + i + "c" + j;
                table += "<td><div class='"+cellClass+ "' id='" + id +"'></div></td>";
            }
            table += "</tr>";
        }
        $('.gameboard').html(table);
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
        attachLeaveRoomHandler();
    };

    // PUBLIC METHODS
    return {
        start: start
    };
})();
