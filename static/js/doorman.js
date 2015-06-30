function setupHandlers() {
    $("button[id^=submit]").click(function() {
        console.log("you clicked submit");
    });
    $("button[id^=delete]").click(function() {
        console.log("you clicked delete");
    });
    $("input[id^=new_add_btn]").attr('disabled','disabled');
    $("form input[id^=name], input[id^=keycode]").keyup(function(eventObject) {
            var code_id = eventObject.target.id;
            var code_suffix = code_id.substring(code_id.indexOf("-")+1);
            if( $("#name").val().trim() != "" && $("#keycode").val().trim() != "") { 
                $("#new_add_btn").removeAttr('disabled');
            } else {
                $("#new_add_btn").attr('disabled','disabled');
            }
    });
    $("#codeListTargetDiv input[id^=name-], input[id^=keycode-]").keyup(function(eventObject) {
            var code_id = eventObject.target.id;
            var code_suffix = code_id.substring(code_id.indexOf("-")+1);
            $("#submit-"+code_suffix).removeAttr('disabled');
    });
    $('#new_add_btn').click( function() {
        var newName = $("#name").val().trim();
        var newKeycode = $("#keycode").val().trim();
        $.post( '/code',
            JSON.stringify({
                name: newName,
                keycode: newKeycode
            }),
            function success(data) { 
                console.log("yay!");
            }
        );
        return false;
    });
}

function buildCodeListHTML(action_map) {
    console.log(action_map);
    if(action_map && action_map.length && action_map.length > 0) {
        for(var i = 0; i < action_map.length; i++) {
            $.get(
                    "/codeinfo/" + action_map[i],
                    function(data) {
                        $("#codeListTargetDiv").append(data);
                        setupHandlers();
                    },
                    "text"
            );
        }
    }
}
