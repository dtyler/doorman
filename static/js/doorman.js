function setupHandlers(action_map) {
    $("button[id^=submit]").click(function() {
        console.log("you clicked submit");
    });
    $("button[id^=delete]").click(function() {
        console.log("you clicked delete");
    });
    $("input[id^=new_add_btn]").attr('disabled','disabled');
    $("input[id^=new_name], input[id^=new_keycode]").keyup(function(eventObject) {
            var code_id = eventObject.target.id;
            var code_suffix = code_id.substring(code_id.indexOf("-")+1);
            if( $("#new_name-"+code_suffix).val().trim() != "" && $("#new_keycode-"+code_suffix).val().trim() != "") { 
                $("#new_add_btn-"+code_suffix).removeAttr('disabled');
            } else {
                $("#new_add_btn-"+code_suffix).attr('disabled','disabled');
            }
    });
    $("input[id^=name-], input[id^=keyword]").keyup(function(eventObject) {
            var code_id = eventObject.target.id;
            var code_suffix = code_id.substring(code_id.indexOf("-")+1);
            $("#submit-"+code_suffix).removeAttr('disabled');
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
                    },
                    "text"
                 );
        }
        setupHandlers(action_map);
    }
}
