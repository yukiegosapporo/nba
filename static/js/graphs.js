queue()
    .defer(d3.json, "/playerchoose/projects")
    .await(makeGraphs);
 
function makeGraphs(error, projectsJson, statesJson) {
    //Clean projectsJson data
    var playerProjects = projectsJson;
    var dateFormat = d3.time.format("%Y-%m-%d");
    playerProjects.forEach(function(d) {
        d["DATE"] = dateFormat.parse(d["DATE"]);
        // d["DATE"].setDate(1);
        // d["DRIBBLES"] = +d["DRIBBLES"];
    });
    //Create a Crossfilter instance
    var ndx = crossfilter(playerProjects);
    // var keyword = document.getElementById("keywordTxt").value;
    //Define Dimensions
    var playerNameDim = ndx.dimension(function(d) {
        return d["PLAYER_NAME"];
    });
    var defenseNameDim = ndx.dimension(function(d) {
        return d["DEFENSE"];
    });
    
    // playerNameDim.filterExact("Stephen Curry")
    document.getElementById("offense").addEventListener("change", offenseFilter);

    function offenseFilter() {
        var offplayer = document.getElementById("offense").value;
        playerNameDim.filterExact(offplayer);
        dc.renderAll();
        console.dir(offplayer);
    };

    document.getElementById("defense").addEventListener("change", defenseFilter);

    function defenseFilter() {
        var defplayer = document.getElementById("defense").value;
        defenseNameDim.filterExact(defplayer);
        dc.renderAll();
        console.dir(defplayer);
    };


    var periodDim = ndx.dimension(function(d) {
        return d["PERIOD"];
    });
    var pointTypeDim = ndx.dimension(function(d) {
        return d["PTS_TYPE"];
    });
    var shotResultDim = ndx.dimension(function(d) {
        return d["SHOT_RESULT"];
    });
    var locationDim = ndx.dimension(function(d) {
        return d["LOCATION"];
    });
    var dateDim = ndx.dimension(function(d) {
        return d["DATE"];
    });


function reduceAddAvg(attr) {
  return function(p,v) {
    ++p.count
    p.sum += v[attr];
    p.avg = p.sum/p.count;
    return p;
  };
}
function reduceRemoveAvg(attr) {
  return function(p,v) {
    --p.count
    p.sum -= v[attr];
    p.avg = p.sum/p.count;
    return p;
  };
}
function reduceInitAvg() {
  return {count:0, sum:0, avg:0};
}


    //Calculate metrics
    var playerNameGroup = playerNameDim.group();
    var periodGroup = periodDim.group();
    var periodGroupAvg = periodDim.group().reduceSum(function(d) {
        return d["PTS"];
    })/periodDim.group().reduceSum(function(d) {
        return d["PTS"];
    });
    var shotResultGroup = shotResultDim.group();
    var shotResultGroupAvg = shotResultDim.group().reduce(reduceAddAvg('PTS'), reduceRemoveAvg('PTS'), reduceInitAvg);
    var totalPointDate = dateDim.group().reduceSum(function(d) {
        return d["PTS"];
    });


    var all = ndx.groupAll();
    var totalPoints = ndx.groupAll().reduceSum(function(d) {
        return d["PTS"];
    });

    // var max_state = totalDonationsByState.top(1)[0].value;

    //Define values (to be used in charts)
    var minDate = dateDim.bottom(1)[0]["DATE"];
    var maxDate = dateDim.top(1)[0]["DATE"];

    console.log = function(log) {
        document.getElementById('console_log').innerHTML += log + "<br>";
    }



    // //Charts
    var timeChart = dc.lineChart("#time-chart");
    var playerNameChart = dc.rowChart("#resource-type-row-chart");
    var periodChart = dc.rowChart("#poverty-level-row-chart");
    // var usChart = dc.geoChoroplethChart("#us-chart");
    var numberProjectsND = dc.numberDisplay("#number-projects-nd");
    var totalDonationsND = dc.numberDisplay("#total-donations-nd");

    numberProjectsND
        .formatNumber(d3.format("d"))
        .valueAccessor(function(d) {
            return d;
        })
        .group(all);

    totalDonationsND
        .formatNumber(d3.format("d"))
        .valueAccessor(function(d) {
            return d;
        })
        .group(totalPoints)
        .formatNumber(d3.format(".3s"));

    timeChart
        .width(600)
        .height(160)
        .margins({
            top: 10,
            right: 50,
            bottom: 30,
            left: 50
        })
        .dimension(dateDim)
        .group(totalPointDate)
        .transitionDuration(100)
        .x(d3.time.scale().domain([minDate, maxDate]))
        .elasticY(true)
        .xAxisLabel("Game day")
        .yAxis().ticks(10);

    playerNameChart
        .width(300)
        .height(250)
        .dimension(shotResultDim)
        .group(shotResultGroup)
        .elasticX(true)
        .xAxis().ticks(4);


    periodChart
        .width(300)
        .height(250)
        .dimension(periodDim)
        .group(periodGroup)
        .elasticX(true)
        .xAxis().ticks(4);


    // usChart.width(1000)
    //     .height(330)
    //     .dimension(stateDim)
    //     .group(totalDonationsByState)
    //     .colors(["#E2F2FF", "#C4E4FF", "#9ED2FF", "#81C5FF", "#6BBAFF", "#51AEFF", "#36A2FF", "#1E96FF", "#0089FF", "#0061B5"])
    //     .colorDomain([0, max_state])
    //     .overlayGeoJson(statesJson["features"], "state", function(d) {
    //         return d.properties.name;
    //     })
    //     .projection(d3.geo.albersUsa()
    //         .scale(600)
    //         .translate([340, 150]))
    //     .title(function(p) {
    //         return "State: " + p["key"] + "\n" + "Total Donations: " + Math.round(p["value"]) + " $";
    //     })

    dc.renderAll();

};