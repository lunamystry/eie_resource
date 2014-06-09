
'use strict';

var service = angular.module('service.users', []);

service.factory('Users', ['$resource', function($resource) {
    return $resource('/users/:username',
        {username: '@username'},
        {
            query: {
                method: 'GET',
                isArray: true,
                headers: { 'x-auth-key': "session_key" }
            }
        }
        )
}]);
