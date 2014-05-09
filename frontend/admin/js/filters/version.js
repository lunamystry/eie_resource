
'use strict';

var filter = angular.module('filters.version', []);

filter.filter('interpolate', ['version', function(version) {
    return function(text) {
      return String(text).replace(/\%VERSION\%/mg, version);
    }
}]);
