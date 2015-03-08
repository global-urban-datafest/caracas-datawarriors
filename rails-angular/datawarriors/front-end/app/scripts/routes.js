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
     templateUrl: "views/dashboard.html"

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
   })
   .state('gov.profile.category', {
     url: '/category/:categoryId',
     templateUrl: "views/tweet_sentiment.html",
     controller: "govCategorieCtr"
   })
   .state('gov.profile.relevants', {
     url: '/relevants/:relevanceId',
     templateUrl: "views/relevant_words.html",
     controller: "govRelevantCtr"
   });
  }]);

