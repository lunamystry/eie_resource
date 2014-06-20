
'use strict';

var service = angular.module('service.groups', []);

service.factory('Groups', ['$log', '$cookieStore', '$resource', function($log, $cookieStore, $resource) {
    var key = $cookieStore.get('session_id');
    return $resource('/groups/:name',
        {name: '@name'},
        {
            query: {
                method: 'GET',
                isArray: true,
                headers: { 'x-auth-key': key }
            }
        }
        )
}]);
