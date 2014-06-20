'use strict'

var controller = angular.module('controller.profile', []);

controller.controller('profileCtrl', [
        '$scope', 
        'SessionUser', 
        'Users', 
        function($scope, SessionUser, Users) {
            $scope.change_password = function() {
                if ( Users.authenticate()) {
                    console.log("Changed password");
                    if ( $scope.password_form.new_password == $scope.password_form.new_password2) {
                        Users.change_password($scope.password, $scope.new_password);
                    } else {
                        $scope.password_form.error_message = "Passwords don't match";
                    }
                } else {
                    $scope.password_form.error_message = "Password is wrong bud!";
                }
            }
        }
]);
