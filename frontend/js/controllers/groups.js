'use strict'

var controller = angular.module('controller.groups', []);

controller.controller('groupsCtrl', [
        "$scope",
        "$http",
        "Alerts",
        "Groups",
        function ($scope, $http, Alerts, Groups) {
            $scope.groups = Groups.query();

            var group = $scope.group = {'name':'',
                                        'gid_number': '',
                                        'members': [],
                                        'description': ''}; // for the form

            $scope.saveGroup = function  () {
                var new_group = new Groups(group);
                new_group.$save(function (group) {
                    $scope.groups.push(group);
                    $scope.group = {'name':'',
                                    'gid_number': '',
                                    'members': [],
                                    'description': ''};
                }, function(response) {
                    var error_msg = response.data;
                    Alerts.add('danger', error_msg);
                }
                )
            };

            $scope.deleteGroup = function(name) {
                Groups.delete({'name': name});
                for (var i = 0; i < $scope.groups.length; ++i) {
                    var entry = $scope.groups[i];
                    if (entry.name == name){
                        $scope.groups.splice(i, 1);
                    }
                }
            }

            $scope.alerts = [];
            $scope.addAlert = function(type, msg) {
                $scope.alerts.push({type: type, msg: msg});
            };

            $scope.closeAlert = function(index) {
                $scope.alerts.splice(index, 1);
            }

            $scope.form = {};
            $scope.form.host = "";
            $scope.group.hosts = [];
            $scope.addMember = function() {
                if ($scope.group.hosts.indexOf($scope.form.host) == -1) {
                    $scope.group.hosts.push($scope.form.host);
                }
            }

            $scope.removeMember = function(name) {
                $scope.group.hosts.splice(name, 1);
            }
        }
]);
