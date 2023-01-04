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
      $ cd <PROJECT_DIRECTORY>
      
      $ python -m pip install -r requirements.txt
      
      $ python run.py
      
      > run server -p 8090 --debug <BOOLEAN> -d postgresql -u <DB_USER> -pwd <DB_PASSWORD>
    ```
  - __For `docker` users__
    ```shell
      $ docker build -t bluech:test-run .

      $ docker run -it bluech:test-run
      
      > run server -p 8090 --debug <BOOLEAN> -d postgresql -u <DB_USER> -pwd <DB_PASSWORD>
    ```

### Tests

To run pre-defined test units, run the below from the app `core shell`
  ```shell  
    > run tests
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
