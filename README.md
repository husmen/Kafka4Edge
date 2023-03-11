# Kafka4Edge
Demonstrating Data Offloading for Digital Twins with Kafka - Project for  521290S Distributed Systems, Spring 2023, @unioulu

## How-to

Run the cluster, remove `-d` to watch logs.

```bash
docker compose up -d --build
```

Then check web api on [http://localhost:8000/docs](http://localhost:8000/docs).

To run outside docker, comment out `producer-0` service in `docker-compose.yml` and run

```bash
python demo/producer.py
```

**N.B.** only second method is working for now

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
