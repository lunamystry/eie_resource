'use strict';

angular.module('resource', [
  'ngRoute',
  'ngResource',
  'ngCookies',
  'ngAnimate',
  'ui.bootstrap',
])
.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/home', {
        templateUrl: 'views/home.html',
    controller: 'homeCtrl'});
    $routeProvider.otherwise({redirectTo: '/home'});
}])
