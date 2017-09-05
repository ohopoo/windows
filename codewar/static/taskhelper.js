/**
 * Created by TuDinhTan on 5/26/17.
 */
$(document).ready(function ()  {
   // When we're using HTTPS, use WSS too.
   var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
   var ws_path = ws_scheme + '://' + window.location.host + '/tasks';
   console.log("Connecting to " + ws_path);
   var socket = new ReconnectingWebSocket(ws_path);
   socket.onmessage = function(message) {
   //    console.log("Got message: " + message.data);
       var data = JSON.parse(message.data);
       var outputdiv = document.getElementById("iframeResult");
       var state = document.getElementById("stateResult");
        if(data.state=="Wait")
        {
            outputdiv.innerHTML ="Console:<br/>"
        }
        if(data.message)
        {
            outputdiv.innerHTML = outputdiv.innerHTML+'<p>'+data.message.replace(/(?:\r\n|\r|\n)/g, '<br />');+"</p>";
        }

        state.innerHTML = data.state +" ";
        if (data.color){
            state.innerHTML ='<span style="color: red;!important;">'+data.state+'</span>';
        }
   };
   socket.onclose = function(e) {
    var state = document.getElementById("stateResult");
    state.innerHTML ='<span style="color: red;!important;">Disconnected! </span>';
};
   $("#runcode").on("click", function(event) {
       var message = {
           action: "compile_run",
           data: {
               'editor':editor.getValue(),
               'question_id':$('#question_id').val(),
               'language':$('#language').val()
           }
       };
       socket.send(JSON.stringify(message));
       return false;
   });
});