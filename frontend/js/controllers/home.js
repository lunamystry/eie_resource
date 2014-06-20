'use strict';

var controller = angular.module('controller.home', []);

controller.controller('homeCtrl', [
        '$scope',
        '$log',
        '$location',
        'SessionUser',
        function($scope, $log, $location, SessionUser) {
            if (SessionUser.isLoggedIn) {
                $location.path(SessionUser.homePage);
            }
            $scope.sign_in = function() {
                if ($scope.login_form.$valid) {
                    SessionUser.sign_in($scope.username, $scope.password,
                        function(value, headers) {
                            $scope.has_error = false;
                            $location.path(SessionUser.homePage);
                        },
                        function(response) {
                            $scope.password = "";
                            if (response.status == 500) {
                                $scope.login_form.error_message = "So the server is acting up, tell the webmaster please :-)";
                            } else {
                                $scope.login_form.error_message = "username of password error";
                            }
                            $scope.has_error = true;
                        });
                }
            }

            $scope.session = function() {
                return SessionUser.session;
            }
        }
]);
