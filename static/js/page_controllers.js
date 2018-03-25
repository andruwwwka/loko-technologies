var global_from_year = null,
    global_to_year = null;

$(function () {
    fillYearRange("year_from", null, null);
    fillYearRange("year_to", null, null);
    initialBranches();
    fillSeries(null);
    drowReport(null, null, null, null)
});

function fillYearRange(selector_name, from_year, to_year, default_value){
    $.get("/app/common/year_range/?from=" + from_year + "&to=" + to_year + "&default=" + default_value, function(data) {
        $("#" + selector_name)
            .find("option")
            .remove()
            .end();
        $.each(data, function(key, value) {
            $("#" + selector_name)
                .append($("<option>", { value : value })
                .text(value));
        });
        if (default_value){
            $("#" + selector_name + " option[value=" + default_value + "]").attr("selected","selected");
        }
        else{
            if ((selector_name == "year_to")&&(global_to_year == null)){
                $("#" + selector_name + " option").last().attr("selected","selected");
            }
        }
    })
}

$("#year_from").change(function() {
    global_from_year = $(this).val();
    fillYearRange("year_to", $(this).val(), null, global_to_year);
});

$("#year_to").change(function() {
    global_to_year = $(this).val();
    fillYearRange("year_from", null, $(this).val(), global_from_year);
});

$("#branches").change(function() {
    $("#series")
        .find("option")
        .remove()
        .end();
    fillSeries($(this).val());
});

$("#search_form").submit(function(event){
    event.preventDefault();
    var from_year=$("#year_from").val(),
        to_year=$("#year_to").val(),
        branches=$("#branches").val(),
        series=$("#series").val();
    drowReport(from_year, to_year, branches, series);
});

function initialBranches(){
    $.get("/app/common/branches/", function(data) {
        $.each(data, function(key, value) {
            $("#branches")
                .append($("<option>", { value : value })
                .text(value));
        });
    })
}

function fillSeries(branches){
    $.get("/app/common/series/?branches=" + branches, function(data) {
        $.each(data, function(key, value) {
            $("#series")
                .append($("<option>", { value : value })
                .text(value));
        });
    })
}

function drowReport(from_year, to_year, branches, series) {
    $.get("/app/report_data/?from_year=" + from_year + "&to_year=" + to_year + "&branches=" + branches + "&series=" + series, function(data) {
        var report_data = [];
        Object.keys(data).forEach(function(key) {
          var val = [data[key]["year"], data[key]["total_cost"]];
          report_data.push(val);
        });
        var bar_data = {
          data : report_data,
          color: "#f52343"
        };
        $.plot("#bar-chart", [bar_data], {
          grid  : {
            borderWidth: 1,
            borderColor: "#f3f3f3",
            tickColor  : "#f3f3f3"
          },
          series: {
            bars: {
              show    : true,
              barWidth: 0.1,
              align   : "center"
            }
          },
          xaxis : {
            mode      : "categories",
            tickLength: 0
          }
        })
    })
}