#!/bin/bash

# accept an argument that is the name of your lambda function
# if no argument is provided, prompt for the name of your lambda function
# if the lambda function does not exist, exit with an error message

# get the argument
lambda_function_name=$1

# if no argument was provided, prompt for the lambda function name
if [ -z "$lambda_function_name" ]
then
  echo "Enter the name of your lambda function:"
  read lambda_function_name
fi


start_time=$(date +%s)

while true
do
  for i in {1..6}
  do
    if [ $i -eq 1 ]; then
      aws lambda invoke --function-name $lambda_function_name outputfile.txt
    fi

    current_time=$(date +%s)
    elapsed_time=$(expr $current_time - $start_time)
    elapsed_minutes=$(expr $elapsed_time / 60)

    echo "Elapsed time: $elapsed_minutes minutes"

    echo "Checking alarm states..."
    aws cloudwatch describe-alarms --alarm-name-prefix "alarmtest" --query 'MetricAlarms[*].[AlarmName,AlarmDescription,StateValue,StateUpdatedTimestamp]' --output table

    sleep 10
  done
done

