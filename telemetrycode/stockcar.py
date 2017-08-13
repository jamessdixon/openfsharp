import RPi.GPIO as GPIO
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

GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.OUT)
GPIO.output(36,True)

GPIO.setup(38, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(38,GPIO.RISING,bouncetime=500)
isCapturing = False
while True:
    if isCapturing == True:
        try:
            report = session.next()
            if report['class'] == 'TPV':
                output = formatReport(report)
                targetFile.write(output)
                print(output)
        except KeyError: pass
        except KeyboardInterrupt:
            targetFile.close()
            print('closing program') 
            quit()
        except StopIteration:
            session = None
            print('GPSD has terminated') 

    if GPIO.event_detected(38):
        if isCapturing == False:
            print('capturing')
            GPIO.output(36,False)
            isCapturing = True
        else:
            print('not capturing')
            GPIO.output(36,True)
            targetFile.close()
            isCapturing = False
            

    
