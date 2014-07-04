'use strict';

var service = angular.module('service.computers', []);

service.factory('Computer', [
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
service.factory('Computers', [
        '$log',
        'Computer',
        function($log, Computer) {
            var computers = {
                all_computers: null,
                all: function(successFn, errorFn) {
                    if (computers.all_computers == null) {
                        Computer.query(function(value, header){
                        }, function(response) {

                        });
                    } else {
                        return computers.all_computers;
                    }
                },
                first_col: function(successFn, errorFn) {

                },
                second_col: function(successFn, errorFn) {

                },
                third_col: function(successFn, errorFn) {

                }
            };
            return computers;
}]);
