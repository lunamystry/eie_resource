'use strict';

var controller = angular.module('controller.home', []);

controller.controller('homeCtrl', [
        '$scope',
        '$log',
        '$location',
        'SessionUser',
        'Alerts',
        function($scope, $log, $location, SessionUser, Alerts) {
            $scope.alerts = Alerts.alert_list;

            $scope.sign_in = function() {
                if ($scope.login_form.$valid) {
                    SessionUser.sign_in($scope.username, $scope.password,
                        function(value, headers) {
                            $scope.has_error = false;
                            Alerts.add("info", "You have been logged in");
                            $location.path(SessionUser.homePage);
                        },
                        function(response) {
                            $scope.password = "";
                            if (response.status == 500) {
                                Alerts.add("danger", "So the server is acting up, tell the webmaster please :-)");
                                $scope.login_form.error_message = "So the server is acting up, tell the webmaster please :-)";
                            } else {
                                Alerts.add("danger", "username of password error");
                                $scope.login_form.error_message = "username of password error";
                            }
                            $scope.has_error = true;
                        });
                }
            }

            $scope.sign_out = function () {
                SessionUser.sign_out(function() {
                    $location.path("/home");
                });
            }

            $scope.isLoggedIn = function() {
                return SessionUser.isLoggedIn;
            }

            $scope.session = function() {
                return SessionUser.session;
            }

            $scope.currentRoute = function () {
                return $location.path().substring(1);
            };
        }
]);
