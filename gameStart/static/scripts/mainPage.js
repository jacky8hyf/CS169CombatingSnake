

var Frontpage = (function() {
	var gameRule;
	var intro;
	var login;
	var leaderboard;
	var signup;
	var fadeInTime = 1000;
	var userInfo;
	var roomAction;
	var createRoom;

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
			$('.login_container').fadeIn(fadeInTime);
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
			$('.intro').fadeIn(1000);
		});
	};
	var attachLeaderboardHandler = function(e){
		$('.leader-button').click(function(e){
			e.preventDefault();
			hideAll();
			$('.leaderboard').fadeIn(1000);
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