# stcp_api

An unofficial API for the public bus system in Porto, Portugal, STCP (Serviço de Transportes Coletivos do Porto).

Since STCP does not provide its users with a freely accessible API to check the departure times in real time, I've decided to sniff the HTTP requests made by the SMSBus app, available for Windows. This app, developed by STCP themselves, communicates with a real-time server using an uid. This can easily be identified due to the lack of encrypted communication between client and server. Using this uid, one can simulate the app and send an HTTP request and retrieve the departure times, as well as a collection of all stops and lines in the whole service network. It provides the user with real-time data about the time it will take for a bus of a certain line to arrive at said stop. 

The api consists of the following functions, which can be used to access all real-time data about the times of the buses: 
- getLines() - Returns all the lines of the bus service.
- getStops(line) - Returns the stops for a particular line.
- getTimes(stop) - Returns the time until the next departures from a particular stop.

The file capture.py contains an application of the api to check whether a bus has passed a certain stop, adding it to a sqlite database (capture.db). It currently cycles over all stops of the whole network and checks whether a bus has passed the stop. Using that I'm planning on building a program that reliably predicts when a given bus will arrive at a certain stop.

Required Python libraries:
  - Requests 
  - SQLite3
  - Multiprocessing
  
