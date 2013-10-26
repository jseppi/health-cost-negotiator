

google.load('visualization', '1', {packages: ['corechart']});

google.setOnLoadCallback(function () {
    angular.bootstrap(document, ['ngCmsApp']);
});

app = angular.module('ngCmsApp', ['ui.select2', 'googlechart.directives',
    'angulartics', 'angulartics.ga']);

app.config(['$locationProvider', '$routeProvider', 
    function($locationProvider, $routeProvider) {

        $locationProvider.html5Mode(true);

        $routeProvider.when('/results/:type/:id/:zipcode/', {
            templateUrl: 'resultsView',
            caseInsensitiveMatch: true
        });

        $routeProvider.when('/start/:type/:zipcode', {
            templateUrl: 'formView'
        });

        $routeProvider.otherwise({
            templateUrl: 'formView'
        });

}]);


app.controller('FormCtrl', ['$scope', '$routeParams', '$location',
    function($scope, $routeParams, $location) {

        $('label a').tooltip();

        $scope.isSubmitting = false;

        $scope.formVals = {};

        $scope.formVals.zip = $routeParams.zipcode || '';
        $scope.formVals.apcdrg = $routeParams.type || 'drg';

        $scope.$watch('formVals.apcdrg', function(newVal) {
            if (newVal === 'drg') {
                $scope.formVals.apc = '';
            } else {
                $scope.formVals.drg = '';
            }
        });

        $scope.canSubmit = function(mainForm) {
            if (mainForm.$invalid) { return false; }

            if (_.isEmpty($scope.formVals.drg) &&
                    _.isEmpty($scope.formVals.apc)) {

                return false;
            }
            return true;
        };

        $scope.submitForm = function(mainForm) {
            var id;

            if (!$scope.canSubmit(mainForm)) { return; }

            if ($scope.formVals.apcdrg === 'apc') {
                id = $scope.formVals.apc;
            } else {
                id = $scope.formVals.drg;
            }

            var pathArr = ["results",  $scope.formVals.apcdrg, id, $scope.formVals.zip];

            $location.path(pathArr.join("/"));
        };
    }]
    );

app.controller('ResultsCtrl', ['$scope', '$http', '$routeParams', '$location', '$filter', '$window',
    function($scope, $http, $routeParams, $location, $filter, $window) {

        $scope.zip = $routeParams.zipcode;
        $scope.type = $routeParams.type;
        $scope.apcDrgId = $routeParams.id;

        $scope.showFacebookShare = function() {
           
            $window.open(
                'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent($location.absUrl()),
                'facebook-share-dialog', 
                'width=626,height=436'
            );
        };

        $scope.showTwitterShare = function() {
            
            $window.open(
                'https://twitter.com/intent/tweet?url=' + encodeURIComponent($location.absUrl()) +
                    '&text=Check out my results on Health Cost Negotiator!',
                'twitter-share-dialog',
                'width=626,height=436'
            );
        };

        var showResults = function(data) {

                var pct = function(payment, charge) {
                        return $filter('number')(payment / charge * 100, 0) + "% of Average Charge";
                    },
                    pmtLabel = function(payment, charge) {
                        return $filter('currency')(payment) + "\n(" + pct(payment, charge) + ")";
                    },
                    chartTitle = function() {
                        return "Charges and Payments for " + $scope.type.toUpperCase() + " "
                            + $scope.apcDrgId + " in ZIP " + $scope.zip;
                    };

                //See: https://github.com/bouil/angular-google-chart
                $scope.chart = {
                    "type": "ColumnChart",
                    "displayed": true,
                    "cssStyle": "height:300px; width:100%;",
                    "options": {
                        "colors": ['#A06A6C', '#237798'],
                        "title": chartTitle(),
                        "isStacked": "false",
                        "fill": 20,
                        "displayExactValues": true,
                        "vAxis": {
                            "format": '$#,###',
                            "gridlines": {
                                "count": 10
                            },
                            "viewWindow": {
                                "min": 0
                            }
                        }
                    },
                    "data": {
                        "cols": [
                            {
                                "id": "region",
                                "label": "Region",
                                "type": "string"
                            },
                            {
                                "id": "charge_avg",
                                "label": "Average Charge",
                                "type": "number"
                            },
                            {
                                "id": "pmt_avg",
                                "label": "Average Payment",
                                "type": "number"
                            }
                        ],
                        "rows": [
                            {
                                "c" : [
                                    {
                                        "v": "Referral Region for " + data.zip
                                    },
                                    {
                                        "v": data.charge_avg_region,
                                        "f": $filter('currency')(data.charge_avg_region)
                                    },
                                    {
                                        "v": data.pmt_avg_region,
                                        "f": pmtLabel(data.pmt_avg_region, data.charge_avg_region)
                                    }
                                ]
                            },
                            {
                                "c" : [
                                    {
                                        "v": "State (" + data.state + ")"
                                    },
                                    {
                                        "v": data.charge_avg_state,
                                        "f": $filter('currency')(data.charge_avg_state)
                                    },
                                    {
                                        "v": data.pmt_avg_state,
                                        "f": pmtLabel(data.pmt_avg_state, data.charge_avg_state)
                                    }
                                ]
                            },
                            {
                                "c" : [
                                    {
                                        "v": "National"
                                    },
                                    {
                                        "v": data.charge_avg_natl,
                                        "f": $filter('currency')(data.charge_avg_natl)
                                    },
                                    {
                                        "v": data.pmt_avg_natl,
                                        "f": pmtLabel(data.pmt_avg_natl, data.charge_avg_natl)
                                    }
                                ]
                            }
                        ]
                    }
                };

                $scope.procedureName = data.name;
                $scope.regionPaymentInfos = data.region_pmt_info;
                $scope.regionAvgCharge = data.charge_avg_region;
                $scope.regionAvgPayment = data.pmt_avg_region;
                $scope.state = data.state;

                if (data.charge_avg_region !== 0) {
                    $scope.regionReduction = (data.charge_avg_region - data.pmt_avg_region) /
                        data.charge_avg_region;
                }

            },

            validateParams = function() {
                var zipPattern = /^[0-9]{5}$/,
                    idPattern = /^[0-9]+$/;

                if (!zipPattern.test($scope.zip) ||
                        ($scope.type !== 'apc' && $scope.type !== 'drg') ||
                            !idPattern.test($scope.apcDrgId)) {

                    $location.path("");
                }
            },

            getPriceData = function() {
                var zipcode = $scope.zip,
                    type = $scope.type,
                    id = $scope.apcDrgId,
                    prom;

                $scope.isFetching = true;
                $scope.hasError = false;

                //Using GET because ajax posts are broken in IE10
                prom = $http.get('/data?zip=' + zipcode + 
                    '&type=' + type + '&id=' + id);

                prom.success(showResults);

                prom.error(function() {
                    $scope.hasError = true;
                });

                prom.always(function() {
                    $scope.isFetching = false;
                });

            };

        validateParams();
        getPriceData();
    }]);





