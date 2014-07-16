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

            var computer = $scope.computer = {'name':'DLAB',
                                              'mac': 'F8:B1:56:',
                                              'ipv4': '146.141.119.',
                                              'number': '',
                                              'eietag': 'ND',
                                              'servicetag': 'ND02',
                                              'status': 'available',
                                              'comment': ''};

            $scope.saveComputer = function () {
                var new_computer = new Computer(computer);
                new_computer.$save(function (computer) {
                    $scope.computers.push(computer);
                    Alerts.add('success', 'No.' + computer.number + ' added');
                }, function (response) {
                    var error_msg = 'could not save ' + computer.name;
                    Alerts.add('danger', error_msg);
                });
            };
            $scope.updateComputer = function(computer) {
                computer.$update(function(data) {
                    Alerts.add('success', 'No.'+computer.number + ' save');
                }, function (response) {
                    var error_msg = 'could not save ' + computer.name;
                    Alerts.add('danger', error_msg);
                });
            }
            $scope.deleteComputer = function(computer, index) {
                var number = computer.number;
                var really_delete = confirm('are you sure?');
                if (really_delete) {
                    computer.$remove(function(data, headers) {
                        console.log(index);
                        $scope.computers.splice(index, 1);
                        Alerts.add('success', 'No.' + number + ' deleted');
                    }, function(response) {
                        var error_msg = 'could not delete ' + computer.name;
                        Alerts.add('danger', error_msg);
                    });
                }
            }
            $scope.downloadMacs = function() {
                var data = Computer.get_macs(function(response, headers) {
                    var file = new Blob([response.data], { type: 'text/conf' });
                    saveAs(file, 'mac-ethx.txt');
                }, 
                function(response) {
                    var error_msg = 'could not download MACs';
                    Alerts.add('danger', error_msg);
                });
            }
            $scope.downloadDhcpConf = function() {
                var data = Computer.get_dhcp_conf(function(response, headers) {
                    var file = new Blob([response.data], { type: 'text/conf' });
                    saveAs(file, 'dhcp.conf');
                }, 
                function(response) {
                    var error_msg = 'could not download MACs';
                    Alerts.add('danger', error_msg);
                });
            }
        }
]);
