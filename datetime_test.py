import datetime

mytime = '2018-04-02T00:00:00.000+02:00'
timelist = [int(mytime[0:4]), int(mytime[5:7]), int(mytime[8:10]),
            int(mytime[11:13]), int(mytime[14:16]), int(mytime[17:19])]

# print(timelist)
#
# print(datetime.datetime(*timelist))

tod = datetime.date.today()
print()