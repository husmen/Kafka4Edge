# Kafka4Edge
Demonstrating Data Offloading for Digital Twins with Kafka - Project for  521290S Distributed Systems, Spring 2023, @unioulu

## How-to

Run the main and edge clusters:
NOTE: ALL COMMANDS ARE FOR LINUX DISTRIBUTION
```bash
docker-compose -f docker-compose-main.yml up -d
docker-compose -f docker-compose-edge.yml up -d --build --force-recreate
```

Make sure kafka-connect has started by checking logs (it'll take 30/40 seconds)
```bash
docker logs kafka-connect
```

After kafka-connect has started, run the following command to configure mongoDB as the sink for our kafka cluster
```bash
curl -d @config/connect-mongodb-sink.json -H "Content-Type: application/json" -X POST http://localhost:8083/connectors
```

Then check:
- Kafka Producer Web API on [http://localhost:8000/docs](http://localhost:8000/docs).
- MongoDB Client on port 3000 [http://localhost:3000](http://localhost:3000/).
- Grafana on [http://localhost:4000](http://localhost:4000).

When opening grafana: 
- Enter `admin` as username and password
- Go to Configurations -> Data-Source -> Add Data Source, then select prometheus
- Enter `http://prometheus:9090` in the URL, Click Save & Test


To bring everything down:
```bash
docker-compose -f docker-compose-main.yml down
docker-compose -f docker-compose-edge.yml down
```

## TODO
- [x] Kafka cluster configuration
- [X] Kafka edge node configuration, to join main cluster
- [x] Simple Producer
- [ ] Simple Consumer
- [x] MQTT Source
- [x] MongoDB Sink
- [x] Prometheus Monitoring
- [x] Grafana Visualization
- [X] Multithreaded Producer(s), to simulate multi sensor nodes and larger data loads
- [ ] Benchmarking, [more info](https://www.ericsson.com/4a492d/assets/local/reports-papers/ericsson-technology-review/docs/2021/xr-and-5g-extended-reality-at-scale-with-time-critical-communication.pdf)
- [ ] Attach to ditto, maybe?

## References
-
