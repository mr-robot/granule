'use strict';

/* Controllers */
var granuleControllers = angular.module('granuleControllers', []);



granuleControllers.controller('LoginCtrl', [ 'authDefaults',
                                            'authService',
                                             '$rootScope',
                                             '$scope','$location',
                                             function(authDefaults, authService, $rootScope, $scope,$location){


            authDefaults.authenticateUrl = '/api/2015-05-30/authenticate';
            // listen for login events
            $rootScope.$on('login', function() {
                $scope.loggedInUsername = authService.username();
            });

            // listen for logout events
            $rootScope.$on('logout', function() {
                $scope.loggedInUsername = null;
            });

            // method to log-in
            $scope.onLoginButton = function () {
                // pass input username and password to
                // the service for authentication
                authService
                .login($scope.username, $scope.password)
                .success(function() {
                    $location.path('/activity');
                })
                .error(function() {
                    // handle login error

                });
            };

            // method to log out
            $scope.onLogoutButton = function () {
                // simply call the logout button
                authService.logout();
            };






}]);



granuleControllers.controller('ActivityListCtrl', ['$scope', 'Activity',
    function ($scope, Activity) {
        var entry = Activity.get({ }, function() {
            console.log(entry);
          });
    }]);


granuleControllers.controller('ActivityDetailCtrl', ['$scope', '$routeParams','Activity',
    function ($scope, $routeParams, Activity) {
        var entry = Activity.get({ activityId: $routeParams.activityId }, function() {
            console.log(entry);
          });
    }]);