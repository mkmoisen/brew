<!DOCTYPE html>
<html>

<head>
<script src= "http://ajax.googleapis.com/ajax/libs/angularjs/1.3.14/angular.min.js"></script>
</head>

<body>

<div ng-app="myApp" ng-controller="personController">

First Name: <input type="text" ng-model="firstName"><br>
Last Name: <input type="text" ng-model="lastName"><br>
<br>
Full Name: {{'{{firstName + " " + lastName}}'}}

</div>

<script>
angular.module('myApp', []).controller('personController', ['$scope', function($scope) {
    $scope.firstName = "{{first_name}}",
    $scope.lastName = "{{last_name}}"
}]);
</script>

</body>
</html>
