'use strict';

var service = angular.module('service.computers', []);

service.factory('Computer', [
        '$log',
        '$cookieStore',
        '$resource',
        function($log, $cookieStore, $resource) {
            var key = $cookieStore.get('session_id');
            return $resource('/computers/:_id',
                {_id: '@_id'},
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
                    get_macs: {
                        method: 'GET',
                        headers: { 'x-auth-key': key, 'Accept': 'text/x-macs'}
                    },
                    get_dhcp_conf: {
                        method: 'GET',
                        headers: { 'x-auth-key': key, 'Accept': 'text/x-dhcp-conf'}
                    },
                }
                )
        }
]);
