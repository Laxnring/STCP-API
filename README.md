# stcp_api

An unofficial API for the public bus system in Porto, Portugal, STCP (Serviço de Transportes Coletivos do Porto).

Since SCTP does not provide its users with a freely accessible API to check the departure times in real time, I've decided to sniff the HTTP requests made by the SMSBus app, available for Windows. This app, developed by STCP themselves, communicates with a real-time server using an uid. This can easily be identified due to the lack of encrypted communication between client and server. Using this uid, one can send an HTTP request and retrieve the departure times, as well as a collection of all stops and lines in the whole service. 

There are three functions in the python file: 
- getLines() - Returns all the lines of the bus service.
- getStops(line) - Returns the stops for a particular line.
- getTimes(stop) - Returns the time until the next departures from a particular stop.
