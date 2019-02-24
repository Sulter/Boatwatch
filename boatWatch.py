#!/usr/bin/python3
import ctypes
import os
import bs4
import time
import csv
import matplotlib
matplotlib.use('Agg')
import pylab
import datetime

timeInterval = 10

class DHT22():

  lib = ctypes.cdll.LoadLibrary(os.path.dirname(os.path.realpath(__file__)) + "/dht22.so")
  htmlFilePath = "/var/www/html/index.html"
  dataFilePath = "/var/www/html/data.csv"
  dataPlotPath = "/var/www/html/plot.png"

  def updateHtmlFile(self, temp, hum, timeStamp, file = htmlFilePath):
    with open(file) as inf:
      txt = inf.read()
      soup = bs4.BeautifulSoup(txt, features="html5lib")

    soup.find(id="tmp").string.replace_with(str(temp) + "C")
    soup.find(id="humidity").string.replace_with(str(hum) + "%")
    soup.find(id="time").string.replace_with(time.asctime(time.localtime(timeStamp)))
    # save the file again
    with open(file, "w") as outf:
      outf.write(str(soup))

  def updateDataFile(self, temp, hum, time, file = dataFilePath):
    if not os.path.isfile(file):
      with open(file, 'w') as the_file:                                                                                                                                                                              
        the_file.write("Temperature (C), humidity (%), time (unix)\n")      
    with open(file, 'a') as the_file:
      the_file.write(str(temp) + ", " + str(hum) + ", " + str(time) + "\n")

  def readDHT22(self):
    t = ctypes.c_float()
    h = ctypes.c_float()
    ret = self.lib.read_dht22(ctypes.byref(t), ctypes.byref(h))
    t = t.value
    h = h.value
    return {"status": ret, "temp": t, "hum": h, "time": time.time()}

  def printSensor(self):
    sensData = self.readDHT22()
    if sensData["status"] == 1:
      print("temp: " + str(sensData["temp"]) + "C")
      print("humidity: " + str(sensData["hum"]) + "%")
    else:
      print("Invalid sensor data")

  def updatePlotFile(self, csvFile = dataFilePath, imageFile = dataPlotPath):
    temp = []
    humidity = []
    time = []

    with open(csvFile,'r') as csvfile:
      plots = csv.reader(csvfile, delimiter=',')
      firstRow = True
      for row in plots:
        if firstRow is False:
          temp.append(float(row[0]))
          humidity.append(float(row[1]))
          time.append(datetime.datetime.fromtimestamp(float(row[2])))
        else:
          firstRow = False

      pylab.figure(figsize=(15,8))
      pylab.xticks(rotation=15)

      ax=pylab.gca()
      xfmt = matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M')
      ax.xaxis.set_major_formatter(xfmt)

      pylab.plot(time, temp, 'r', label='Temperature C')
      pylab.plot(time, humidity, 'b', label='Humidity %')
      pylab.legend(loc='best')


      pylab.savefig(imageFile, dpi = 100)
      pylab.close('all')

if __name__ == "__main__":
  dht22 = DHT22()
  while 1:
    sensData = dht22.readDHT22()
    if sensData["status"] == 1:
      dht22.updateHtmlFile(round(sensData["temp"], 2), round(sensData["hum"], 2), sensData["time"])
      dht22.updateDataFile(sensData["temp"], sensData["hum"], sensData["time"])
      dht22.updatePlotFile()
    time.sleep(timeInterval)
