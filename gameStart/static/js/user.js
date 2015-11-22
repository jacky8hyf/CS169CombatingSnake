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
    var msg;
    var reconn_msg;

    //pick room
    var pickRoomButton;
    var pickRoomForm;
    var cancelRoomButton;
    var roomList;

    var joinRoomButton;
    var roomSize = 8;
    var players;    // list of players inside the room
    var playerHtmlTemplate;

    // Handle player color
    var color_lookup = ['white', 'red', 'blue', 'orange', 'black', 'yellow', 'green', 'purple', 'pink', 'aqua'];
    var user_color_map = {};

    // Handle gameboard
    var nRows = 21;
    var nCols = 38;
    var old_snakes_state = {};   // list of the positions of all old snakes
    var old_foods = [];   // list of the positions of all old foods

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
    };

    /**
     * Add event handlers for submitting the create form.
     * @return {None}
     */
    var attachLoginHandler = function(e) {
        loginForm.on('click', '.submit-login', function(e) {
            e.preventDefault();
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
            e.preventDefault();

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
            e.preventDefault();
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
            };
            makePostRequest("/users/", user, onSuccessLogin, onFailure);
        });
    };

    var leaveRoomResult = function() {
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

    var attachLeaveRoomHandler = function(e) {
        $('div.game-start-leave').on('click','.submit-leave', function(e){
            e.preventDefault();

            var onSuccess = function(data) {
                inbox.send("quit");
                gameStarted = false;
                inbox.close();
                leaveRoomResult();
            };
            var onFailure = function(error) {
                console.log(error);
                leaveRoomResult(); // FIXME: BACKEND FAILURE ON LEAVE ROOM, NEED TO GO BACK TO CREATE ROOM PAGE FOR NOW
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
                inbox = new ReconnectingWebSocket(urlstr);
                var ts = Date.now();
                var hashStr = sessionId + ":" + userId + ":" + ts;
                var auth = sha256(hashStr);
                msg = "join " + JSON.stringify({userId:userId, ts:ts, auth:auth});
                reconn_msg = "reconn " + JSON.stringify({userId:userId, ts:ts, auth:auth});
                var i = 0;
                var notReceive = true;
                inbox.onopen = function(e){
                    if (i < 20) {
                        if(gameStarted == true){
                            inbox.send(reconn_msg);
                        }
                        else if(gameStarted == false){
                            inbox.send(msg);
                        }
                        i++;
                    }
                };

                inbox.onmessage = function(message) {
                    var data = message.data.match(/^(\w*)((\s+(.*?))|)$/);
                    var cmd = data[1];
                    var dict = data[4];
                    if (dict != undefined) {
                        dict = JSON.parse(dict);
                    }

                    //if (message.data.indexOf("err") != -1) {
                    if (cmd == 'error') {
                        return;
                    }
                    if (cmd == "start") {
                        removeFoods();
                        removeSnakes();
                        alert("Starting Game");
                        gameStarted = true;
                        old_foods = [];
                        old_snakes_state = {};
                        return;
                    } else if (cmd == "room") {
                        notReceive = false;
                        players.html('');   //clear players list
                        var player = $(playerHtmlTemplate);
                        player.attr("id", dict.creator.userId);  // add id so we can update health field later
                        player.find('.name').text(dict.creator.nickname);
                        players.append(player);
                        user_color_map[dict.creator.userId] = color_lookup[players.size()];
                        player.addClass(color_lookup[players.size()]);

                        for(i = 0; i < dict.members.length && i < roomSize - 1; i++){
                            var player = $(playerHtmlTemplate);
                            player.attr("id", dict.members[i].userId);  // add id so we can update health field later
                            player.find('.name').text(dict.members[i].nickname);
                            user_color_map[dict.members[i].userId] = color_lookup[i + 2];
                            player.addClass(color_lookup[i + 2]);
                            players.append(player);
                        }
                    } else if (cmd == "g") { //game command
                        // Place holder for getting the snakes' positions from the server
                        drawSnakes(dict); // draw out all snakes
                        drawFoods(dict["_food"]); // draw out all foods
                        updateHealth(dict); // update health field
                    } else if (cmd == "end") {
                        if (dict == undefined) {
                            alert("Draw");
                        } else {
                            alert("Winner is " + dict.winner.nickname); // print the nickname of the winner player
                        }
                        gameStarted = false;
                    }
                };
            };
            var onFailure = function(error) {
                console.log(error);
            };
            var url = "/rooms";
            makePostRequest(url, room, onSuccess, onFailure);
        });
    };

    function roomListShowingHelper(e) {
        e.preventDefault();
        var onSuccess = function (data) {
            if (data.rooms.length < 1) {
                alert("No room available! Please create a room instead!");
            }
            else {//get all room id and put into roomList
                //roomList = [];
                setBoard();
                roomList = data.rooms;  // global roomList to track all available room objects
                var myroomlist = $('#listofrooms');
                myroomlist.empty();
                for (room in data.rooms) {
                    //roomList.push(room.roomId);
                    try {
                        console.log(data.rooms[room]);
                        var current_room = data.rooms[room];
                        var members = "";
                        for (var i = 0; current_room.members.length; i++) {
                            members += current_room.members[i].nickname + " ";
                        }
                        myroomlist.append($('<option></option>').val(data.rooms[room].roomId).html(current_room.roomId + ": creator: "
                            + current_room.creator.nickname + ", members: " + members));

                    } catch (err) {
                        console.log(err);
                    }
                    //myroomlist.append($('<option></option>').val(room).html(data.rooms[room].roomId));  // use val to track index of room
                    //$('<option></option>').addClass(data.rooms[room].roomId);  //  set class name as room id
                }
                //add to listbox
                actionMenu.hide();
                roomsAction.hide();
                $('.logout').hide();
                pickRoomForm.show();
                //attachAvailableRoomOnClickHandler();
            }

        }
        var onFailure = function (error) {
            console.log(error);
        };
        //send get request to get a rooms list
        var url = "/rooms?creator-profile=true&members=true&member-profile=true";
        makeGetRequest(url, onSuccess, onFailure);
    }

    var attachPickRoomHandler = function(e){
        $('body').on('click','.join_specific_room', function(e){
            roomListShowingHelper(e);
        });
    };

    var attachRefreshRoomListHandler = function(e){
        $('body').on('click','.refresh_rooms', function(e){
            roomListShowingHelper(e);
        });
    };

    //var attachAvailableRoomOnClickHandler = function(e){
    //    for (room in roomList){
    //        $('body').on('click', '#listofrooms option[value='+ room +']', function(e){
    //            //e.preventDefault();
    //            joinAvailableRoom(roomList[e.target.value]);
    //        });
    //    }
    //};
    var attachAvailableRoomOnClickHandler = function(e){
        $('body').on('click', '#listofrooms',function(e){
            var id = $('#listofrooms').val();
            console.log(id);
            for (room in roomList){
                if(roomList[room].roomId == id){
                    console.log('room is:');
                    console.log(roomList[room].roomId);
                    joinAvailableRoom(roomList[room]);
                }
            }
        });
    };

    function joinAvailableRoom(available_room) {
        roomId = available_room.roomId;
        var urlstr = "wss://combating-snake-chat-backend.herokuapp.com/rooms/" + available_room.roomId;
        inbox = new ReconnectingWebSocket(urlstr);
        //inbox = new WebSocket(urlstr);
        var ts = Date.now();
        var hashStr = sessionId + ":" + userId + ":" + ts;
        var auth = sha256(hashStr);
        msg = "join " + JSON.stringify({userId: userId, ts: ts, auth: auth});
        reconn_msg = "reconn " + JSON.stringify({userId: userId, ts: ts, auth: auth});
        //send hello message
        var i = 0;
        var notReceive = true;
        inbox.onopen = function (e) {
            if (i < 20) {
                if (gameStarted == true) {
                    inbox.send(reconn_msg);
                }
                else {
                    inbox.send(msg);
                }
                i++;
            }
        };
        inbox.onmessage = function (message) {
            var data = message.data.match(/^(\w*)((\s+(.*?))|)$/);
            var cmd = data[1];
            var dict = data[4];
            if (dict != undefined) {
                dict = JSON.parse(dict);
            }

            //if (message.data.indexOf("err") != -1) {
            if (cmd == 'error') {
                return;
            }
            if (cmd == "start") {
                removeFoods();
                removeSnakes();
                alert("Starting Game");
                gameStarted = true;
                old_foods = [];
                old_snakes_state = {};
                return;
            } else if (cmd == "g") { //game command
                // Place holder for getting the snakes' positions from the server
                drawSnakes(dict); // draw out all snakes
                drawFoods(dict["_food"]); // draw out all foods
                updateHealth(dict); // update health field
            } else if (cmd == "end") {
                if (dict == undefined) {
                    alert("Draw");
                } else {
                    alert("Winner is " + dict.winner.nickname); // print the nickname of the winner player
                }
                gameStarted = false;
            } else if (cmd == "room") {
                notReceive = false;
                //var roominfo = JSON.parse(message.data.substring(message.data.indexOf(" ")));
                var roominfo = dict;
                if (roominfo.members.length > roomSize - 1) {
                    return;
                }

                createRoomForm.find('.room_id').text("Room " + available_room.roomId);
                createRoomForm.show();
                actionMenu.hide();
                roomsAction.hide();
                pickRoomForm.hide();
                $('.logout').hide();

                players.html('');
                var player = $(playerHtmlTemplate);
                player.attr("id", dict.creator.userId);  // add id so we can update health field later
                player.find('.name').text(available_room.creator.nickname);
                user_color_map[dict.creator.userId] = color_lookup[players.size()];
                player.addClass(color_lookup[1]);
                players.append(player);

                //add room_members
                for (i = 0; i < roominfo.members.length && i < roomSize - 1; i++) {
                    var player = $(playerHtmlTemplate);
                    player.attr("id", dict.members[i].userId);  // add id so we can update health field later
                    player.find('.name').text(roominfo.members[i].nickname);
                    user_color_map[dict.members[i].userId] = color_lookup[i + 2];
                    player.addClass(color_lookup[i + 2]);
                    players.append(player);
                }
            }
        };
        $('#cssmenu').hide();
    }

    var attachJoinRoomHandler = function(e) {
        $('body').on('click','.submit-roomjoin', function(e){
            e.preventDefault();
            var onSuccess = function(data) {
                setBoard();
                //find available room for joining
                var available_room;
                for (room in data.rooms){
                    if(!room.hasOwnProperty("members") || (room.members.length < roomSize)){
                        available_room = data.rooms[room];
                        //break; // FIXME: COMMENT THIS OUT TO JOIN THE LATEST ROOM, NOT THE OLDEST ROOM
                    }
                }
                if(available_room != null){
                    joinAvailableRoom(available_room);
                } else{
                    alert("No room available now. Please create a new room!");
                }
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
            gameStarted = true;
        });
    };

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
                    // msg = "l"; //FIXME: FIND OUT WHY THE DIRECTION IS OPPOSITE
                    msg = "r";
                    break;
                case 37:      // RIGHT: 39
                    // msg = "r";
                    msg = "l";
                    break;
            }
            inbox.send(msg);
        }
    }

    var updateHealth = function(snakes) {
        for (var key in snakes){
            if (key != '_food') {
                var snake_body = snakes[key];
                $("#"+ key).find('.health').text(10*snake_body.length);
            }
        }
    };

    var drawSnakes = function(snakes) {
        removeSnakes();
        for (var key in snakes){
            if (key != '_food') {
                var snake_body = snakes[key];
                for (var i = 0; i < snake_body.length; i++) {
                    id = "r" + snake_body[i][0] + "c" + snake_body[i][1];
                    $("#" + id).addClass(user_color_map[key]);
                }
            }
        }
        old_snakes_state = snakes;
    };

    var removeSnakes = function() {
        for (var key in old_snakes_state){
            var snake_body = old_snakes_state[key];
            for (var i = 0; i < snake_body.length; i++) {
                id = "r" + snake_body[i][0] + "c" + snake_body[i][1];
                $("#" + id).removeClass(user_color_map[key]);
            }
        }
    };

    /**
     * Draw all foods onto the board.
     * @param foods : new foods
     */
    var drawFoods = function(foods) {
        removeFoods();
        for (var i = 0; i < foods.length; i++) {
            var food = foods[i];
            id = "r" + food[0] + "c" + food[1];
            $("#" + id).addClass("food");
        }
        old_foods = foods;
    };

    /**
     * Remove all old foods
     */
    var removeFoods = function() {
        for (var i = 0; i < old_foods.length; i++){
            var food = old_foods[i];
            id = "r" + food[0] + "c" + food[1];
            $("#" + id).removeClass("food");
        }
    };


    var setBoard = function() {
        var table = "<table>";
        for(var i=0; i < nRows; i ++) {
            table += "<tr>";
            for(var j=0; j < nCols; j ++) {
                id = "r" + i + "c" + j;
                table += "<td><div class='"+"cell"+ "' id='" + id +"'></div></td>";
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
        pickRoomForm = $(".pick_room");
        createRoomButton = $(".create_button");
        userInfo = $('div.userInfo');
        roomsAction = $('.roomcreate_container');
        actionMenu = $('#cssmenu');

        joinRoomButton = $(".submit-roomjoin");
        pickRoomButton = $(".join_specific_room");
        cancelRoomButton = $(".cancel_room_pick");
        playerHtmlTemplate = $(".players .player")[0].outerHTML;
        players = $(".players");
        players.html('');
        createRoomForm.hide();
        pickRoomForm.hide();

        attachLoginHandler();
        attachLogoutHandler();
        attachSignupHandler();
        attachCreateRoomHandler();
        attachJoinRoomHandler();
        attachPickRoomHandler();
        attachRefreshRoomListHandler();
        attachLeaveRoomHandler();
        attachStartGame();
        attachAvailableRoomOnClickHandler();
    };

    // PUBLIC METHODS
    return {
        start: start,
        sendKeyStroke: sendKeyStroke
    };
})();
