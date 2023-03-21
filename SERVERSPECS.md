# bluech Server Endpoints Specs
All requests mirror the **general interface** only the _**request**_ property is unique for each instance.

For all requests to server, the followings are required for successful processing

### General Interfaces
+ Request
  ```json
    {
      "content_size": "string",
      "content_length": "number",
      "protocol": "string",
      "request": {
        "body": {"required": false},
        "params": {"required": false}
      } 
    }
  ```
+ Response
  ```json
    {
      "proto": "string",
      "status": "number"
    }
  ```
  
### Session Interfaces

#### Signin
+ Request
  ```json
    {
      "request": {
        "body": {
          "user": {
            "email": "string",
            "password": "string"
          }     
        }
      }
    }
  ```
+ Success Response
  ```json
    {
      "proto": "signin_success",
      "status": 200,
      "user": {
        "id": "number",
        "email": "string",
        "nickname": "string"
      } 
    }
  ```
+ BadRequest Response
  ```json
    {
      "proto": "invalid_request",
      "status": 400,
      "message": "Bad Request"
    }
  ```
+ Unauthorized Response
  ```json
    {
      "proto": "signin_failure",
      "status": 401,
      "message": "Unauthorized"
    }
  ```
  
#### Signout
+ Request
  ```json
    {
      "request": {}
    }
  ```
+ Success Response
  ```json
    {
      "proto": "signout_success",
      "status": 200
    }
  ```
  
### Users' Interfaces

#### Edit Nickname
+ Request
  ```json
    {
      "request": {
        "body": {
          "user": {
            "nickname": "string"
          }   
        }
      }
    }
  ```
+ Success Response
  ```json
    {
      "proto": "edit_username_success",
      "status": 200,
      "user": {
        "id": "number",
        "email": "string",
        "nickname": "string"
      } 
    }
  ```
+ Resource Not Changed Response
  ```json
    {
      "proto": "resource_not_changed",
      "status": 304,
      "user": {
        "id": "number",
        "email": "string",
        "nickname": "string"
      } 
    }
  ```
