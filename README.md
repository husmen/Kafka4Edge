# Kafka4Edge
Demonstrating Data Offloading for Digital Twins with Kafka - Project for  521290S Distributed Systems, Spring 2023, @unioulu

## How-to

Run the main and edge clusters:

```bash
docker compose -f ./docker-compose-main.yml up -d
docker compose -f ./docker-compose-edge.yml up -d --build --force-recreate
```

Then check web API on [http://localhost:8000/docs](http://localhost:8000/docs).

## TODO
- [x] Kafka cluster configuration
- [X] Kafka edge node configuration, to join main cluster
- [x] Simple Producer
- [ ] Simple Consumer
- [X] Multithreaded Producer(s), to simulate multi sensor nodes and larger data loads
- [ ] Benchmarking, [more info](https://www.ericsson.com/4a492d/assets/local/reports-papers/ericsson-technology-review/docs/2021/xr-and-5g-extended-reality-at-scale-with-time-critical-communication.pdf)
- [ ] Attach to ditto, maybe?

## References
-
