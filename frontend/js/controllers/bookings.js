'use strict'

var controller = angular.module('controller.bookings', []);

controller.controller('bookingsCtrl', [
        "$scope",
        "$log",
        "Computers",
        function ($scope, $log, Computers) {
            $scope.section1 = Computers.sections()[0];
            $scope.section2 = Computers.sections()[1];
            $scope.section3 = Computers.sections()[2];
        }
]);
