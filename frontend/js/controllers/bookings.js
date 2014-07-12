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
                    $scope.section1.push({"name": "dlab"+i});
                }
                for (var i = 0; i < response.length; i++) {
                    var n = response[i].number;
                    if (n > 0 && n < 19) {
                        $scope.section1[n - 1] = response[i];
                    }
                }
                var section2 = [];
                for (var i = 19; i < 43; i++) {
                    $scope.section2.push({"name": "dlab"+i});
                }
                for (var i = 0; i < response.length; i++) {
                    var n = response[i].number;
                    if (n > 18 && n < 43) {
                        $scope.section2[n - 19] = response[i];
                    }
                }
                var section3 = [];
                for (var i = 43; i < 78; i++) {
                    $scope.section3.push({"name": "dlab"+i});
                }
                for (var i = 0; i < response.length; i++) {
                    var n = response[i].number;
                    if (n > 42 && n < 78) {
                        $scope.section3[n - 43] = response[i];
                    }
                }
            }, function (response) {
                console.log("failure");
            })
        }
]);
