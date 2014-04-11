
'use strict';

var service = angular.module('service.users', []);

service.factory('Users', ['$resource', function($resource) {
    return $resource('/users/:username', {username: '@username'})
}]);
