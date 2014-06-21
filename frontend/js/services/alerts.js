'use strict';

var service = angular.module('service.alerts', []);

service.factory('Alerts', [
        '$log', 
        function($log) {
            var alerts = {
                add: function(type, message, timeout) {
                    alerts.alert_list.push({type: type, message: message, timeout:timeout, timedOut: false});
                },
                cleanup: function() {

                },
                alert_list: []
            };
            return alerts;
        }
]);
