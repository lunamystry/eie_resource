'use strict'

var controller = angular.module('controller.login', []);

controller.controller('loginCtrl', ["$scope", "Sessions", function ($scope, Sessions) {
    $scope.login = function() {
        var username = $scope.login_form.username;
        var password = $scope.login_form.password;
        Sessions.create(username, password).success(
            function(response) {
                Sessions.current = reponse.key
            });
    }

    $scope.logout = function() {
    }
}]);
