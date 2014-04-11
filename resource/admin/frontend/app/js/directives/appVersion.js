'use strict'

var dir = angular.module('directives.appVersion', []);

dir.directive('appVersion', ['version', function(version) {
    return function(scope, elm, attrs) {
        elm.text(version);
    };
}]);
