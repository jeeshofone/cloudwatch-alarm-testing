#!/bin/bash

start_time=$(date +%s)

while true
do
  aws lambda invoke --function-name alarmtest-HelloWorldLambdaFunction-byG45Vo1LM8d outputfile.txt

  current_time=$(date +%s)
  elapsed_time=$(expr $current_time - $start_time)
  elapsed_minutes=$(expr $elapsed_time / 60)

  echo "Elapsed time: $elapsed_minutes minutes"

  echo "Checking alarm states..."
  aws cloudwatch describe-alarms --alarm-name-prefix "alarmtest" --query 'MetricAlarms[*].[AlarmName,AlarmDescription,StateValue]' --output table

  sleep 60
done

