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
  'service.session',
  'service.users',
  'directives.alert',
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
    .otherwise({redirectTo: '/home'});
}])
.run(['$rootScope', '$location', 'SessionUser', function($rootScope, $location, SessionUser) {
    var noAuthRoutes = ['/home', '/about', '/class_photos'];

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
