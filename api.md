# Websocket connection json data

## Response base template:
```json
{
    "status": integer,
    "content": null or object
}
```

## Status codes
| Status code |  Message              |
|-------------|-----------------------|
| 404         | Unknown request       |
| 400         | Invalid request       |
| 200         | Ok                    |
| 500         | Internal server error |

## Request json format
```json
{
    "method": string,
    "content": null or object
}
```

## Methods
| Method | Use                                   |
|--------|---------------------------------------|
| join   | Register client                       |
| cal    | Sends rssi value of server ap         |
| rssi   | Send rssi values                      |
| status | Gets state for client                 |

### join

Sends the client mac address to identify it

request content:
```json
{
    "mac": string
}
```

response content:
```json
null
```

### cal

Sends the rssi of all essids when the button is pressed

request content:
```json
{
    "mac": string,
    "signals": [
        {
            "essid": string,
            "rssi": integer
        }
    ]
}
```

response content:
```json
null
```

### rssi

Sends a list of essid's and their rssi

*Same request and response content as cal*

### status

request content: 
```json
{
    "mac": string
}
```

response content:
```json
{
    "alive": boolean,
    "game_running": boolean,
    "ready": boolean,
    "do_cal": boolean,
    "do_ident": boolean
}
```

When not ready and not in cal  
Flash LEDS On 1s Off 1s  

When in cal, heartbeat pattern (0.25s on 0.25s off 0.25s on 0.5s off)  
when button pressed, send cal message  

When game running and alive, LEDS on solid  
When ident, strobe pattern (0.1s on 0.1s off) until button pressed  


*do_ident is set to false after being read by the client*

## Web Methods

This is actually implemented using a slightly different rest api to make javascript programming easier

| Method   | Use                                   |
|----------|---------------------------------------|
| clients  | Gets list of clients                  |
| nick     | Sets the nickname for a client        |
| startcal | Starts the cal routine for a client   |
| ident    | Makes a client identify itself        |
| start    | Starts the game                       |
| stop     | Stops the game                        |
| state    | Gets the game state                   |

### clients

Returns list of clients

request content:
```json
null
```

response content:
```json
{
    "clients": [
        {
            "mac": string,
            "nick": string,
            "signals": [
                {
                    "essid": string,
                    "rssi": integer
                }
            ],
            "cal_rssi_threshold": integer,
            "alive": boolean
        }
    ]
}
```

### nick

Sets the nick with an associated client

request content:
```json
{
    "mac": string,
    "nick": string
}
```

response content:
```json
null
```

### startcal

Starts the cal process for a client

request content:
```json
{
    "mac": string
}
```

response content:
```json
null
```

### ident

Makes a client indentify itself with a strobe until its button is pressed (not available until cal complete for client)

### start

Starts the game

request content
```json
{
    "imposters": [
        mac strings
    ]
}
```

response content
```json
null
```

### stop

Stops the game

request content
```json
null
```

response content
```json
null
```

### state

Gets the state for the web interface

request content
```json
null
```

response content
```json
{
    "game_running": boolean,
    "clients": integer
    
}
```