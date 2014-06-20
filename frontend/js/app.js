'use strict';

angular.module('resource', [
  'ngRoute',
  'ngResource',
  'ngCookies',
  'ngAnimate',
  'ui.bootstrap',
  'controller.home',
  'controller.profile',
  'controller.admin',
  'service.session',
  'service.users',
])
.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/home', {
        templateUrl: 'views/home.html',
        controller: 'homeCtrl'})
    .when('/profile', {
        templateUrl: 'views/profile.html',
        controller: 'profileCtrl'})
    .when('/admin', {
        templateUrl: 'views/admin.html',
        controller: 'adminCtrl'})
    .otherwise({redirectTo: '/home'});
}])
