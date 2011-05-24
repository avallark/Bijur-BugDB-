function init ( )
{

  user_id = 0;

  timeDisplay = document.createTextNode ( "" );
  document.getElementById("clock").appendChild ( timeDisplay );
  
  nameDisplay = document.createTextNode ( "" );
  document.getElementById("displayMessage").appendChild ( nameDisplay );
      
  i = 0;
  bb = 0;
      
     FB.init({
     appId  : '104595322956808',
     status : true, // check login status
     cookie : true, // enable cookies to allow the server to access the session
     xfbml  : true  // parse XFBML
     });
     
     FB.getLoginStatus(function(response) {
     if (response.session) {
        // get the uid
        user_id = response.session.uid;
        alert(user_id);
     } else {
         top.location.href= {{auth_url}}
         alert(auth_url);
     }
     });

     var query = FB.Data.query('select name, uid,email from user where uid={0}',
     user_id);
     query.wait(function(rows) {
     name = rows[0].name;
     email = rows[0].email;
     alert(name);
     });

}

 
function updateClock ()
{
  
  i = i + 1;
  //currentCost = Math.round((i * num * (costph/3600))*100)/100;

  var currentTimeString = i/100;
 
  document.getElementById("clock").firstChild.nodeValue = currentTimeString;
}


function do_submit(){

       
       clearInterval ( bb );

       var id = user_id;
       if ((i/100) == 10.00){
       alert(name + '!!! You did it!!');
       }
       else {
       alert('Sorry '+name+', better luck next time ;(');
       }
       
       //display_message(, '122');

}
 
function restart_clock(){
       window.location.reload();
}

function get_data(id){
       
FB.api(
       {
       method: 'fql.query',
       query: 'SELECT name,email FROM user WHERE uid='+id
       },       
       function(response) {
       var result = [];
       result[0] = response[0].name;
       result[1] = response[0].email;
       }
       );
       
       return result;
}


function display_message(name, email, score){
        document.getElementById("displayMessage").firstChild.nodeValue = name+' stopped the clock at '+score+' - '+email;
}