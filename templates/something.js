window.onload = function(){
   
    function submit(){
        var name = document.getElementsByName('user_id')[0].value
        var password = document.getElementsByName('user_password')[0].value
        var email = document.getElementsByName('email_address')[0].value
        var button = document.getElementById('submit')
        var json = {
            'name' : name ,
            'password' : password ,
            'email' : email,
        }
        var req = new XMLHttpRequest();
        req.responseType = 'json';
        req.open('POST','http://localhost:5000/register',true)
        req.onload = function(){
            var jsonResponse = req.response;
        }
        req.send(json)
    }

    
}
