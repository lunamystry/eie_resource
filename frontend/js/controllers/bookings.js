'use strict'

var controller = angular.module('controller.bookings', []);

controller.controller('bookingsCtrl', [
        "$scope",
        "$log",
        "Computer",
        function ($scope, $log, Computer) {
            $scope.section1 = [];
            $scope.section2 = [];
            $scope.section3 = [];

            Computer.query(null, function(response, headers) {
                var section1 = [];
                for (var i = 1; i < 19; i++) {
                    if (typeof(response[i - 1]) !== 'undefined' && response[i - 1].number == i) {
                        $scope.section1.push(response[i - 1]);
                    } else {
                        $scope.section1.push({"name": "dlab"+i});
                    }
                }
                var section2 = [];
                for (var i = 19; i < 43; i++) {
                    if (typeof(response[i - 1]) !== 'undefined' && response[i - 1].number == i) {
                        $scope.section2.push(response[i - 1]);
                    } else {
                        $scope.section2.push({"name": "dlab"+i});
                    }
                }
                var section3 = [];
                for (var i = 43; i < 78; i++) {
                    if (typeof(response[i - 1]) !== 'undefined' && response[i - 1].number == i) {
                        $scope.section3.push(response[i - 1]);
                    } else {
                        $scope.section3.push({"name": "dlab"+i});
                    }
                }
            }, function (response) {
                console.log("failure");
            })
        }
]);
