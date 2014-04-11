
'use strict';

var controller = angular.module('controller.title', []);

controller.controller('titleCtrl', ["$scope", "$location", function ($scope, $location) {
    $scope.title = function () {
      var currentRoute = $location.path().substring(1) || 'home';
      return currentRoute;
    };
}]);
