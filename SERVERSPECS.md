# bluech Endpoints
All requests & responses follow a **general interface** correspondant to their nature.
The _**request**_ property of the **request** interface is unique for every instance.

<blockquote>

  #### Request General Interface
  ```json
    {
      "content_type": "string",
      "content_length": "number",
      "protocol": "string",
      "request": {
        "body": {"type": "object", "required": false},
        "params": {"type": "object", "required": false}
      } 
    }
  ```
  #### Response General Interface
  ```json
    {
      "proto": "string",
      "status": "number"
    }
  ```
</blockquote>
  
### Session
<details>
  <summary>Signin</summary>

  #### Request
  ```json
    {
      // ...
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
  #### Response
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
</details>
  
<details>
<summary>Signout</summary>

#### Request
  ```json
    {
      // ...
      "protocol": "signout",
      "request": {}
    }
  ```
#### Response
  ```json
    {
      "proto": "signout_success",
      "status": 200
    }
  ```
</details>
  
### User

<details>
<summary>Edit Nickname</summary>

#### Request
  ```json
    {
      // ...
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
#### Response
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
</details>
  
### Message
<details>
<summary>New Message</summary>

#### Request
  ```json
    {
      // ...
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
#### Response
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
</details>

<details>
<summary>Edit Message</summary>

#### Request
  ```json
    {
      // ...
      "protocol": "edit_message",
      "request": {
        "body": {
          "message": {"description": "string"}
        },
        "params": {"id": "number"}
      } 
    }
  ```
#### Response
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
</details>
  
<details>
<summary>All Messages per Chatroom</summary>

#### Request
  ```json
    {
      // ...
      "protocol": "all_messages",
      "request": {
        "params": {"recipient": "number", "page": {"type": "number", "required": false}}
      } 
    }
  ```
#### Response
  ```json
    {
      "status": 200,
      "proto": "all_messages",
      "messages": [
        {
          "id": "number",
          "description": "string",
          "is_edited": "boolean",
          "sender": "number",
          "sent_date": "string",
          "last_update": "string"
        },
        ...
      ] 
    }
  ```
</details>

<details>
<summary>Remove Message</summary>

#### Request
  ```json
    {
      // ...
      "protocol": "remove_message",
      "request": {
        "params": {"id": "number"}
      } 
    }
  ```
#### Response
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
</details>
  
### Error Response Contexts
<details>
<summary>Active Record Error</summary>

#### <a id="ARE">ActiveRecordError</a>
  ```json
    {
      "proto": "active_record_error",
      "status": 501,
      "message": "Active Record operation failure"
    }
  ```
</details>
  
<details>
<summary>Bad Request Error</summary>

#### <a id="BR">BadRequest</a>
  ```json
    {
      "proto": "invalid_request",
      "status": 400,
      "message": "Bad Request"
    }
  ```
</details>
  
<details>
<summary>Unauthorized Error</summary>

#### <a id="UA">Unauthorized</a>
  ```json
    {
      "proto": "signin_failure",
      "status": 401,
      "message": "Unauthorized"
    }
  ```
</details>
  
<details>
<summary>Internal Error</summary>

#### <a id="IE">InternalError</a>
  ```json
    {
      "proto": "internal_error",
      "status": 500,
      "message": "Internal Error"
    }
  ```
</details>
  
<details>
<summary>Resource Not Changed Error</summary>

#### <a id="RNC">ResourceNotChanged</a>
  ```json
    {
      "proto": "resource_not_changed",
      "status": 304,
      "message": "Resource was already up to date."
    }
  ```
</details>
  
<details>
<summary>Resource Not Found Error</summary>

#### <a id="RNF">ResourceNotFound</a>
  ```json
    {
      "proto": "resource_not_found",
      "status": 404,
      "message": "Resource Not Found"
    }
  ```
</details>
