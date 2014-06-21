'use strict';

var service = angular.module('service.alerts', []);

service.factory('Alerts', [
        '$log', 
        function($log) {
            alerts = {
                add: function() {

                },
                cleanup: function() {

                },
                alert_list: []
            };
            return alerts;
        }
]);
