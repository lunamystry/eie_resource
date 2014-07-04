'use strict'

var controller = angular.module('controller.bookings', []);

controller.controller('bookingsCtrl', [
        "$scope",
        "$log",
        function ($scope, $log) {
            $scope.computers = [{"name": "dlab1",
                                 "comment": "not in the lab"},
                                {"name": "dlab2",
                                "comment": "not in the lab"},
                                {"name": "dlab44",
                                "comment": "not in the lab"},
                                {"name": "dlab45",
                                "comment": "not in the lab"},
                                {"name": "dlab28",
                                "comment": "not in the lab"},
                                {"name": "dlab19",
                                "comment": "not in the lab"},
                                {"name": "dlab20",
                                "comment": "not in the lab"},
                                {"name": "dlab43",
                                "comment": "not in the lab"}]
        }
]);
