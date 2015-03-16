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
        document.getElementById('ex0'));

      chart.draw(data, options);

    }
     $(document).ready(function() {
            $('#lol').click(function() {
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
</HEAD>
<BODY>
    <div id="ex0"></div>
    <button id="lol" type="button">lol</button>
</BODY>
</HTML>