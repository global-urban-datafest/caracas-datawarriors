'use strict';
var govControllers = angular.module('govControllers', []);

govControllers.controller('govProfileCtr', [
  '$scope',
  '$state',
  'Tweets',
  function($scope, $state, Tweets) {
    if ($state.params.govId == 0) {
      $scope.gov = {
        id: 0,
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
        id: 1,
        name: "Alcaldía de Sucre",
        mayor: "Carlos Oscariz",
        politics: ["1", "2"]
      };
    }
}]);
