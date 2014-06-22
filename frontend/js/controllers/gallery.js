'use strict'

var controller = angular.module('controller.gallery', []);

controller.controller('galleryCtrl', [
        "$scope",
        "$log",
        "$http",
        "Images",
        function ($scope, $log, $http, Images) {
            $scope.images = Images.query(null, 
                function(value, headers){
                }, 
                function(response){
                    if (response.status == 401) {
                        $location.path("#/home");
                    }
                });
        }
]);
