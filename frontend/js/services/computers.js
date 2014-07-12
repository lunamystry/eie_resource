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
                        headers: { 'x-auth-key': key, 'Content-Type': 'text/x-macs'}
                    },
                    get_dhcp_conf: {
                        method: 'GET',
                        headers: { 'x-auth-key': key, 'Content-Type': 'text/x-dhcp-conf'}
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
                all_computers: [],
                sections: function(successFn, errorFn) {
                    if (computers.all_computers == null) {
                        Computer.query(function(value, header){
                        }, function(response) {

                        });
                    } else {
                        var section1 = [];
                        for (var i = 1; i < 19; i++) {
                            section1.push({"name": "dlab"+i});
                        }
                        var section2 = [];
                        for (var i = 19; i < 43; i++) {
                            section2.push({"name": "dlab"+i});
                        }
                        var section3 = [];
                        for (var i = 43; i < 78; i++) {
                            section3.push({"name": "dlab"+i});
                        }
                        var sections = [section1, section2, section3]
                        return sections;
                    }
                },
            };
            return computers;
}]);
