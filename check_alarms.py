import argparse
import boto3
import tkinter as tk
from tkinter import ttk
import datetime
from threading import Thread, Event
import time
import queue

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--lambda_name', help='The name of the lambda function to be invoked', default='')
args = parser.parse_args()

# create AWS clients
cloudwatch = boto3.client('cloudwatch')
lambda_client = boto3.client('lambda')

root = tk.Tk()

# flag to control lambda invocation
invoke_lambda_flag = Event()
invoke_rate = 20 
lambda_response = queue.Queue()

def get_alarm_data():
    alarms = cloudwatch.describe_alarms(AlarmNamePrefix='alarmtest')
    alarm_data = [
        {
            'AlarmName': alarm['AlarmName'],
            'StateValue': alarm['StateValue'],
            'StateReason': alarm['StateReason'],
            'LastModified': alarm['AlarmConfigurationUpdatedTimestamp'].strftime('%Y-%m-%d %H:%M:%S'),
        }
        for alarm in alarms['MetricAlarms']
    ]
    return alarm_data

def populate_table():
    alarm_data = get_alarm_data()
    for alarm in alarm_data:
        tree.insert('', 'end', values=(alarm['AlarmName'], alarm['StateValue'], alarm['StateReason'], alarm['LastModified']))

    # Adjust column widths to the max length of data
    for idx, column in enumerate(tree['columns']):
        max_width = max([len(str(alarm[column])) for alarm in alarm_data])
        tree.column(column, width=max_width*8)

    # Update status bar
    status_label.config(text=f'Last updated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    root.after(1000, refresh_table)

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    populate_table()

def lambda_invoker():
    while invoke_lambda_flag.is_set():
        try:
            response = lambda_client.invoke(FunctionName=args.lambda_name)
            lambda_response.put(response['Payload'].read().decode('utf-8'))
            time.sleep(invoke_rate)
        except Exception as e:
            print(f"Error invoking Lambda: {e}")

def update_lambda_status():
    while not lambda_response.empty():
        lambda_status = lambda_response.get()
        lambda_status_label.config(text=f'Lambda Response: {lambda_status} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        time.sleep(0.2)  # Add delay here
    root.after(1000, update_lambda_status)

def toggle_lambda_invocation():
    if invoke_lambda_flag.is_set():
        invoke_lambda_flag.clear()
        lambda_button.config(text="Start Lambda Invocation")
    else:
        invoke_lambda_flag.set()
        lambda_button.config(text="Stop Lambda Invocation")
        Thread(target=lambda_invoker).start()

root = tk.Tk()
tree = ttk.Treeview(root)

tree['columns'] = ('AlarmName', 'StateValue', 'StateReason', 'LastModified')
for col in tree['columns']:
    tree.heading(col, text=col)

# Add lambda control widgets
lambda_button = tk.Button(root, text="Start Lambda Invocation", command=toggle_lambda_invocation)
invoke_rate_entry = tk.Entry(root)
invoke_rate_entry.insert(0, '20')  # Default invoke rate

status_label = tk.Label(root, text='', bd=1, relief=tk.SUNKEN, anchor=tk.W)
lambda_status_label = tk.Label(root, text='', bd=1, relief=tk.SUNKEN, anchor=tk.W)

populate_table()

root.after(1000, update_lambda_status)

tree.pack()
lambda_button.pack()
invoke_rate_entry.pack()
status_label.pack(fill=tk.X)
lambda_status_label.pack(fill=tk.X)

root.mainloop()
