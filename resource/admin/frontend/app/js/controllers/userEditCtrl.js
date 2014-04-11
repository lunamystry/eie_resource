
'use strict';

var controller = angular.module('controller.userEdit', []);

controller.controller('userEditCtrl', ["$scope", "$http", "$routeParams", function ($scope, $http, $routeParams) {
    var username = $routeParams.username;
    $http({method: 'GET', url: '/users/' + username})
      .success(function(data) {
        $scope.users = data;
      });
}]);
