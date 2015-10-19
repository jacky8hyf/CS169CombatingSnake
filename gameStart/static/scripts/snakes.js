var Frontpage = (function() {
	var attachHomeHandler = function(e){
		$('.active').click(function(e){
			e.preventDefault();
			$('.gamerule').hide();
			$('.intro').hide();
			$('.leaderboard').hide();
		});
	};
	var attachGameRuleHandler = function(e) {
		$('.rule-button').click(function(e){
			e.preventDefault();
			$('.leaderboard').hide();
			$('.intro').hide();
			$('.gamerule').show();
		});
	};
	var attachIntroductionHandler = function(e){
		$('.intro-button').click(function(e){
			e.preventDefault();
			$('.gamerule').hide();
			$('.leaderboard').hide();
			$('.intro').show();
		});
	};
	var attachLeaderboardHandler = function(e){
		$('.leader-button').click(function(e){
			e.preventDefault();
			$('.gamerule').hide();
			$('.intro').hide();
			$('.leaderboard').show();
		});
	};
	var start = function(){
		$('.gamerule').hide();
		$('.intro').hide();
		$('.leaderboard').hide();
		attachGameRuleHandler();
		attachHomeHandler();
		attachIntroductionHandler();
		attachLeaderboardHandler();
	};

	return {
		start:start
	};
})();