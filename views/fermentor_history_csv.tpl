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
    <TR ng-repeat="fermwrap in fermwraps">
        <TD><SPAN ng-bind="fermwrap"></SPAN></TD>
    </TR>
</TABLE>


<SCRIPT>
    angular.module('myApp', []).controller('temperatureController', ['$scope','$http', function($scope, $http) {
        console.log('hai');

        $scope.get_fermwraps = function() {
            $http.get('/fermentation/fermwrap-history/get/csv')
            .success(function(data, status, headers, config) {
                console.log(data);
                $scope.fermwraps = data; // JSON array of Fermwrap Data

            }).error(function(data, status, headers, config) {
                console.log("It's a failure NOOB");
            });
        }

        $scope.get_fermwraps();
    }]);
</SCRIPT>

</BODY>

</HTML>