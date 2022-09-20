from datadog import initialize, api
from time import time
from datetime import datetime
from csv import writer

options = {'api_key': 'b83cf3130bd47ee96695c66661ef702b',
           'app_key': 'aae2c6d1c3a402791d5f4448d4c8c61c2896a4e8'}
query = "aws.rds.cpuutilization{host:db-CSCVBFEHHS4HEJXTV6CUDPGJGI}"  # Enter the metric you want, see your list here: https://app.datadoghq.com/metric/summary.
                                                                      # Optionally, enter your host to filter the data, see here: https://app.datadoghq.com/infrastructure
daysToGrab = 30

def getresults(apiInfo, daysBack):
  initialize(**apiInfo)

  end = int(time() - (daysBack*24*3600))  # Specify the time period over which you want to fetch the data in seconds
  start = end - 86400 # End -24hrs in seconds (24*60*60)

  return api.Metric.query(start=start, end=end, query=query)

header = ['identifier', 'timestamp', 'cpuusage']
csvOutput = []  # List container for csv output data
csvOutput.append(header)

for days in range(0, daysToGrab+3):  # Loop through, offsetting the days until it works it's way back to the earliest day to grab
  daysResults=getresults(options,days)
  for dataPoint in range(0, len(daysResults['series'][0]['pointlist'])):  # Loop through the day, pulling data and formatting it
    identifier=daysResults['series'][0]['scope']
    timeStamp=datetime.fromtimestamp(daysResults['series'][0]['pointlist'][dataPoint][0]/1000).strftime("%d/%m/%Y, %H:%M:%S")
    cpuUsage=daysResults['series'][0]['pointlist'][dataPoint][1]
    csvOutput.append([identifier,timeStamp,cpuUsage]) # Once formatted, add it to the to be outputted list

with open('output.csv', 'w', newline='') as file:  # Open the file, write the data.
  writer = writer(file)
  writer.writerows(csvOutput)
