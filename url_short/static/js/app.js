'use strict';

angular
    .module('UrlShortener', [])
    .factory('windowAlert', [
        '$window',
        function($window) {
            return $window.alert;
        }
    ])
    .directive('watchUrl', function(){
        /* If the input has no text, the 'your url must start with http://' error on the page
         * should not be shown. This directive sets the parent scope's valid_input_length to 0
         * if the input is empty. This prevents the error block from being shown. */
            return{
                restrict: 'A',
                link: function(scope, elem, attrs){
                        elem.bind("keyup", function(){
                            scope.$apply(function(){
                                scope.valid_input_length = elem[0].value.length;
                            })
                            ;
                            event.keyCode == 13 && form.$valid ? shorten_url(url_to_summarize) : null;
                        })
                        ;
                      }
            }
        }
    )
    .controller('ShortenController', [
            '$scope',
            '$http',
            'windowAlert',
            function ($scope, $http, windowAlert) {
                $scope.url_to_summarize = "";
                $scope.result = {};
                ZeroClipboard.config({swfPath: "/static/swf/ZeroClipboard.swf"});
                $scope.copy_button = $("button#copy_short_url");
                $scope.zero_client = new ZeroClipboard($scope.copy_button);

                $scope.zero_client.on('ready', function(event){
                    $scope.zero_client.on('copy', function(event){
                        event.clipboardData.setData('text/plain', $scope.result.short_url);
                    })
                    ;

                    $scope.zero_client.on( 'aftercopy', function(event){
                        $scope.copy_button.text('Copied!');
                    })
                    ;
                })
                ;

                $scope.shorten_url = function(url_to_summarize){
                    $http
                        .get('/shorten?url='+encodeURIComponent(url_to_summarize))
                        .success(function(data, status, headers, config) {
                            if (data.success) {
                                $scope.copy_button.text('Copy');
                                $scope.result.long_url = data.long_url;
                                $scope.result.short_url = data.short_url;
                                $scope.form.$setPristine();
                                delete $scope.shortenerror
                            } else {
                                $scope.result = {};
                                $scope.shortenerror = 'Something went wrong. Could not create result for: '+url_to_summarize;
                            }
                        })
                }
                ;

            }
    ])
;
