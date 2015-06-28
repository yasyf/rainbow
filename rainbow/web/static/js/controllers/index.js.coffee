FlaskStart.controller 'IndexCtrl', ['$scope', '$timeout', ($scope, $timeout) ->
  $scope.data = {}
  $scope.lastEvents = []
  $scope.markers = []
  $scope.bounds = new google.maps.LatLngBounds()

  initMap = ->
    $scope.map = new google.maps.Map $('#map-canvas')[0],
      center:
        lat: 37.580254
        lng: -122.343750
      zoom: 13

  populateMap = (events, oldEvents) ->
    return if events is oldEvents or _.isEqual(events, oldEvents)
    return unless $scope.map?

    uuids = _.map events, 'group_id'

    if _.isEqual($scope.lastEvents, uuids)
      return

    $scope.lastEvents = uuids

    _.each $scope.markers, (marker) ->
      marker.setMap(null)

    $('li').remove()

    $scope.markers = _.map events, (event) ->
      marker = new google.maps.Marker
        position: new google.maps.LatLng(event.location.latitude, event.location.longitude)
        map: $scope.map
        title: event.title
      $scope.bounds.extend marker.getPosition()
      link = $('<a>').text(event.title).click ->
        marker.getMap().panTo(marker.getPosition())
      $('#events-list').append($('<li>').append(link))
      infoWindow = new google.maps.InfoWindow
        content: event.description or event.location.value or event.title
      google.maps.event.addListener marker, 'click', ->
        infoWindow.open marker.getMap(), marker
      marker

    $scope.map.fitBounds $scope.bounds

  $(document).ready ->
    initMap()
    navigator?.geolocation.getCurrentPosition (position) ->
      $timeout ->
        $scope.map.panTo new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
        $scope.data.lat = position.coords.latitude
        $scope.data.lng = position.coords.longitude

  pollForEvents = (id, deferred = undefined) ->
    unless deferred?
      deferred = $.Deferred()
    $.get("/api/calendar/#{id}.json").then (response) ->
      if response.events.length > 0
        deferred.notify(id, response.events)
        timeout = 60000
      else
        timeout = 500

      $timeout ->
        pollForEvents(id, deferred)
      , timeout
    deferred.promise()

  $scope.$watch 'data.events', populateMap

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
      .progress (id, events) ->
        $timeout ->
          $scope.data.events = events
          $scope.data.calendarURL = "https://#{document.location.host}/api/calendar/#{id}.vcs"

]
