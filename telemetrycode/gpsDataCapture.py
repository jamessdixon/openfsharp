import gps
import datetime

def formatReport(report):
    if hasattr(report,'time')  & hasattr(report,'speed'):
        return ("\n" +
        str(report.time) +
        "," + str(report.lat) +
        "," + str(report.lon) +
        "," + str(report.alt) +
        "," + str(report.speed))

def getFileName():
    now = datetime.datetime.now()
    return ("gpsdata_" +
    str(now.year) +
    str(now.month) +
    str(now.day) +
    str(now.hour) +
    str(now.minute) +
    ".csv")

session = gps.gps("localhost","2947")
session.stream(gps.WATCH_ENABLE)
targetFile = open(getFileName(),"w")
while True:
    try:
        report = session.next()
        if report['class'] == 'TPV':
            output = formatReport(report)
            targetFile.write(output)
    except KeyError: pass
    except KeyboardInterrupt:
        targetFile.close()
        print "closing program" 
        quit()
    except StopIteration:
        session = None
        print "GPSD has terminated" 

            
