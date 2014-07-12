'use strict'

var dir = angular.module('directives.computer', []);

dir.directive('eieComputer', [
        function() {
            return {
                restrict: 'A',
                replace: true,
                transclude: true,
                require: 'ngModel',
                template: "<div class='computer computer-{{ngModel.status}}'>"+
                  "<h2 tooltip='{{ngModel.comment}}' tooltip-placement='right'>{{ngModel.name}}</h2>"+
                  "<div class='clearfix'></div>"+
                  "</div>",
                scope: {
                    ngModel: '=',
                },
                controller: ['$scope', function($scope) {
                }],
            }
        }
]);
