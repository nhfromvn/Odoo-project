window.fbAsyncInit = function () {
    FB.init({
        appId: '580656120523395',
        cookie: true,
        xfbml: true,
        version: 'v16.0'
    });
    FB.AppEvents.logPageView();
    FB.getLoginStatus(function (response) {
        // statusChangeCallback(response);
        console.log(response)
    });
    FB.api('/me', function (response) {
        console.log(JSON.stringify(response));
    });

    function checkLoginState() {
        FB.getLoginStatus(function (response) {
            // statusChangeCallback(response);
        }, scope = 'public_profile,email');
    }

    FB.api('me', {fields: 'id,first_name,last_name'}, function (respone) {
        console.log(respone)
        document.getElementById('user_data').innerHTML = `<div>${respone.first_name}</div>
<div>${respone.last_name}</div>`
    })
};

(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {
        return;
    }
    js = d.createElement(s);
    js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));