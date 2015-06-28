FlaskStart.controller 'IndexCtrl', ['$scope', '$timeout', ($scope, $timeout) ->
  $scope.data = {}

  $(document).ready ->
    navigator?.geolocation.getCurrentPosition (position) ->
      $timeout ->
        $scope.data.lat = position.coords.latitude
        $scope.data.lng = position.coords.longitude

  pollForEvents = (id, deferred = undefined) ->
    unless deferred?
      deferred = $.Deferred()
    $.get("/api/calendar/#{id}.json").then (response) ->
      if response.events.length > 0
        deferred.resolve(id, response.events)
      else
        $timeout ->
          pollForEvents(id, deferred)
        , 500
    deferred.promise()

  $scope.$watch 'data.docURL', (newDocURL, oldDocURL) ->
    if newDocURL and newDocURL isnt oldDocURL
      $scope.data.calendarURL = "Loading..."
      $.post '/api/calendar',
        url: newDocURL
        type: 'google_docs'
        lat: $scope.data.lat
        lng: $scope.data.lng
      .then (response) ->
        pollForEvents(response.id)
      .then (id, events) ->
        $timeout ->
          $scope.data.events = JSON.stringify events, null, 2
          $scope.data.calendarURL = "https://#{document.location.host}/api/calendar/#{id}.vcs"

]
