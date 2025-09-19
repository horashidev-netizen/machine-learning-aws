Our test service will make two separate calls to the API Gateway invoke URL. The first call will be a GET request to the /vehicles URL to retrieve all vehicles. The second call will be a GET request to /vehicles/{id} to retrieve the details for a single vehicle.

Call one: GET /vehicles
{
 [ { id: 1, ... }, { id:2, ...} ]
}

Call two: GET /vehicles/1
{"id": "1", "type": "bike", "available": "true"}

Enter your API Gateway URL in the test validation screen to confirm. Include /vehicles at the end of the URL.