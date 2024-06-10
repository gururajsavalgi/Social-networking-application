
# Social Networking API

This project provides API for social networking application.

## How to start the application as Docker container.

Run below commands to start the application 

 docker build -t my-drf-app .

 docker run -p 8000:8000 my-drf-app



## API Reference
Import the postman collection named --> 'Postman-collection-for-DRF.postman_collection.json' at postman.

#### Register a user
```http
  POST /api/register/
```

| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `` {"username":"raghf", "email":"raghu@gmail.com",  "password":"1234","password2":"1234"}| `` | Register your new user by name and email  |

#### Search user by Query

```http
  POST /api/users/?search={{searchQuery}}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `searchQuery` | `string` | **Required**. Enter your searchQuery|

#### Send friend request by user id

```http
  POST /api/send-friend-request/{{friendRequestId}}/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `friendRequestId` | `string` | **Required**. Your user ID to send request |

#### List Friend Request

```http
  GET /api/friend-requests/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| ``      | `` | Lists friend request with their ID |

#### Accept friend request by Friend request ID

```http
  POST /api/accept-friend-request/{{acceptFrinedRequestById}}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `acceptFrinedRequestById`      | `string` | **Required**. Id of item to Accept friend request.**ID can be obtained from List Friend Request API**|


#### Reject friend request by Friend request ID
```http
  POST /api/decline-friend-request/{{rejectFriendRequestById}}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `rejectFriendRequestById`      | `string` | **Required**. Id of item to Reject friend request. **ID can be obtained from List Friend Request API**|

#### List Friends
```http
  GET friends/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| ``      | `` | Lists friends List |



## NOTE : We have few sample users kept in the ORM database for easier evaluation.