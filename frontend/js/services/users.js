'use strict';

var service = angular.module('service.users', []);

service.factory('Users', [
        '$log', 
        '$cookieStore', 
        '$resource', 
        function($log, $cookieStore, $resource) {
            var key = $cookieStore.get('session_id');
            return $resource('/users/:username',
                {username: '@username'},
                {
                    query: {
                        method: 'GET',
                        isArray: true,
                        headers: { 'x-auth-key': key }
                    },
                }
                )
        }
]);
