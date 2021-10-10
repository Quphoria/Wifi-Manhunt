// Template config file
// Edit this file with the correct details
// and rename it to "config.h"

#ifndef __CONFIG_H__
#define __CONFIG_H__

// Backend wifi credentials
#define BaseWiFiSSID "backend-wifi-ssid"
#define BaseWiFiPass "backend-wifi-password"

// Prefix for game networks
#define GamePrefix   "game-"

// Api server address
#define WebsocketServer "ws://192.168.11.182:8765/"

// The softAP will have to use the same channel as the
// backend network as it has only 1 hardware channel
// This will dynamically change with the channel of the backend network
// Please make sure all access points of the backend network
// Operate on the same channel

#endif