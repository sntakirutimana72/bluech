# bluech Release Note (v1.0)

+ Environment
  - Windows 11
  - Postgres 13
  + Python 3.10
    + Dependencies
      - bcrypt==4.0.1
      - peewee==3.16.0
      - schema==0.7.5
      - pytest==7.2.2
      - pytest-asyncio==0.20.3
      - psycopg2-binary==2.9.5
      - aiofiles==23.1.0
      - requests==2.28.2
      - pytest-mock==3.10.0

+ Error Contexts
  - _**Database**_: occurs at database level.
  + _**Validation**_: occurs at system level but during validation process.
    - Protocols
    - Request

+ Supported
  - Minimal logging at both system & database levels.
  - Asynchronous response (except database).
  - Connection with session supported which means users can sign in & out.
  - Sending messages supported (only for signed users).
  - Receiving messages supported (only for signed users).
  - Editing messages supported (only for signed users).
  - Deleting messages supported (only for signed users).
  - Editing user profile supported (only for signed users).
  - Database paginating supported while retrieving messages (only for signed users).

+ Unsupported
  - No customizable configuration files supported.
  - No advanced core runner introduced.
  - No advanced logging at both levels, database & system.
  - No real-time visualization.
  - No **_threaded chats_** supported.
  - No **_Channels/Chat-Groups_** supported.
  - No **_attachments_** supported.
  - No **_Emojis_** supported.
  - No **_audio/video_** calls supported.
  - No **_Ping/Pong_** signals like _typing_, _seen_, _read_, _etc.._ supported.
  - No **_ssl/Encrypted_** connection supported.
