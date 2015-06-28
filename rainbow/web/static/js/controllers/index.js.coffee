FlaskStart.controller 'IndexCtrl', ['$scope', '$timeout', ($scope, $timeout) ->
  $scope.data = {}

  pollForEvents = (id, deferred = undefined) ->
    unless deferred?
      deferred = $.Deferred()
    $.get("/api/calendar/#{id}.json").then (response) ->
      if response.events.length > 0
        deferred.resolve(id)
      else
        $timeout ->
          pollForEvents(id, deferred)
        , 500
    deferred.promise()

  $scope.$watch 'data.docURL', (newDocURL, oldDocURL) ->
    if newDocURL? and newDocURL isnt oldDocURL
      $scope.data.calendarURL = "Loading..."
      $.post '/api/calendar',
        url: newDocURL
        type: 'google_docs'
      .then (response) ->
        pollForEvents(response.id)
      .then (id) ->
        $timeout ->
          $scope.data.calendarURL = "http://#{document.location.host}/api/calendar/#{id}.vcs"

]
