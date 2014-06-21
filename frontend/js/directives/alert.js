'use strict'

var dir = angular.module('directives.alert', []);

dir.directive('eieAlert', [
        function() {
            return {
                restrict: 'A',
                replace: true,
                transclude: true,
                require: 'ngModel',
                template: "<div class='alert alert-{{ngModel.type}}' ng-show='shown()'>"+
                  "<span class='glyphicon glyphicon-remove pull-right' ng-click='close()'></span>"+
                  "<div ng-transclude></div>" +
                  "<div class='clearfix'></div>"+
                  "</div>",
                scope: {
                    ngModel: '=',
                },
                controller: ['$scope', '$timeout', function($scope, $timeout) {
                  var show = true;
                  if ($scope.ngModel.type == '' || typeof($scope.ngModel.type) == 'undefined') {
                    $scope.ngModel.type = 'info';
                  }
                  if ($scope.ngModel.timeout == '' || typeof($scope.ngModel.timeout) == 'undefined') {
                    $scope.ngModel.timeout = 5000;
                  }
                  $scope.close = function() {
                      show = false;
                  }
                  $timeout(function() {
                      $scope.close();
                      $scope.ngModel.timedOut = true;
                  }, parseInt($scope.ngModel.timeout, 10));
                  $scope.shown = function() {
                        return show;
                  }
                }],
            }
        }
]);
