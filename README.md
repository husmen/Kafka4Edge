# Kafka4Edge
Demonstrating Data Offloading for Digital Twins with Kafka - Project for  521290S Distributed Systems, Spring 2023, @unioulu

## How-to

Run the cluster, remove `-d` to watch logs.

```bash
docker compose up -d
```

Check MongoDB Client on port 3000 [http://localhost:3000](http://localhost:8000/docs).


## TODO
- [x] Kafka cluster configuration
- [ ] Kafka edge node configuration, to join main cluster
- [x] MQTT Source
- [x] MongoDB Sink
- [ ] Multithreaded Producer(s), to simulate multi sensor nodes and larger data loads
- [ ] Benchmarking, [more info](https://www.ericsson.com/4a492d/assets/local/reports-papers/ericsson-technology-review/docs/2021/xr-and-5g-extended-reality-at-scale-with-time-critical-communication.pdf)
- [ ] Attach to ditto, maybe?

## References
-
