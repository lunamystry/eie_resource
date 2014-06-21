'use strict'

var dir = angular.module('directives.alert', []);

dir.directive('eieAlert', [
        function() {
            return {
                restrict: 'A',
                replace: true,
                template: "<div class='alert alert-{{type}}'>"+
                  "{{message}}" +
                  "</div>",
                scope: {
                    message: "@",
                    type: "@",
                    timeout: "@"
                },
                controller: ['$scope', '$http', function($scope, $http) {
                  $scope.timeout = null;
                  $scope.type = "info";
                  $scope.message = "";
                  $scope.close = function() {
                  }
                }],
            }
        }
]);
