$(document).ready(function(){
    $("#show-diff-group button").on("click", function(){
        $("input[name=\"show_diff\"]").val($(this).val());
    });
});
