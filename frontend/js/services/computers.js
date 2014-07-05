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
                first_col: function(successFn, errorFn) {
                },
                second_col: function(successFn, errorFn) {
                },
                third_col: function(successFn, errorFn) {
                    return section3;
                }
            };
            return computers;
}]);
