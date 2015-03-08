'use strict';

angular.module('datawarriors');

angular.module('datawarriors').config([
  '$stateProvider',
  '$urlRouterProvider',
  '$locationProvider',
  function ($stateProvider, $urlRouterProvider, $locationProvider) {
     
  $urlRouterProvider.otherwise("/");
    $locationProvider.html5Mode(true);

  $stateProvider
   .state('dashboard', {
     url: '/',
     templateUrl: "/static/views/index.html"
   });

  $stateProvider
   .state('category', {
     url: '/category',
     templateUrl: "/static/views/category.html"
   });
  }]);
