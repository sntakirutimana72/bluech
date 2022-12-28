# bluech

An chatting app designed to handle multi users, threaded, and other complex forms of converstions. It supports media attachements, video & audio calls, text messages, and continuous notifications through its built-in push notification features.


## Technologies

### Frameworks

- GIL
- pyPDF2
- python-docx
- Asyncio
- Sockets
- PostgreSQL
- Python

### Tools & Methods

- Git
- GitHub
- Gitflow
- Heroku


# Get Started

To get started using this app, you must first

- Have a working computer with of `Linux` or `MS DOS` operating system distribution.
- Install `vs code` editor. You can install the latest version using this [link]().
- Install `python >= 3.9` in your local system. You can follow instructions found on this [website]().
- Clone this project repo using this [link](../../).
- Start app by running the below commands

  - __For `non-docker` users__
    ```shell
      $ python -m pip install -r requirements.txt
      
      > run server -p 8090 --debug <BOOLEAN> -d postgresql -u <DB_USER> -pwd <DB_PASSWORD>
    ```
  - __For `docker` users__
    ```shell
      $ docker build -t bluech:test-run .

      $ docker run -it bluech:test-run
      
      > run server -p 8090 --debug <BOOLEAN> -d postgresql -u <DB_USER> -pwd <DB_PASSWORD>
    ```

### Tests

To run pre-defined test units, do
```shell    
  > run tests
```
### 
