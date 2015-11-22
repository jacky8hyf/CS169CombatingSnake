

var Frontpage = (function() {
	var gameRule;
	var intro;
	var login;
	var leaderboard;
	var signup;
	var fadeInTime = 500;
	var userInfo;
	var roomAction;
	var createRoom;

	//leaderboard
	var winner_table;
	var makeGetRequest = function(url, onSuccess, onFailure) {
        $.ajax({
            type: 'GET',
            url: url,
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };


	var hideAll = function() {
		gameRule.hide();
		intro.hide();
		login.hide();
		leaderboard.hide();
		signup.hide();
		roomAction.hide();
		createRoom.hide();
	};

	var attachHomeHandler = function(e){
		$('.active').click(function(e){
			e.preventDefault();
			hideAll();
			if(is_login) {
				roomAction.fadeIn(fadeInTime);
			} else {
				$('.login_container').fadeIn(fadeInTime);
			}
		});
	};
	var attachGameRuleHandler = function(e) {
		$('.rule-button').click(function(e){
			e.preventDefault();
			hideAll();
			$('.gamerule').fadeIn(1000);
		});
	};
	var attachIntroductionHandler = function(e){
		$('.intro-button').click(function(e){
			e.preventDefault();
			hideAll();
			$('.intro').fadeIn(fadeInTime);
		});
	};

//	GET /users/scores?limit=3&offset=0&profile=true&scores=true Example Output:
//[
//{"userId":"2e98dd","nickname":"jacky","numgames":1,"numwin":0}, {"userId":"2e98df","nickname":"Krist","numgames":4,"numwin":2}, {"userId":"2e98df","nickname":"Zoe","numgames":1,"numwin":0}
//]
	var attachLeaderboardHandler = function(e){
		$('.leader-button').click(function(e){
			e.preventDefault();
			$('.winner_table').html('');	//clear the board
			$('.winner_table').append('<tr><th>Winner Name</th><th>Number of plays</th><th>Number of wins</th></tr>');
			var onSuccess = function(data){
				if(data.users.length > 0){	
					for (winner in data.users){
						var id = data.users[winner].userId;
						var numgames = data.users[winner].numgames;
						var numwins = data.users[winner].numwin;
						$('.winner_table').append('<tr><td>' + id + '</td><td>' + numgames + '</td><td>' + numwins + '</td></tr>');
					}

				}
				

			};

			var onFailure = function(error) {
                console.log(error);
            };
			hideAll();
			$('.leaderboard').fadeIn(fadeInTime);
			//default is getting 20 winners
			var url = "/users/scores?profile=true&scores=true";
            makeGetRequest(url, onSuccess, onFailure);
		});
	};
	var attachStartGameHandler = function(e){
		$('.gamestart-button').click(function(e){
			e.preventDefault();
			hideAll();
			$('.login_container').fadeIn(fadeInTime);
		});
	};
	var attachSignUpHandler = function(e){
		$('.text-center').click(function(e){
			e.preventDefault();
			$('.login_container').hide();
			$('.signup_container').fadeIn(100);
		});
	};

	var start = function(){
		gameRule = $('.gamerule');
		intro = $('.intro');
		login = $('.login_container');
		leaderboard = $('.leaderboard');
		winner_table = $('.winner_table');
		signup = $('.signup_container');
		roomAction = $('.roomcreate_container');
		createRoom = $('.create_room');
		$('.userInfo').hide();
		hideAll();
		$('.logo').hide();
		$('#cssmenu').hide();
		$('.logo').fadeToggle(fadeInTime);
		$('#cssmenu').fadeIn(fadeInTime);
		$('.login_container').fadeIn(fadeInTime);
		attachGameRuleHandler();
		attachHomeHandler();
		attachIntroductionHandler();
		attachLeaderboardHandler();
		attachStartGameHandler();
		attachSignUpHandler();
	};

	return {
		start:start
	};
})();