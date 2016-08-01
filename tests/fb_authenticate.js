console.log("You've entered the FB Authenticate script like you're supposed to");


window.fbAsyncInit = function(){
	FB.init({
		appId	: '1060269840728852',
		xfbml	: true,
		version	: 'v2.7'
	});
};

(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) {return;}
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

window.test_oauth = function(){
	FB.login(function(response){
		if (response.authResponse) {
			var access_token = FB.getAuthResponse()['accessToken'];
			var user_id = FB.getAuthResponse()['userID'];
			
			var request = require("request");

			console.log('Access Token = ' + access_token);
			console.log('User ID = ' + user_id);

			var keys = JSON.stringify({'oauth_token' : access_token, 'user_id' : user_id });

			console.log(keys);

			request({
		        url:'http://spencer.mybluemix.net/piroute',
						body: keys,
		        method: 'POST',
		        headers: {
		          'Content-Type': 'application/json'
		        }
		      }, function(err,res,body){
		          if(!err && res.statusCode == 200){
		            console.log(body);
		         }
        });
		} else {
			console.log('User cancelled login or did not fully authorize.');
		}
	}, {scope: 'email, public_profile, user_friends'});
}

