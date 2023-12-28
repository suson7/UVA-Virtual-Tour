let directionsService;
let directionsRenderer;
let map;
let toursMap;
let locationsMap;

function initData(){
  toursMap = new Map()
  toursData.forEach(element =>{
    toursMap.set(element.pk,element)
  });
  locMap = new Map()
  locationsData.forEach(element => {
    locMap.set(element.pk,element)
  });
}

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: { lat: 38.0336, lng: -78.5080 },
    zoom: 12,
  });
   directionsService = new google.maps.DirectionsService();
   directionsRenderer = new google.maps.DirectionsRenderer({
    map: map,
  });

  option = toursData[0].pk;
  setWaypoints();
}

function setWaypoints() {
  const selectedTour = toursMap.get(Number(option));
  const waypoints = [];

  for (let i = 0; i < selectedTour.fields.locations.length; i++) {
    const pk = selectedTour.fields.locations[i];
    waypoints.push({ location: locMap.get(pk).fields.address });
  }
  updateDirections(waypoints);
} 

function updateDirections(waypoints) {
  const request = {
    origin: waypoints[0]['location'],
    destination: waypoints[waypoints.length-1]['location'],
    waypoints: waypoints,
    travelMode: google.maps.TravelMode.WALKING,
    optimizeWaypoints: true
  };

  // Request directions
  directionsService.route(request, function (result, status) {
    if (status === 'OK') {
      // Display the route on the map
      directionsRenderer.setDirections(result);
    } else {
      alert('Directions request failed due to ' + status);
    }
  });
}