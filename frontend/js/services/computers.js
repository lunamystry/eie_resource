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
                        var section1 = [{"name": "dlab1",
                                         "comment": "not in the lab"},
                                        {"name": "dlab2",
                                        "comment": "not in the lab"},
                                        {"name": "dlab3",
                                        "comment": "not in the lab"},
                                        {"name": "dlab4",
                                        "comment": "not in the lab"},
                                        {"name": "dlab5",
                                        "comment": "not in the lab"},
                                        {"name": "dlab6",
                                        "comment": "not in the lab"},
                                        {"name": "dlab7",
                                        "comment": "not in the lab"},
                                        {"name": "dlab8",
                                        "comment": "not in the lab"}];
                        var section2 = [{"name": "dlab19",
                                         "comment": "not in the lab"},
                                        {"name": "dlab20",
                                        "comment": "not in the lab"},
                                        {"name": "dlab21",
                                        "comment": "not in the lab"},
                                        {"name": "dlab22",
                                        "comment": "not in the lab"},
                                        {"name": "dlab23",
                                        "comment": "not in the lab"},
                                        {"name": "dlab24",
                                        "comment": "not in the lab"},
                                        {"name": "dlab25",
                                        "comment": "not in the lab"},
                                        {"name": "dlab26",
                                        "comment": "not in the lab"}];
                        var section3 = [{"name": "dlab43",
                                         "comment": "not in the lab"},
                                        {"name": "dlab44",
                                        "comment": "not in the lab"},
                                        {"name": "dlab45",
                                        "comment": "not in the lab"},
                                        {"name": "dlab46",
                                        "comment": "not in the lab"},
                                        {"name": "dlab47",
                                        "comment": "not in the lab"},
                                        {"name": "dlab48",
                                        "comment": "not in the lab"},
                                        {"name": "dlab49",
                                        "comment": "not in the lab"},
                                        {"name": "dlab50",
                                        "comment": "not in the lab"}];
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
