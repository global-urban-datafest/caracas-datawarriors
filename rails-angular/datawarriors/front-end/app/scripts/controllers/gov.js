'use strict';
var govControllers = angular.module('govControllers', []);

govControllers.controller('govProfileCtr', [
  '$scope',
  '$state',
  'Tweets',
  function($scope, $state, Tweets) {
    if ($state.params.govId == 1) {
      $scope.gov = {
        id: 1,
        name: "Alcaldía del Hatillo",
        mayor: "David Smolansky",
        politics: [
          "Participación ciudadana con asociaciones de vecinos y consejos comunales",
          "Basura: diversificar la flota de camiones, factibilidad de la recolección nocturna, gps en los camiones de basura,  optimizar el tiempo de recolección de los camiones" ,
          "Vías: Eliminar filtraciones en las vías, Programa de bacheo amplio, Brigada cuya función sea tapar huecos provisionalmente, Mejorar el rayado y señalización de las vías"
        ]
      };
    } else {
      $scope.gov = {
        id: 2,
        name: "Alcaldía de Sucre",
        mayor: "Carlos Oscariz",
        politics: [
          "Seguridad: Una policía más grande, inteligente y eficiente, Incrementar el número de funcionarios, patrullas, motos y equipamiento policial para mejorar la seguridad, Patrullaje comunitario",
          "Vías: Mantenimiento de vías con bacheo y afaltado, Manejo del flujo de tráfico",
          "Basura: Nuevas empresas en el servicio de recolección de basura, Supervisión del servicio de recolección con las últimas tecnologías, Fomentación del reciclaje" 

        ]
      };
    }
    
    $scope.goCategory = function(index) {
      if ($state.current.name =="gov.profile.relevants")
        $state.go('gov.profile.relevants', {relevanceId: index});
      else
        $state.go('gov.profile.category', {categoryId: index});

    };
    $scope.goSentiment = function(index) {
      $state.go('gov.profile.category', {categoryId: index});
    };
    $scope.goRelevance = function(index) {
      $state.go('gov.profile.relevants', {relevanceId: index});
    };


    $scope.goCategory(0);

    
}]);

govControllers.controller('govCategorieCtr', [
  '$scope',
  '$state',
  'Tweets',
  function($scope, $state, Tweets) {
    $scope.category = $state.params.categoryId;
    Tweets.sentiment($state.params.govId, $state.params.categoryId).success(function(data){
      $scope.tweets = data;
      window.tweets = $scope.tweets;
    });
}]);

govControllers.controller('govRelevantCtr', [
  '$scope',
  '$state',
  'Relevants',
  function($scope, $state, Words) {
    $scope.category = $state.params.categoryId;
    $scope.colors = ["#800026", "#bd0026", "#e31a1c", "#fc4e2a", "#fd8d3c", "#feb24c", "#fed976"];
    Words.all($state.params.govId, $state.params.relevanceId).success(function(data){
      $scope.words_raw = data[0];
      $scope.words = $.map($scope.words_raw.neighbourhoods, function(w){
        return {text: w._id, weight: w.value} 
      })
      $scope.arrived = true;
    });
}]);
