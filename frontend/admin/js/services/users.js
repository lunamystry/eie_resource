
'use strict';

var service = angular.module('service.users', []);

service.factory('Users', ['$resource', function($resource) {
    return $resource('/users/:username',
        {username: '@username'},
        {
            query: {
                method: 'GET',
                isArray: true,
                headers: { 'Session-Key': "session_key" }
            }
        }
        )
}]);
