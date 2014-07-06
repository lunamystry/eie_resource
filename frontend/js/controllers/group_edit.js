'use strict'

var controller = angular.module('controller.group_edit', []);

controller.controller('groupEditCtrl', [
        "$scope",
        "$location",
        "$routeParams",
        "Alerts",
        "Groups",
        function ($scope, $location, $routeParams, Alerts, Groups) {

            var group = $scope.group = new Groups();
            var group_name = $routeParams.name;
            group.$get({"name": group_name}, function(data, headers) {},
                function(response) {
                    if (response.status == 404) {
                        Alerts.add('danger', group_name + " not found");
                        $location.path('/groups');
                    }
                });

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

            $scope.deleteGroup = function(group) {
                group.$remove(function(data, headers) {
                    for (var i = 0; i < $scope.groups.length; ++i) {
                        var entry = $scope.groups[i];
                        if (entry.name == name){
                            $scope.groups.splice(i, 1);
                        }
                    }
                }, function(response) {
                    console.log(response.status);
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
