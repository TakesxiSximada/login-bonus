// -*- coding: utf-8 -*-
setInterval(function (){
    $.ajax({
        type: "GET",
        url: "/api/data",
        data: "device_code=1015f6a",  // A
        dataType: 'JSON',
        success: function(msg){
            var point = document.querySelector('#point-a');
            console.log( "Data Saved: " + msg );
            $(point).text(msg.count);
        },
        error: function (err){
            console.log('nga');
        }
    });
    $.ajax({
        type: "GET",
        url: "/api/data",
        data: "device_code=1015fa8",  // B
        dataType: 'JSON',
        success: function(msg){
            var point = document.querySelector('#point-a');
            console.log( "Data Saved: " + msg );
            $(point).text(msg.count);
        },
        error: function (err){
            console.log('ngb');
        }
    });
}, 1000);
