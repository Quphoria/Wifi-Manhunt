# Wifi Manhunt

## Hardware

ESP8266

Used module: `NodeMCU 1.0 (ESP-12E Module)`

## IMPORTANT

**Make sure all the access points on the backend wifi network operate on the same channel as the clients all need to be operating on the same channel**  

This is to increase scanning speed by only scanning 1 channel

## Wifi Manhunt Python Server

### Creating the virtual environment
To create an instance of the server:  

1. Open a terminal in the `server` directory

2. Create a Python 3.9 virtual environment using  
    ```bash
    python -m venv env
    ```

3. Enter the virtual environment using  

    > Windows: `.\env\Scripts\activate`  

    > Bash: `./env/bin/activate`  

4. Install the required dependencies using
    ```bash
    pip install -r requirements.txt
    ````

### Running the server

1. Open a terminal in the `server` directory

2. Enter the virtual environment using  

    > Windows: `.\env\Scripts\activate`  

    > Bash: `./env/bin/activate`  

3. Run the server using
    ```bash
    python websocket-api.py
    ````

## Wifi Manhunt Webserver

To access the configuration website run `startweb.bat` or `startweb.sh` in the `web` directory

This uses `python -m http.server 8000` to create a local webserver located at http://localhost:8000

### Changing the api url

If you change the url/port of the api you will need to change the corresponding variable in `web/js/game.js`

You will want to change this line at the top of the file with the new api url you have set
```js
const api_url = "http://localhost:8080";
```