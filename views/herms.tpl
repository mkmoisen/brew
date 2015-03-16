<HTML>
<HEAD>
    <link type="text/css" href="/static/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://code.jquery.com/jquery-latest.min.js"
        type="text/javascript"></script>
    <script type="text/javascript" src="https://www.google.com/jsapi?autoload={'modules':[{'name':'visualization','version':'1','packages':['corechart']}]}"></script>
    <script>
        google.load('visualization', '1', {packages: ['corechart']});
        rows = $.parseJSON("{{data}}");
    google.setOnLoadCallback(drawChart);

    function drawChart() {

      var data = new google.visualization.DataTable();
      data.addColumn('number', 'X');
      data.addColumn('number', 'HLT');
      data.addColumn('number', 'Mashtun');
      data.addRows(rows);

      var options = {
        width: 1000,
        height: 563,
        hAxis: {
          title: 'Time'
        },
        vAxis: {
          title: 'Popularity'
        }
      };

      var chart = new google.visualization.LineChart(
        document.getElementById('temp_chart'));

      chart.draw(data, options);

    }
     $(document).ready(function() {
            $('#temp_chart').click(function() {
                $.ajax({
                    url : "test_chart_ajax",
                    success : function(ajaxdata) {
                        alert(ajaxdata);
                        rows = $.parseJSON(ajaxdata);
                        alert(rows);
                        drawChart();
                    },
                    error : function() {
                        alert("Error");
                    }
                });
            });
        });

    </script>

    <TITLE>HERMS Setup</TITLE>
</HEAD>
<Body>

<div id="ex0"></div>

% if not herms.strike_completed:
    <STRONG>Strike Duration: {{strike_duration}}</STRONG><BR />

    <Strong>Temperatures</Strong><BR/>
    <TABLE class="table">
        <TR>
            <TD>Probe Name</TD><TD>Temp</TD>
        </TR>
        <TR>
            <TD>HLT</TD><TD>{{hlt_temp}}</TD>
        </TR>
        <TR>
            <TD>Strike Water</TD><TD>{{mashtun_temp}}</TD>
        </TR>
    </TABLE>

    <Strong>Probes</Strong><BR />
    <TABLE class="table">
        <TR>
            <TD>Strike Water Temp</TD><TD>{{strike_water_temp}}</TD>
        </TR>
        <TR>
            <TD>Strike Water Initialized</TD><TD>{{initialized_strike_water}}</TD>
        </TR>
    </TABLE>
    % if not herms.strike_ready:
        <FORM action="/strike_ready" method="POST">
            After Strike water is initialized, click submit to stop the pump and then pour it in mashtun: <BUTTON type="submit">Submit</BUTTON>
        </FORM>
    % else:
        <FORM action="/strike_complete" method="POST">
            After pouring strike water in mashtun and switching the pump and probe to mashtun, click submit to start: <BUTTON type="submit">Submit</BUTTON>
        </FORM>
    % end
    <STRONG>Strike History</STRONG>
    <div id="strike_temp_chart"></div>
% else:
    % if herms.herms_complete:
        <h1> Mashing is complete. Time to Strike! </h1>
    % end
    <Strong>Total Duration: {{total_duration}}</Strong><br />

    <Strong>Temperatures</Strong><BR/>
    <TABLE class="table">
        <TR>
            <TD>Probe Name</TD><TD>Temp</TD>
        </TR>
        <TR>
            <TD>HLT</TD><TD>{{hlt_temp}}</TD>
        </TR>
        <TR>
            <TD>Mashtun</TD><TD>{{mashtun_temp}}</TD>
        </TR>
    </TABLE>

    <Strong>Probes</Strong><BR />
    <TABLE class="table">
        <TR>
            <TD>Name</TD><TD>Temperature</TD><TD>Duration</TD><TD>Time Elapsed</TD>
        </TR>
        % for step in steps:
            <TR>
                <TD>{{step.name}}</TD><TD>{{step.temp}}</TD><TD>{{step.duration}}</TD><TD>{{step.time_elapsed}}</TD>
            </TR>
        % end
    </TABLE><BR />

    <STRONG>Temperature History</STRONG>
    <div id="temp_chart"></div>
% end
</Body>
</HTML>