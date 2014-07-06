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
                    save: {
                        method: 'POST',
                        headers: { 'x-auth-key': key }
                    },
                    update: {
                        method: 'PUT',
                        headers: { 'x-auth-key': key }
                    },
                    remove: {
                        method: 'DELETE',
                        headers: { 'x-auth-key': key }
                    },
                    query: {
                        method: 'GET',
                        isArray: true,
                        headers: { 'x-auth-key': key }
                    },
                }
                )
        }
]);
