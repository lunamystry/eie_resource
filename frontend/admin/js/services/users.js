
'use strict';

var service = angular.module('service.users', []);

service.factory('Users', ['$resource', function($resource) {
    return $resource('/users/:username', 
        {username: '@username'},
        {
            query: {
                method: 'GET',
                isArray: true,
                headers: { 'API-Token': "api_token" }
            } 
        }
        )
}]);
