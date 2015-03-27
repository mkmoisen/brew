<HTML>
<HEAD>
    <TITLE>Fermentation Temperature History</TITLE>
    <!-- Bootstrap -->
    <link type="text/css" href="/static/css/bootstrap.min.css" rel="stylesheet">
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/static/js/bootstrap.min.js"></script>
    <script src="/static/js/moment.js"></script>

    <script src= "http://ajax.googleapis.com/ajax/libs/angularjs/1.3.14/angular.min.js"></script>
</HEAD>

<BODY ng-app="myApp" ng-controller="temperatureController">

<TABLE class="table">
<TR>
<TD>
    <TABLE class="table table-striped">
        <THEAD>
            <TH>Hostname</TH>
            <TH>Fermentor</TH>
            <TH>Date</TH>
            <TH>Ambient</TH>
            <TH>Wort</TH>
            <TH>Target</TH>
            <TH>Is Fermwrap On?</TH>
            <TH>Fermwrap Turned On Now?</TH>
            <TH>Fermwrap Turned Off Now?</TH>
        </THEAD>
        <TBODY>
            <TR ng-repeat="temp in raw_temps">
                <TD><SPAN ng-bind="temp.hostname"></SPAN></TD>
                <TD><SPAN ng-bind="temp.fermentor"></SPAN></TD>
                <TD><SPAN ng-bind="temp.dt"></SPAN></TD>
                <TD><SPAN ng-bind="temp.ambient_temp"></SPAN></TD>
                <TD><SPAN ng-bind="temp.wort_temp"></SPAN></TD>
                <TD><SPAN ng-bind="temp.target_temp"></SPAN></TD>
                <TD><SPAN ng-bind="temp.is_fermwrap_on"></SPAN></TD>
                <TD><SPAN ng-bind="temp.fermwrap_turned_on_now"></SPAN></TD>
                <TD><SPAN ng-bind="temp.fermwrap_turned_off_now"></SPAN></TD>
            </TR>
        </TBODY>
    </TABLE>
</TD>

<TD>
    <TABLE class="table table-striped">
        <THEAD>
            <TH>Fermentor</TH>
            <TH>Date</TH>
            <TH>Ambient</TH>
            <TH>Target at Start</TH>
            <TH>Target at End</TH>
            <TH>Temp Differential</TH>
            <TH>Minutes Heater On</TH>
            <TH>Minutes Heater Off</TH>
        </THEAD>
        <TBODY>
            <TR ng-repeat="fermwrap in fermwraps">
                <TD><SPAN ng-bind="fermwrap.fermentor"></SPAN></TD>
                <TD><SPAN ng-bind="fermwrap.dt"></SPAN></TD>
                <TD><SPAN ng-bind="fermwrap.ambient_temp"></SPAN></TD>
                <TD><SPAN ng-bind="fermwrap.target_temp_at_start"></SPAN></TD>
                <TD><SPAN ng-bind="fermwrap.target_temp_at_end"></SPAN></TD>
                <TD><SPAN ng-bind="fermwrap.temp_differential"></SPAN></TD>
                <TD><SPAN ng-bind="fermwrap.minutes_heater_on"></SPAN></TD>
                <TD><SPAN ng-bind="fermwrap.minutes_heater_off"></SPAN></TD>
            </TR>
        </TBODY>
    </TABLE>
</TD>
</TR>
</TABLE>



<SCRIPT>
    angular.module('myApp', []).controller('temperatureController', ['$scope','$http', function($scope, $http) {
        console.log('hai');

        $scope.get_raw_temps = function() {
            $http.get('/fermentation/temperature/raw/get')
            .success(function(data, status, headers, config) {
                $scope.raw_temps = data; // JSON Array of Raw Data
            }).error(function(data, status, headers, config) {
                console.log("It's a failure NOOB");
            });
        }

        $scope.get_fermwraps = function() {
            $http.get('/fermentation/fermwrap-history/get')
            .success(function(data, status, headers, config) {
                $scope.fermwraps = data; // JSON array of Fermwrap Data
            }).error(function(data, status, headers, config) {
                console.log("It's a failure NOOB");
            });
        }

        $scope.get_raw_temps();
        $scope.get_fermwraps();
    }]);
</SCRIPT>

</BODY>

</HTML>