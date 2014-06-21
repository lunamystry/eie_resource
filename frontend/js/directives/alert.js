'use strict'

var dir = angular.module('directives.alert', []);

dir.directive('eieAlert', [
        function() {
            return {
                restrict: 'A',
                replace: true,
                template: "<div class='alert alert-{{type}}' ng-show='shown()'>"+
                  "{{message}}" +
                  "<span class='glyphicon glyphicon-remove pull-right' ng-click='close()'></span>"+
                  "<div class='clearfix'></div>"+
                  "</div>",
                scope: {
                    message: "@",
                    type: "@",
                    timeout: "@"
                },
                controller: ['$scope', '$timeout', function($scope, $timeout) {
                  var show = true;
                  $scope.close = function() {
                      show = false;
                  }
                  $timeout($scope.close, parseInt($scope.timeout, 10));
                  $scope.shown = function() {
                        return show;
                  }
                }],
            }
        }
]);
