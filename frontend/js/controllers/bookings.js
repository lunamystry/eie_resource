'use strict'

var controller = angular.module('controller.bookings', []);

controller.controller('bookingsCtrl', [
        "$scope",
        "$log",
        function ($scope, $log) {
            $scope.computers = [{"name": "dlab1",
                                 "number": 1,
                                 "eietag": "0000",
                                 "ipv4": "0.0.0.0",
                                 "mac": "0:0:0:0:0",
                                 "booked_date": null,
                                 "status": "absent",  // faulty | available | unknown
                                 "software": [],
                                 "comment": "not in the lab"},
                                {"name": "dlab19",
                                "number": 19,
                                "eietag": "0000",
                                "ipv4": "0.0.0.0",
                                "mac": "0:0:0:0:0",
                                "booked_date": null,
                                "status": "available",
                                "software": [],
                                "comment": "not in the lab"},
                                {"name": "dlab1",
                                "number": 43,
                                "eietag": "0000",
                                "ipv4": "0.0.0.0",
                                "mac": "0:0:0:0:0",
                                "booked_date": null,
                                "status": "faulty",  // faulty | available | unknown
                                "software": [],
                                "comment": "not in the lab"}]
        }
]);
