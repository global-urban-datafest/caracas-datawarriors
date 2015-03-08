'use strict';

angular.module('datawarriors');

angular.module('datawarriors').config([
  '$stateProvider',
  '$urlRouterProvider',
  '$locationProvider',
  function ($stateProvider, $urlRouterProvider, $locationProvider) {
     
  $urlRouterProvider.otherwise("/");
    //$locationProvider.html5Mode(true);

  $stateProvider
   .state('dashboard', {
     url: '/',
     //templateUrl: "views/index.html"
   })
   .state('gov', {
     abstract: true,
     url: '/gov',
     template: "<ui-view/>"
   })
   .state('gov.profile', {
     url: '/:govId',
     templateUrl: "views/gov.html",
     controller: "govProfileCtr"
   });
  }]);
