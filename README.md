# bluech

**bluech** is a chat-app designed to handle multi users, threaded, and other complex forms of chatting. 
The idea is to support media attachments, video & audio calls, text messages, and continuous notifications through its built-in push notification features.
Currently, it only supports text messaging and one-on-one single threaded user chat.


## Technologies

### Built with

- Python (v3.10)
- Postgres

### Tools & Methods

- Git
- GitHub
- Gitflow
- docker


# Get Started
To get started using this app, you must first

- Have a working computer with of `MS Windows 10` (or above) os.
- Install `PyCharm` editor. You can install the latest version using this [link]().
- Install `python==3.10` in your local system. You can follow instructions found on this [website]().
- Install `postgres` database with a user as `postgres` and password as `postgres`.
- Clone this project repo using this [link](../../).
  - Start the app by running the below commands from the terminal:
    - __For `non-docker` users__
      ```shell
        $ cd <PROJECT_DIRECTORY>
      
        $ python -m pip install --no-cache-dir -r requirements.txt
      
        $ python run.py
      ```
    - __For `docker` users__
      ```shell
        $ docker build -t bluech .

        $ docker run bluech
  
        $ docker ps

        $ docker exec -it <bluech_IMAGE_UID> /bin/bash

        $ service postgresql start
  
        $ su postgres
  
        $ psql
  
        $ \password postgres;
        $ \q
  
        $ service postgresql reload
      
        $ python3.10 run.py
      ```

### Tests
To run pre-defined test units, run the below from command line
  + __For `non-docker` users__
     ```shell  
       $ pytest -q --disable-warnings
        
       OR
        
       $ pytest --disable-warnings
     ```
  + __For `docker` users__
     ```shell  
       $ python3.10 -m pytest -q --disable-warnings
        
       OR
        
       $ python3.10 -m pytest --disable-warnings
     ```


## Authors

👤 **Steve**

- GitHub: [@sntakirutimana72](https://github.com/sntakirutimana72/)
- LinkedIn: [steve-ntakirutimana](https://www.linkedin.com/in/steve-ntakirutimana/) 

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](../../issues/).

## Show your support

Give a ⭐️ if you like this project!

## Acknowledgments

- Devs Communities for great free and resourceful articles.

## 📝 License

This project is [MIT](./LICENSE) licensed.
