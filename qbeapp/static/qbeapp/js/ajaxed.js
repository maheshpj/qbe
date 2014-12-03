$(document).ready(function () {

    $("body").append('<div id="loading_indicator">Loading...</div>');

    $("#loading_indicator").css({
        display: "none",
        margin: "0px",
        paddingLeft: "0px",
        paddingRight: "0px",
        paddingTop: "0px",
        paddingBottom: "0px",
        position: "absolute",
        right: "43%",
        top: "3px",
        width: "200px",
        height: "20px",
        border: "1px dotted #E6E65C",
        background: "#FFFF33",
        textAlign: "center",
    });

    $(document).ajaxStart(function () {
        $("#loading_indicator").show();
    }).ajaxStop(function () {
        $("#loading_indicator").hide();
    });
    
    var qbeFormId = "#qbeform";
    var CLICK = "click";

    function getReport(data) {
        var report_data = $(data).find("#reporttbl");        
        $("#main-report").empty().append(report_data);
        showError(data);
    }

    $(document).on(CLICK, "#prevlink", function (event) {
        nxtpage = $("#prvpage").val().toString();
        to_url = "/report/" + nxtpage + "/"
        $.post(to_url, $(qbeFormId).serialize())
        .done(function (data) { 
            getReport(data);
        })
        .fail(function (xhr, errmsg, err) {
            failure(xhr, errmsg, err);
        });
    });

    $(document).on(CLICK, "#nextlink", function (event) {
        nxtpage = $("#nxtpage").val().toString();
        to_url = "/report/" + nxtpage + "/"
        $.post(to_url, $(qbeFormId).serialize())
        .done(function (data) {
            getReport(data);
        })
        .fail(function (xhr, errmsg, err) {
            failure(xhr, errmsg, err);
        });
    });

    $("#runbtn").on(CLICK, function (event) {
        $.post("/report/", $(qbeFormId).serialize())
        .done(function (data) { 
            getReport(data); 
        })
        .fail(function (xhr, errmsg, err) {
            failure(xhr, errmsg, err);
        });
    });

    $("#showGraphBtn").click(function (event) {
        $.post("/draw/", $(qbeFormId).serialize())
        .done(function (data) {
            showError(data);
        })
        .fail(function (xhr, errmsg, err) {
            failure(xhr, errmsg, err);
        });
    });
    
    $("#showChartBtn").click(function (event) {
        $.post("/report/chart/", $(qbeFormId).serialize())
        .done(function (data) {
            showError(data);
        })
        .fail(function (xhr, errmsg, err) {
            failure(xhr, errmsg, err);
        });
    });

    $("#exportBtn").click(function (event) {
        $.post("/export/", $(qbeFormId).serialize())
        .done(function (data) {
            try {
                showError(data);
            } catch (err) {
                $("#reportfor_err").empty();
                window.URL = window.webkitURL || window.URL;
                var contentType = 'text/csv';
                var csvFile = new Blob([data], { type: contentType });
                var a = document.createElement('a');
                ts = event.timeStamp
                a.download = 'qbe-export-' + ts + '.csv';
                a.href = window.URL.createObjectURL(csvFile);
                a.dataset.downloadurl = [contentType, a.download, a.href].join(':');
                a.click();
            }
        })
        .fail(function (xhr, errmsg, err) {failure(xhr, errmsg, err)});
    });

    $("#toggleDesign").click(function() {
        $("#subdesign").toggle('blind', 500);
        if ($("#toggleDesign").text() == 'hide') {
            $("#toggleDesign").text('show report fields');
        } else {
            $("#toggleDesign").text('hide');
        }
    });

    $("#clearAllClms").click(function() {
        var checkBoxes = $("input[name=cbQbeClm]");
        checkBoxes.prop("checked", !checkBoxes.prop("checked"));
        checkBoxes.each(function(){
            this.click();
        })
    });

});

function showError(data) {
    var errors = $(data).find("#reportfor_err");
    $("#reportfor_err").empty().append(errors);
}

function failure(xhr, errmsg, err) {
    $("#reportfor_err").html("<div class='errorlist'>" + err + "</div>");
    console.log(xhr.status + ": " + xhr.responseText);
}

function hist(id) {
    $.post("/report/hist/" + id, $("#qbeform").serialize())
    .done(function (data) {
        showError(data);
    })
    .fail(function (xhr, errmsg, err) {
        failure(xhr, errmsg, err);
    });
}