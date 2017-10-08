console.log("connected")
var checking = true

$(".callGroupContainer .phoneCall").css({'width':($(".phoneCall").width()+'px')});
$('.phoneCall').draggable({
     revert: "invalid",
     helper: "clone"
 });

    
$( ".callGroupContainer, #inactiveCallContainer" ).droppable({
    drop: function( event, ui ) {
            
        //remove hover from dropped box 
        $(this).removeClass('groupHover');

        //get info from dropped call box
        var origin = $(ui.draggable[0]).data('callgroup')
        var phoneNumber = $(ui.draggable[0]).data('phonenumber')
        var routing = $(this).data('roomid')


        console.log(origin, phoneNumber, routing)

        //determine routing of call
        //first get rid of false drops where same box was used
        if (origin != routing) {
            console.log("Hey this box MOVED!");

            //route call appropriately
            if (routing == 'inactiveRoom') {
                endCall (phoneNumber, origin)
            } else if (origin == 'inactiveRoom') {
                startCall(phoneNumber, routing, origin);
            } else {
                rerouteCall(phoneNumber, routing, origin);
            }

            //update the status of the call and move row by appending
            $(ui.draggable[0]).attr('data-callgroup',routing)
            $(ui.draggable).clone().appendTo(this);   

            //Make new item draggable
            $(this).children('.phoneCall').draggable({
                 revert: "invalid",
                 helper: "clone"
             });

            ui.draggable.remove();

        } else {
            console.log("Hey this box didn't move!")
        }
    },
    over: function (event, ui) {
        $(this).addClass('groupHover');
    },
    out: function(event, ui) {
        $(this).removeClass('groupHover');
    }
});

//this will probably phase out, and replace with front end JS loop that utilizes start call for proper groups
$('#startCalls').on('click', function(){
    console.log("start calls")
    var group = "musicRoom"
    // var group = "confRoom2"
    $.post( "/startCalls", { routing: $('#selectRouting').val() } )
        .done(function( res ) {
            checking = true;
            // checkCallStatus()
            console.log(res)
    });
});


function startCall (phoneNumber, routing, origin) {
    $.post( "/startCall", { phoneNumber: phoneNumber, routing: routing, origin: origin } )
        .done(function( res ) {
            console.log(res);
    });

}

function endCall (phoneNumber, origin) {
    $.post( "/endCall", { phoneNumber: phoneNumber, origin: origin } )
        .done(function( res ) {
            console.log(res);
    });
}

function rerouteCall(phoneNumber, routing, origin) {

    $.post( "/rerouteCall", { phoneNumber: phoneNumber, routing: routing, origin: origin } )
            .done(function( res ) {
                console.log(res);
    });
}




$('#endCalls').on('click', function(){
    console.log("end calls")
    $.post( "/endCalls", { routing: "test" } )
        .done(function( res ) {
            checking = false;
            // $('#contactRows').html(initialTableHtml)

    });
});


function checkCallStatus() {
    if (checking == true) {
        $.get( "/callsStatus").done(function( res ) {

            obj = JSON.parse(res)
            for (contact in obj.contacts) {

                name = obj.contacts[contact].name
                phoneNumber = obj.contacts[contact].phoneNumber
                callStatus = obj.contacts[contact].calls[obj.contacts[contact].calls.length - 1].callStatus

                rowsHTML.push(generateContactRowHTML(name, phoneNumber, callStatus));
                
            }

            htmlStr = rowsHTML.join()

            $('#contactRows').html('')
            $('#contactRows').html(htmlStr)

            setTimeout(checkCallStatus, 500)
        });
    }
} 
