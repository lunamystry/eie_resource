'use strict';

var service = angular.module('service.images', []);

service.factory('Images', [
        '$log',
        '$resource',
        function($log, $resource) {
            return $resource('/images/:_id',
                {_id: '@id'},
                {
                    query: {
                        method: 'GET',
                        isArray: true,
                    },
                }
                )
        }
]);
