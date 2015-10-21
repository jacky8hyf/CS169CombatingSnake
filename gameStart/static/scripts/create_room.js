
var Room = (function(){
	var form;
	var button;
	var apiUrl = 'https://shielded-hollows-7501.herokuapp.com'; 
	/**
    * HTTP GET request 
    * @param  {string}   url       URL path, e.g. "/api/smiles"
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
     * HTTP POST request
     * @param  {string}   url       URL path, e.g. "/api/smiles"
     * @param  {Object}   data      JSON data to send in request body
     * @param  {function} onSuccess   callback method to execute upon request success (200 status)
     * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
     * @return {None}
     */
    var makePostRequest = function(url, data, onSuccess, onFailure) {
        $.ajax({
            type: 'POST',
            url: apiUrl + url,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };


	var clickHandler = function(){
		$('body').on('click','.create_button',function(){
			

			var room = {};
			var onSuccess = function(data) {
                
             /*   recommend added 1 field: status = 1: success, -1: fail
                add: best_score field to user:
                add:picture to user
                and change original status to: room_status
				POST /rooms
				Input: {}
				Output: {"roomId":"sheZs8w34","capacity":8,"status":"waiting"
				"creator":{"userId":"2s98dD","nickname":"jacky"},
				"members":[]}/*/
                if(data.status == 1){
                	form.find(".room_id").text('Room' + data.roomId);
					form.find(".player .name").text(data.creator.nickname);
                	form.show();
					button.hide();
                    $('#cssmenu').hide();
                }
                else{
                    console.error(data.errors);
                }
                
            };
            var onFailure = function() { 
                console.error('create room fails'); 
            };
            var url = "/rooms";
            makePostRequest(url, room, onSuccess, onFailure);
            /*		id = 10;
					form.find(".room_id").text("new room"+id);
                    form.fadeIn("slow","linear");
                	//form.show();
					button.hide();*/
                    
			
		});
	};
	var start = function(){
		form = $(".create_room");
        button = $(".create_button");
		form.hide();
		clickHandler();
	};

	return {
        start: start
    };

})();