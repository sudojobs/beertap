$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/t02test');
    var numbers_received = [];

    socket.on('t02number', function(msg) {
        console.log("Received numbers" + msg.tap1 + msg.tap2);
        $('#tap1').html(msg.tap1);
        $('#tap2').html(msg.tap2);        
    });

});
