# Assignment 9

In this assignment we implemented event-driven system using pipes-and-filters pattern
and message brokers (in this case, RabbitMQ).

[DEMO VIDEO](https://www.youtube.com/watch?v=28hK_swa5Bk)

## Implementation on top of pipes-and-filters

The implementation of pipes-and-filters is in the `rest-api-pipes-and-filters`
directory. Mainly, it is a single service that can be started using a single `main.py`
file. 

The implementation of different processes-filters is in the `filters` subdirectory.

This entire service requires `.env` file to successfully be started with docker compose.

## Implementation with message brokers

Different services from this implementation are on different directories with
corresponding names
- `filter-service`
- `screaming-service`
- `publish-service`
- `rabbitmq`
- `rest-api`

These services can also be started with single 
docker compose from the root of the project.

## Performance testing

We implemented performance testing allowing us to get a time to process a single request.

Process a single request — time from receival a JSON body until sending an email. In order to implement
that we added a new RabbitMQ topic / IPC Queue to allow publisher service "notify" a root endpoint about
successfull processing of a request. It is enabled only in performance testing mode.

`performance-test.sh` script starts all the necessary services, waits some time until startup, and
sends several messages to `/message` endpoint. During all the process it measures total time required for
request processing and prints an average.

In order to start performance test, needed to provide `.env` file with `PERFORMANCE_TEST=true` variable.
Both services can be started from the same .sh file

### Results interpretation

As one can see from the `.logs` file, the implementation of system with pipes-and-filters is insignificantly faster than RabbitMQ one. This can be a consequence of direct usage of IPC primitives instead of web-services (RabbitMQ).

However, results can be understood in other way. The implementation via RabbitMQ is slightly inferior in performance to the implementation via pipes-and-filters. But at the same time it provides much more flexibility and scalability through easy deployment of new queues, connection to them, replication. Therefore, this option is more preferable in the industry.


