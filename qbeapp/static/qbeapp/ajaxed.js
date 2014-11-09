$(document).ready(function() {
    
     $("body").append('<div id="loading_indicator">Loading...</div>');
     
     $("#loading_indicator").css({
        display:"none",
        margin:"0px",
        paddingLeft:"0px",
        paddingRight:"0px",
        paddingTop:"0px",
         paddingBottom:"0px",
         position:"absolute",
         right:"50%",
         top:"3px",
         width:"200px",
         height: "30px",
         border: "1px dotted #E6E65C",
         background: "#FFFF66"
     });

    $(document).ajaxStart(function() {
        $("#loading_indicator").show();
    }).ajaxStop(function() {
        $("#loading_indicator").hide();
    });

    $("#runbtn").click(function(event) {        
        $.post("/report/", $("#qbeform").serialize())
        .done(function(data){
            var report_data = $( data ).find( "#reporttbl" );
            $( "#reporttbl" ).empty().append(report_data);
        })
        .fail(function(data){
            $( "#reportfor_err" ).html("<div class='errorlist'>Report for is required field</div>");
        });
    });
})
    