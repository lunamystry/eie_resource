'use strict';

var service = angular.module('service.computers', []);

service.factory('Computers', [
        '$log', 
        '$cookieStore', 
        '$resource', 
        function($log, $cookieStore, $resource) {
            var key = $cookieStore.get('session_id');
            return $resource('/computers/:_id',
                {_id: '@id'},
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
