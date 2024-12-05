#!/bin/bash

docker compose up --build -d

echo "Wait a little (5 seconds)"
sleep 5

test_count=20
url="http://localhost:8011/message"
total_time=0

for ((i=1; i<=test_count; i++)); do
    start_time=$(date +%s.%N)

    curl --location $url --header 'Content-Type: application/json' --data '{"user_alias": "user_example","message": "msg_example"}'

    end_time=$(date +%s.%N)

    elapsed_time=$(echo "$end_time - $start_time" | bc)
    total_time=$(echo "$total_time + $elapsed_time" | bc)

    echo -e "\nRequest $i: Time: $elapsed_time seconds"
done

echo ""
average_time=$(echo "$total_time / $test_count" | bc -l)
echo "Average time: $average_time seconds"

docker compose down