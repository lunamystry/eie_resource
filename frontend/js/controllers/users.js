'use strict'

var controller = angular.module('controller.users', []);

controller.controller('usersCtrl', [
        "$scope",
        "$log",
        "$http",
        "$location",
        "Alerts",
        "Users",
        function ($scope, $log, $http, $location, Alerts, Users) {
            $scope.users = Users.query(null, 
                function(value, headers){
                }, 
                function(response){
                    if (response.status == 401) {
                        Alerts.add('danger', 'You are not authorized');
                        $location.path("#/home");
                    }
                });

            var user = $scope.user = {'last_name':"", "first_name": ""
                ,"student_number": "", "yos": 3}; // for the form
            $scope.updateUsername = function() {
                if (typeof user.last_name !== 'undefined' && typeof user.first_name !== 'undefined'){
                    $scope.user.username = user.last_name.toLowerCase()+user.first_name.toLowerCase().charAt(0);
                } else {
                    $scope.user.username = "";
                }

            }
            var studentSuffix = "@students.ug.eie.wits.ac.za";
            var staffSuffix = "@wits.ac.za"
            var emailSuffixes = {1: studentSuffix,
                                 2: studentSuffix,
                                 3: studentSuffix,
                                 4: studentSuffix,
                                 5: studentSuffix,
                                 6: staffSuffix,
                                 7: staffSuffix};
            $scope.updateEmail = function() {
                if(user.yos < 6) {
                    $scope.user.email = [user.student_number.toLowerCase()+emailSuffixes[user.yos]];
                } else {
                    $scope.user.email = [user.first_name.toLowerCase()+"."+user.last_name.toLowerCase()+staffSuffix];
                }
            }
            user.login_shell = "/bin/bash";
            user.home_directory = "/home/ug/";
            $scope.saveUser = function () {
                var new_user = new Users(user);
                new_user.$save(function (user) {
                    $scope.users.push(user);
                    $scope.user = {};
                    $scope.user.login_shell = "/bin/bash";
                    $scope.user.home_directory = "/home/ug/";
                    Alerts.add('success', 'saved');
                }, function (response) {
                    var error_msg = 'could not save ' + user.first_name + " " + user.last_name;
                    Alerts.add('danger', error_msg);
                });
            };
            $scope.deleteUser = function(user, index) {
                var username = user.username;
                user.$remove(function(data, headers) {
                    $scope.users.splice(index, 1);
                    Alerts.add('success', 'deleted');
                }, function(response) {
                    var error_msg = 'could not delete ' + user.first_name + " " + user.last_name
                    Alerts.add('danger', error_msg);
                });
            }

            $scope.alerts = [];
            $scope.addAlert = function(type, msg) {
                $scope.alerts.push({type: type, msg: msg});
            };
            $scope.closeAlert = function(index) {
                $scope.alerts.splice(index, 1);
            }

            $scope.availableHosts = ["babbage.ug.eie.wits.ac.za",
                "hotseat1.ug.eie.wits.ac.za",
                "hotseat2.ug.eie.wits.ac.za",
                "testing.ug.eie.wits.ac.za",
                "resource.eie.wits.ac.za",
                "eieldap.eie.wits.ac.za",
                "volt.eie.wits.ac.za"];
            $scope.form = {};
            $scope.form.host = "";
            $scope.user.hosts = [];
            $scope.addHost = function() {
                if ($scope.user.hosts.indexOf($scope.form.host) == -1) {
                    $scope.user.hosts.push($scope.form.host);
                }
            }
            $scope.removeHost = function(id) {
                $scope.user.hosts.splice(id, 1);
            }
            $scope.userViewCtrl = function($scope) {
                $scope.resetPassword = function() {
                    $http({method: 'PUT', url: '/users/' + $scope.user.username})
                        .success(function(data) {
                            $scope.user = data;
                            console.log(data);
                        });
                }
                $scope.showEditForm = function() {
                    $scope.editing = true;
                }
                $scope.showView = function() {
                    $scope.editing = false;
                }
                $scope.editing = true;
                $scope.updateUser = function(user) {
                    user.$update(function(data) {
                        Alerts.add('success', 'updated');
                    }, function (response) {
                        var error_msg = 'could not save ' + user.first_name + " " + user.last_name;
                        Alerts.add('danger', error_msg);
                    });
                }

                var studentSuffix = "@students.ug.eie.wits.ac.za";
                var staffSuffix = "@wits.ac.za"
                    var emailSuffixes = {1: studentSuffix,
                        2: studentSuffix,
                        3: studentSuffix,
                        4: studentSuffix,
                        5: studentSuffix,
                        6: staffSuffix,
                        7: staffSuffix}
                $scope.updateEmail = function() {
                    if($scope.user.yos < 6) {
                        $scope.user.email = [$scope.user.student_number.toLowerCase()+emailSuffixes[user.yos]];
                    } else {
                        $scope.user.email = [$scope.user.first_name.toLowerCase()+"."+$scope.user.last_name.toLowerCase()+staffSuffix];
                    }
                }
                $scope.addHost = function() {
                    if ($scope.user.hosts.indexOf($scope.form.host) == -1) {
                        $scope.user.hosts.push($scope.form.host);
                    }
                }
                $scope.removeHost = function(id) {
                    $scope.user.hosts.splice(id, 1);
                }
            }
        }
]);
