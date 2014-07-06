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

            $scope.deleteGroup = function(group, index) {
                group.$remove(function(data, headers) {
                    $scope.groups.splice(index, 1);
                    Alerts.add('success', 'deleted');
                }, function(response) {
                    console.log(response.status);
                    Alerts.add('danger', 'could not delete user');
                }
                );
            }

            $scope.form = {};
            $scope.form.member = "";
            $scope.group.members = [];
            $scope.addMember = function() {
                if ($scope.group.members.indexOf($scope.form.member) == -1) {
                    $scope.group.members.push($scope.form.member);
                }
            }

            $scope.removeMember = function(name) {
                $scope.group.members.splice(name, 1);
            }
        }
]);
