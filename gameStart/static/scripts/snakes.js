var Frontpage = (function() {
	var attachHomeHandler = function(e){
		$('.active').click(function(e){
			e.preventDefault();
			$('.gamerule').fadeOut(1000);
			$('.intro').fadeOut(1000);
			$('.login_container').fadeOut(1000);
			$('.leaderboard').fadeOut(1000);
			$('.signup_container').hide();
		});
	};
	var attachGameRuleHandler = function(e) {
		$('.rule-button').click(function(e){
			e.preventDefault();
			$('.leaderboard').hide();
			$('.intro').hide();
			$('.login_container').hide();
			$('.signup_container').hide();
			$('.gamerule').fadeIn(1000);
		});
	};
	var attachIntroductionHandler = function(e){
		$('.intro-button').click(function(e){
			e.preventDefault();
			$('.gamerule').hide();
			$('.leaderboard').hide();
			$('.login_container').hide();
			$('.signup_container').hide();
			$('.intro').fadeIn(1000);
		});
	};
	var attachLeaderboardHandler = function(e){
		$('.leader-button').click(function(e){
			e.preventDefault();
			$('.gamerule').hide();
			$('.intro').hide();
			$('.login_container').hide();
			$('.signup_container').hide();
			$('.leaderboard').fadeIn(1000);
		});
	};
	var attachStartGameHandler = function(e){
		$('.gamestart-button').click(function(e){
			e.preventDefault();
			$('.gamerule').hide();
			$('.intro').hide();
			$('.leaderboard').hide();
			$('.signup_container').hide();
			$('.login_container').fadeIn(1000);
		});
	};
	var attachSignUpHandler = function(e){
		$('.text-center').click(function(e){
			e.preventDefault();
			$('.login_container').hide();
			$('.signup_container').fadeIn(1000);
		});
	};
	var start = function(){
		$('.logo').hide();
		$('#cssmenu').hide();
		$('.logo').fadeToggle(1000);
		$('#cssmenu').fadeIn(2000);
		$('.gamerule').hide();
		$('.intro').hide();
		$('.signup_container').hide();
		$('.leaderboard').hide();
		$('.login_container').hide();
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