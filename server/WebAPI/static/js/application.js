$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        $('#log').html(msg.number);
    });

});