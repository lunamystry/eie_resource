'use strict'

var controller = angular.module('controller.computers', []);

controller.controller('computersCtrl', [
        "$scope",
        "$log",
        "$http",
        "$location",
        "Alerts",
        "Computer",
        function ($scope, $log, $http, $location, Alerts, Computer) {
            $scope.computers = Computer.query(null,
                function(value, headers){
                },
                function(response){
                    if (response.status == 401) {
                        Alerts.add('danger', 'You are not authorized');
                        $location.path("#/home");
                    }
                });
            $scope.statuses = ['available', 'faulty', 'absent'];

            var computer = $scope.computer = {'name':'dlab',
                                              'mac': '',
                                              'ip': '',
                                              'number': '',
                                              'eietag': '',
                                              'status': 'available',
                                              'comment': ''};

            $scope.saveComputer = function () {
                var new_computer = new Computer(computer);
                new_computer.$save(function (computer) {
                    $scope.computers.push(computer);
                    $scope.computer = {'name':'dlab',
                                       'mac': '',
                                       'ip': '',
                                       'number': '',
                                       'eietag': '',
                                       'status': 'available',
                                       'comment': ''};
                    Alerts.add('success', 'saved');
                }, function (response) {
                    var error_msg = 'could not save ' + computer.name;
                    Alerts.add('danger', error_msg);
                });
            };
            $scope.updateComputer = function(computer) {
                computer.$update(function(data) {
                    Alerts.add('success', 'updated');
                }, function (response) {
                    var error_msg = 'could not save ' + computer.name;
                    Alerts.add('danger', error_msg);
                });
            }
            $scope.deleteComputer = function(computer, index) {
                computer.$remove(function(data, headers) {
                    $scope.computers.splice(index, 1);
                    Alerts.add('success', 'deleted');
                }, function(response) {
                    var error_msg = 'could not delete ' + computer.name;
                    Alerts.add('danger', error_msg);
                });
            }
            $scope.downloadMacs = function() {
                var file = new Blob([data], { type: 'text/plain' });
                saveAs(file, 'mac-ethx.txt');
                Computer.get_macs();
            }
            $scope.downloadDhcpConf = function() {
                var data = Computer.get_dhcp_conf();
                var file = new Blob([data], { type: 'text/conf' });
                saveAs(file, 'dhcp.conf');
            }
        }
]);
