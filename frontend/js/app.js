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
  'controller.users',
  'controller.groups',
  'controller.group_edit',
  'controller.about',
  'controller.gallery',
  'controller.computers',
  'controller.lab_layout',
  'controller.bookings',
  'service.session',
  'service.users',
  'service.groups',
  'service.alerts',
  'service.images',
  'service.computers',
  'service.version',
  'directives.alert',
  'directives.computer',
  'directives.appVersion',
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
    .when('/users', {
        templateUrl: 'views/users.html',
        controller: 'usersCtrl'})
    .when('/groups', {
        templateUrl: 'views/groups.html',
        controller: 'groupsCtrl'})
    .when('/groups/:name', {
        templateUrl: 'views/group_edit.html',
        controller: 'groupEditCtrl'})
    .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'aboutCtrl'})
    .when('/computers', {
        templateUrl: 'views/computers.html',
        controller: 'computersCtrl'})
    .when('/bookings', {
        templateUrl: 'views/bookings.html',
        controller: 'bookingsCtrl'})
    .when('/gallery', {
        templateUrl: 'views/gallery.html',
        controller: 'galleryCtrl'})
    .otherwise({redirectTo: '/home'});
}])
.run(['$rootScope', '$location', 'SessionUser', 'Alerts', function($rootScope, $location, SessionUser, Alerts) {
    var noAuthRoutes = ['/home', '/about', '/gallery', '/bookings'];

    var routeClean = function (route) {
        return _.find(noAuthRoutes, function (noAuthRoute) {
            return route.startsWith(noAuthRoute);
        });
    };

    SessionUser.restore_session();
    $rootScope.$on('$routeChangeStart', function (event, next, current) {
        if (!routeClean($location.url()) && !SessionUser.isLoggedIn) {
            $location.path("/home");
        }
    });
}]);
