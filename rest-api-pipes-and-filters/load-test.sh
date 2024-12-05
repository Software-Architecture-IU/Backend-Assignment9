#!/bin/bash

docker compose up -d

test_count=10
url="http://localhost:8011/message"
total_time=0

for ((i=1; i<=test_count; i++)); do
    json_data=$(jq -n --arg user_alias "user_$i" --arg message "Message number $i" '{user_alias: $user_alias, message: $message}')

    start_time=$(date +%s.%N)

    curl --location 'http://localhost:8011/message' --header 'Content-Type: application/json' --data '{"user_alias": "user_example","message": "msg_example"}'

    end_time=$(date +%s.%N)

    elapsed_time=$(echo "$end_time - $start_time" | bc)
    total_time=$(echo "$total_time + $elapsed_time" | bc)

    echo "Request $i: Time: $elapsed_time seconds"
done

echo ""
average_time=$(echo "$total_time / $test_count" | bc -l)
echo "Average time: $average_time seconds"

