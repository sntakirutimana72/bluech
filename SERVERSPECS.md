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
  
### Session

#### Signin
+ Request
  ```json
    {
      "protocol": "signin",
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
      "protocol": "signout",
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
  
### User

#### Edit Nickname
+ Request
  ```json
    {
      "protocol": "edit_username",
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
      "message": "Resource was already up to date."
    }
  ```
  
### Message

#### New Message
+ Request
  ```json
    {
      "protocol": "new_message",
      "request": {
        "body": {
          "message": {
            "description": "string",
            "recipient": "number",
            "reply_to": {"type": "number", "required": false}
          }
        }
      } 
    }
  ```
  + Response Success
    ```json
      {
        "status": 200,
        "proto": "new_message",
        "message": {
          "id": "number",
          "description": "string",
          "is_edited": "boolean",
          "sender": "number",
          "sent_date": "string",
          "last_update": "string"
        } 
      }
    ```

#### Edit Message
+ Request
  ```json
    {
      "protocol": "edit_message",
      "request": {
        "body": {
          "message": {"description": "string"}
        },
        "params": {"id": "number"}
      } 
    }
  ```
+ Response Success
  ```json
    {
      "status": 200,
      "proto": "edit_message",
      "message": {
        "id": "number",
        "description": "string",
        "is_edited": true,
        "sender": "number",
        "sent_date": "string",
        "last_update": "string"
      } 
    }
  ```
  
#### All Messages per Chatroom
+ Request
  ```json
    {
      "protocol": "all_messages",
      "request": {
        "params": {"recipient": "number", "page": {"type": "number", "required": false}}
      } 
    }
  ```
+ Response Success
  ```json
    {
      "status": 200,
      "proto": "all_messages",
      "messages": [{
        "id": "number",
        "description": "string",
        "is_edited": "boolean",
        "sender": "number",
        "sent_date": "string",
        "last_update": "string"
      }] 
    }
  ```
  
#### Remove Message
+ Request
  ```json
    {
      "protocol": "remove_message",
      "request": {
        "params": {"id": "number"}
      } 
    }
  ```
+ Response Success
  ```json
    {
      "status": 200,
      "proto": "remove_message",
      "benefactor": {
        "id": "number",
        "email": "string",
        "nickname": "string"
      } 
    }
  ```
