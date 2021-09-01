import xlrd
import tkinter
import pytz


# from tkinter import messagebox
# from tkinter import *

class Supplier:
    def __init__(self, _name):
        self._name = _name
        self._sippCodes = list()
        self._file = None

    def add_sippCode(self, string: str):
        if len(string) != 4:
            print("invalid input")
            return

        for sip in self._sippCodes:
            if sip == string:
                print("already in")
                break
        else:
            self._sippCodes.append(string)

    def getName(self):
        return self._name

    def setFile(self, file: str):
        self._file = file

    def __str__(self):
        # string = self._name + " : "
        # for i in range(len(self._sippCodes)):
        #     string += self._sippCodes[i] + " "
        return self._name


class Country:
    def __init__(self, name, currency):
        self._name = name
        self._currency = currency
        self._suppliers: Supplier = list()
        self._stations = list()
        self._suppliers_station = list()

    def add_supplier(self, supplier: Supplier, file: str):
        for sup in self._suppliers:
            if sup == supplier:
                print("already in the list of suppliers")
                break
        else:
            self._suppliers.append(supplier)
            supplier.setFile(file)
            self.open_file()

    def add_station(self, station: str):
        for Station in self._stations:
            if Station == station:
                print("already in the general list of stations")
                break
        else:
            self._stations.append(station)

    # def get_suplier_station(self, station: str, supplier: Supplier):
    #     if not (station in self._stations and supplier in self._suppliers):
    #         print("Station and / or Supplier doesn't exists")
    #         return
    #     if supplier not in self._suppliers_station.keys():
    #         self._suppliers_station[supplier] = [station]
    #
    #         #    self._suppliers_station = sorted(self._suppliers_station.keys())
    #         print("successful entry2")
    #         return
    #     if station in self._suppliers_station.get(supplier):
    #         print("Station is already in the suppliers dictionary")
    #         return
    #     # must be a new station on existing key
    #     self._suppliers_station[supplier] = set(self._suppliers_station.get(supplier)).union({station})
    #     print("successful entry1")

    def open_file(self):
        book = xlrd.open_workbook(file)
        sheet = book.sheet_by_index(0)
        # sheet by name is also an option
        for row in range(2, sheet.nrows):
            self._suppliers_station.append(sheet.cell(row, 1).value)

        return

    def getData(self, supplier: Supplier, pu: str, do: str):
        book = xlrd.open_workbook(supplier._file)
        sheet = book.sheet_by_index(0)
        rowIndex = -1
        colIndex = -1
        val = -1
        for row in range(2, sheet.nrows):
            if (sheet.cell(row, 1).value == pu):
                rowIndex = row
                break

        for col in range(2, sheet.ncols):
            if (sheet.cell(0, col).value == do):
                colIndex = col
                break

        if rowIndex == -1 or colIndex == -1:
            return -1
        else:
            print(sheet.cell(rowIndex, colIndex).value)
            val = sheet.cell(rowIndex, colIndex).value
            if val is None:
                return -1
            else:
                return val

    def getAllSuppliers(self):
        return self._suppliers

    # def getAllSuppliersStation(self, sup: Supplier):
    #     return self._suppliers_station[sup]

    def getAllSuppliersStationSorted(self, sup: Supplier):
        return sorted(self._suppliers_station)

    def getName(self):
        return self._name

    def getCurrency(self):
        return self._currency

    # def getSupplier(self, i):
    #     return self._suppliers[i]

    def getSupplierFromName(self, str1: str):
        for supplier in self.getAllSuppliers():
            if supplier.getName() == str1:
                return supplier

    def __str__(self):
        # string = self._name + " :: "
        # for i in range(len(self._suppliers)):
        #     string += self._suppliers[i].__str__()
        return self.getName()


class Data:

    def __init__(self):
        self._countries: Country = list()
        self._toGoCountries = dict()

    def addCountry(self, country: Country):
        for country1 in self._countries:
            if country1 == country:
                print("already in the list of countries")
                break
        else:
            self._countries.append(country)
            self._toGoCountries[country] = [country]
            print("country added successfully")

    def getData(self, country: Country, supplier: Supplier, str1: str, str2: str):
        if country.getData(supplier, str1, str2):
            return country.getData(supplier, str1, str2)
        return None

    def addCountryToGo(self, countryFrom: Country, countryTo: Country, twoway=False):
        if countryFrom is countryTo:
            print("was already added when you entered the country")
            return
        if countryTo in self._toGoCountries[countryFrom]:
            print("is already is in the dictionary")
            return
        list1 = list()
        for supplier in countryFrom._suppliers:
            for supplier1 in countryTo._suppliers:
                if supplier is supplier1:
                    list1.append(supplier)

        if len(list1) == 0:
            print("not available")
            return
        else:
            self._toGoCountries[countryFrom] = list(set(self._toGoCountries.get(countryFrom)).union({countryTo}))

        if twoway == True:
            self.addCountryToGo(self, countryTo, countryFrom)

    def getAllCountries(self):
        return self._countries

    def getCountry(self, i):
        if i in range(len(self._countries)):
            return self._countries[i]

    def getCountryfromName(self, str1: str):
        for country in self._countries:
            if country.getName() == str1:
                return country

    def getCountryName(self, cou: Country):
        if cou in self._countries:
            return cou.getName()

    def getCountryCur(self, str1: str):
        for country in self._countries:
            if country.getName() == str1:
                return country.getCurrency()

    def getAllCountriesNames(self):
        return self._countries

    def getAllSuppliersStation(self, coun: Country, sup: Supplier):
        if coun in self.getAllCountries():
            return coun.getAllSuppliersStation(sup)
        return None

    def getAllSuppliersStationS(self, coun: Country, sup: Supplier):
        if coun in self.getAllCountries():
            return coun.getAllSuppliersStationSorted(sup)
        return None

    def getAllSuppliers(self, country: Country):
        if country in self.getAllCountries():
            return country.getAllSuppliers()
        return None

    def getSupplierFromName(self, country: Country, str1: str):
        return country.getSupplierFromName(str1)


class RunGUI:

    @staticmethod
    def start():
        # all buttons functions which are not in classes
        def run():
            str1 = mainWindowPickupStationChosentextvar.get()
            str2 = mainWindowDropoffStationChosentextvar.get()
            country = data.getCountryfromName(mainWindowPUCountryChosenTextVar.get())
            supplier = data.getSupplierFromName(country, mainWindowSupChosenVar.get())
            if mainWindowPickupStationChosentextvar != "" and mainWindowDropoffStationChosentextvar != "":
                val = Data.getData(data, country, supplier, str1, str2)
                if val is None:
                    res.set("Is not defined properly, check manually")
                    return
                val = int(val)
                if val == -1:
                    res.set("You can't do this combination")
                elif val == 0:
                    res.set("No drop off charge")
                else:
                    res.set("{} {} + tax".format(val, country.getCurrency()))
            else:
                # test = messagebox.
                res.set("ERROR")

        def clear():
            mainWindowPickupStationChosentextvar.set("")
            mainWindowDropoffStationChosentextvar.set("")
            res.set("")
            mainWindowSupChosenVar.set("")
            days.set("Not Calculated")
            if mainWindowSup.size() > 0:
                mainWindowSup.delete(0, mainWindowSup.size())
            if mainWindowPickupBoxList.size() > 0:
                mainWindowPickupBoxList.delete(0, tkinter.END)
            if mainWindowDropOffBoxList.size() > 0:
                mainWindowDropOffBoxList.delete(0, tkinter.END)
            mainWindowPUCountryChosenTextVar.set("")

        def dateCalc():
            if int(DropoffmonthSpin.get()) == 2 and int(DropoffdaySpin.get()) >= 29:
                days.set("no such date exist".capitalize())
                return
            if int(PickupmonthSpin.get()) == 2 and int(PickupdaySpin.get()) >= 29:
                days.set("no such date exist".capitalize())
                return
            tup = (4, 6, 9, 11)
            if int(DropoffmonthSpin.get()) in tup and int(DropoffdaySpin.get()) == 31:
                days.set("no such date exist".capitalize())
                return
            if int(PickupmonthSpin.get()) in tup and int(PickupdaySpin.get()) == 31:
                days.set("no such date exist".capitalize())
                return

            dropOffDate = pytz.datetime.date(int(DropoffyearSpin.get()),
                                             int(DropoffmonthSpin.get()),
                                             int(DropoffdaySpin.get()))
            pickUpdate = pytz.datetime.date(int(PickupyearSpin.get()),
                                            int(PickupmonthSpin.get()),
                                            int(PickupdaySpin.get()))

            delta = dropOffDate - pickUpdate
            daysNum = delta.days
            pickUptime = pytz.datetime.time(int(mainWindowPickupTimeHours.get()),
                                            int(mainWindowPickupTimeMinutes.get()))
            dropOfftime = pytz.datetime.time(int(mainWindowDropoffTimeHours.get()),
                                             int(mainWindowDropoffTimeMinutes.get()))
            carry = 0
            if dropOfftime.hour != pickUptime.hour:
                if dropOfftime.hour > pickUptime.hour:
                    carry += 1
            else:
                if dropOfftime.min > pickUptime.min:
                    carry += 1

            if daysNum >= 0:
                days.set("{0}".format(delta.days + carry))
            else:
                days.set("Choose a later pickup date or earilier drop off date")
                # def sel():
                #     mainWindowPUCountryChosenTextVar = mainWindowPickupCountryMenu.selection_own_get()
                # def setSupplier():

        def country_choose_toSup():
            cou = data.getCountryfromName(mainWindowPUCountryChosenTextVar.get())
            listA = cou.getAllSuppliers()
            if listA:
                mainWindowSupChosenVar.set("")
                if mainWindowSup.size() > 0:
                    mainWindowSup.delete(0, mainWindowSup.size())
                for k in range(len(listA)):
                    mainWindowSup.insert(tkinter.END, listA[k])

        def PU_choose_station():
            country = data.getCountryfromName(mainWindowPUCountryChosenTextVar.get())
            supplier = data.getSupplierFromName(country, mainWindowSupChosenVar.get())
            chosen = mainWindowPickupBoxList.curselection()
            mainWindowPickupStationChosentextvar.set(data.getAllSuppliersStationS(country, supplier)[chosen[0]])

        def DO_choose_station():
            country = data.getCountryfromName(mainWindowPUCountryChosenTextVar.get())
            supplier = data.getSupplierFromName(country, mainWindowSupChosenVar.get())
            chosen = mainWindowDropOffBoxList.curselection()
            mainWindowDropoffStationChosentextvar.set(data.getAllSuppliersStationS(country, supplier)[chosen[0]])

        def setSup():
            cou = data.getCountryfromName(mainWindowPUCountryChosenTextVar.get())
            chosen = mainWindowSup.curselection()
            sup = cou.getAllSuppliers()[chosen[0]]
            mainWindowSupChosenVar.set(sup)
            couSupStaList = data.getAllSuppliersStationS(cou, sup)
            if mainWindowPickupBoxList.size() > 0:
                mainWindowPickupBoxList.delete(0, tkinter.END)
            for station in couSupStaList:
                mainWindowPickupBoxList.insert(tkinter.END, station)
            if mainWindowDropOffBoxList.size() > 0:
                mainWindowDropOffBoxList.delete(0, tkinter.END)
            for station in couSupStaList:
                mainWindowDropOffBoxList.insert(tkinter.END, station)

        mainWindow = tkinter.Tk()
        mainWindow.title("National One Way Calculator")
        mainWindow.geometry('1280x960-4+10')

        mainWindowLabel = tkinter.Label(mainWindow, text="National One Way Calculator")
        mainWindowLabel.grid(row=0, column=0, columnspan=10)

        mainWindowPickupStationChosentextvar = tkinter.StringVar()
        mainWindowDropoffStationChosentextvar = tkinter.StringVar()
        mainWindowPUCountryChosenTextVar = tkinter.StringVar()
        mainWindowSupChosenVar = tkinter.StringVar()

        days = tkinter.StringVar()
        res = tkinter.StringVar()
        days.set("Not Calculated")
        # pick up data

        mainWindowPickupLabel = tkinter.Label(mainWindow, text="Pickup Data")
        mainWindowPickupLabel.grid(row=1, column=1, sticky='n')

        mainWindowPickupCountryLabel = tkinter.Label(mainWindow, text="Pickup country:")
        mainWindowPickupCountryLabel.grid(row=2, column=0, sticky='n')

        allCountries = tuple(data.getAllCountries())

        mainWindowPUCountryChosenOptionMenu = tkinter.OptionMenu(mainWindow, mainWindowPUCountryChosenTextVar,
                                                                 *allCountries).grid(row=2, column=1, sticky='wen')
        mainWindowDoCountryChosenEntry = tkinter.Entry(mainWindow,
                                                       textvariable=mainWindowPUCountryChosenTextVar).grid(row=2,
                                                                                                           column=4,
                                                                                                           sticky='wen')

        mainWindowPickupStationLabel = tkinter.Label(mainWindow, text="Pickup Station Name:")
        mainWindowPickupStationLabel.grid(row=3, column=0, sticky='n')

        mainWindowPickupBoxList = tkinter.Listbox(mainWindow)
        mainWindowPickupStationChosen = tkinter.Entry(mainWindow, textvariable=mainWindowPickupStationChosentextvar)
        mainWindowPickupStationChosen.grid(row=6, column=1, sticky='ew')

        mainWindowPickupBoxList.grid(row=3, column=1, sticky='nsew', rowspan=2)
        mainWindowPickupBoxList.config(border=2, relief='sunken', selectmode="SINGLE")

        mainWindowPickupBoxListScrollbar1 = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL,
                                                              command=mainWindowPickupBoxList.yview)
        mainWindowPickupBoxListScrollbar1.grid(row=3, column=2, sticky='nsw', rowspan=2)

        mainWindowPickupBoxListScrollbar2 = tkinter.Scrollbar(mainWindow, orient=tkinter.HORIZONTAL,
                                                              command=mainWindowPickupBoxList.xview)
        mainWindowPickupBoxListScrollbar2.grid(row=5, column=1, sticky='ewn', rowspan=2)
        mainWindowPickupBoxList['yscrollcommand'] = mainWindowPickupBoxListScrollbar1.set
        mainWindowPickupBoxList['xscrollcommand'] = mainWindowPickupBoxListScrollbar2.set

        #
        #
        #
        #
        #
        # drop off data
        mainWindowDropoffLabel = tkinter.Label(mainWindow, text="Dropoff Data")
        mainWindowDropoffLabel.grid(row=1, column=4, sticky='n')

        mainWindowDropoffCountryLabel = tkinter.Label(mainWindow, text="Dropoff country:")
        mainWindowDropoffCountryLabel.grid(row=2, column=3, sticky='n')

        mainWindowDropOffStationLabel = tkinter.Label(mainWindow, text="Dropoff Station Name:")
        mainWindowDropOffStationLabel.grid(row=3, column=3, sticky='n')

        mainWindowDropoffStationChosen = tkinter.Entry(mainWindow, textvariable=mainWindowDropoffStationChosentextvar)
        mainWindowDropoffStationChosen.grid(row=6, column=4, sticky='ew')

        mainWindowDropOffBoxList = tkinter.Listbox(mainWindow)
        mainWindowDropOffBoxList.grid(row=3, column=4, sticky='nsew', rowspan=2)
        mainWindowDropOffBoxList.config(border=2, relief='sunken')

        mainWindowDropOffBoxListScrollbar1 = tkinter.Scrollbar(mainWindow, orient=tkinter.VERTICAL,
                                                               command=mainWindowDropOffBoxList.yview)
        mainWindowDropOffBoxListScrollbar1.grid(row=3, column=5, sticky='nsw', rowspan=2)

        mainWindowDropOffBoxListScrollbar2 = tkinter.Scrollbar(mainWindow, orient=tkinter.HORIZONTAL,
                                                               command=mainWindowDropOffBoxList.xview)
        mainWindowDropOffBoxListScrollbar2.grid(row=5, column=4, sticky='ewn', rowspan=2)
        mainWindowDropOffBoxList['yscrollcommand'] = mainWindowDropOffBoxListScrollbar1.set
        mainWindowDropOffBoxList['xscrollcommand'] = mainWindowDropOffBoxListScrollbar2.set

        mainWindowSupLabel = tkinter.Label(mainWindow, text="Suppliers:")
        mainWindowSupLabel.grid(row=3, column=6, sticky='ne')
        mainWindowSupLabel = tkinter.Label(mainWindow, text="Pickup country:")

        mainWindowSup = tkinter.Listbox(mainWindow)
        mainWindowSup.config(border=2, relief='sunken', selectmode="SINGLE")
        mainWindowSup.grid(row=3, column=7, sticky='wen')

        # list1 = data.getAllSuppliersStationS(japan, times)

        # time data
        # pickup
        mainWindowPickupDateTime = tkinter.LabelFrame(mainWindow, text="Pickup date&time")
        mainWindowPickupDateTime.grid(row=7, column=1, sticky='snew')
        mainWindowPickupDateTime_TimeLabel = tkinter.Label(mainWindowPickupDateTime, text="Time:")
        mainWindowPickupDateTime_TimeLabel.grid(row=0, column=0, sticky='w')
        mainWindowPickupTimeHours = tkinter.Spinbox(mainWindowPickupDateTime, width=2, values=tuple(range(0, 24)))
        mainWindowPickupTimeMinutes = tkinter.Spinbox(mainWindowPickupDateTime, width=2, from_=0, to=59)
        mainWindowPickupTimeHours.grid(row=0, column=1, sticky='w')
        tkinter.Label(mainWindowPickupDateTime, text=':').grid(row=0, column=1, sticky='e')
        mainWindowPickupTimeMinutes.grid(row=0, column=2, sticky='w')
        PickupDateLabel = tkinter.Label(mainWindowPickupDateTime, text="Date:")
        PickupDateLabel.grid(row=5, column=0, sticky='w')
        tkinter.Label(mainWindowPickupDateTime, text='').grid(row=1, column=2)
        PickupdaySpin = tkinter.Spinbox(mainWindowPickupDateTime, width=5, from_=1, to=31)
        PickupmonthSpin = tkinter.Spinbox(mainWindowPickupDateTime, width=5, from_=1, to=12)
        PickupyearSpin = tkinter.Spinbox(mainWindowPickupDateTime, width=5, from_=2000, to=2099)
        PickupdaySpin.grid(row=5, column=1)
        PickupmonthSpin.grid(row=5, column=2)
        PickupyearSpin.grid(row=5, column=3)

        mainWindowDropoffDateTime = tkinter.LabelFrame(mainWindow, text="Dropoff date&time")
        mainWindowDropoffDateTime.grid(row=7, column=4, sticky='snew')
        mainWindowDropoffDateTime_TimeLabel = tkinter.Label(mainWindowDropoffDateTime, text="Time:")
        mainWindowDropoffDateTime_TimeLabel.grid(row=0, column=0, sticky='w')
        mainWindowDropoffTimeHours = tkinter.Spinbox(mainWindowDropoffDateTime, width=2, values=tuple(range(0, 24)))
        mainWindowDropoffTimeMinutes = tkinter.Spinbox(mainWindowDropoffDateTime, width=2, from_=0, to=59)
        mainWindowDropoffTimeHours.grid(row=0, column=1, sticky='w')
        tkinter.Label(mainWindowDropoffDateTime, text=':').grid(row=0, column=1, sticky='e')
        mainWindowDropoffTimeMinutes.grid(row=0, column=2, sticky='w')
        DropoffDateLabel = tkinter.Label(mainWindowDropoffDateTime, text="Date:")
        DropoffDateLabel.grid(row=5, column=0, sticky='w')
        tkinter.Label(mainWindowDropoffDateTime, text='').grid(row=1, column=2)
        DropoffdaySpin = tkinter.Spinbox(mainWindowDropoffDateTime, width=5, from_=1, to=31)
        DropoffmonthSpin = tkinter.Spinbox(mainWindowDropoffDateTime, width=5, from_=1, to=12)
        DropoffyearSpin = tkinter.Spinbox(mainWindowDropoffDateTime, width=5, from_=2000, to=2099)
        DropoffdaySpin.grid(row=5, column=1)
        DropoffmonthSpin.grid(row=5, column=2)
        DropoffyearSpin.grid(row=5, column=3)
        dayCalclabel = tkinter.Label(mainWindow, text="NumOfDays").grid(row=7, column=5, sticky='ews')
        daysEntry = tkinter.Entry(mainWindow, textvariable=days)
        daysEntry.grid(row=7, column=6, sticky='ews')
        mainWindowSupChosenEntry = tkinter.Entry(mainWindow,
                                                 textvariable=mainWindowSupChosenVar).grid(row=3, column=7,
                                                                                           sticky='swe')

        reslabel = tkinter.Label(mainWindow, text="Result :").grid(row=7, column=7, sticky='se')
        resEntry = tkinter.Entry(mainWindow, textvariable=res)
        resEntry.grid(row=7, column=8, sticky='sew')

        # Buttons
        # command=NationalOneWay(PickupmonthSpin,P)
        mainWindowDaysSet = tkinter.Button(mainWindow, text="Set days", command=dateCalc)
        mainWindowDaysSet.grid(row=7, column=5, sticky='ewn')
        mainWindowPUSet = tkinter.Button(mainWindow, text="Set PickUp", command=PU_choose_station)
        mainWindowPUSet.grid(row=5, column=1, sticky='sew')
        mainWindowDOSet = tkinter.Button(mainWindow, text="Set Dropoff", command=DO_choose_station)
        mainWindowDOSet.grid(row=5, column=4, sticky='sew')
        mainWindowSupListSet = tkinter.Button(mainWindow, text="Set List of suppliers", command=country_choose_toSup)
        mainWindowSupListSet.grid(row=2, column=5, sticky='w')
        mainWindowSupSet = tkinter.Button(mainWindow, text="Set Supplier", command=setSup)
        mainWindowSupSet.grid(row=3, column=6, sticky='se', padx=10)
        mainWindowRunButton = tkinter.Button(mainWindow, text="Run", command=run)
        mainWindowRunButton.grid(row=8, column=5, sticky='ew')
        mainWindowClearButton = tkinter.Button(mainWindow, text="Clear", command=clear)
        mainWindowClearButton.grid(row=8, column=6, sticky='ew')
        mainWindowQuitButton = tkinter.Button(mainWindow, text="Quit", command=mainWindow.quit)
        mainWindowQuitButton.grid(row=8, column=7, sticky='ew')
        mainWindowInteractiveModeButton = tkinter.Button(mainWindow, text="Interactive Mode")
        mainWindowInteractiveModeButton.grid(row=8, column=8, sticky='ew')

        # mainWindowHELP = tkinter.Button(mainWindow, text="Help", command=help1)
        # mainWindowHELP.grid(row=8, column=4, sticky='ew')

        # column and row configure
        mainWindow.columnconfigure(0, weight=1)
        mainWindow.columnconfigure(1, weight=1)
        mainWindow.columnconfigure(2, weight=1)
        mainWindow.columnconfigure(3, weight=1)
        mainWindow.columnconfigure(4, weight=1)
        mainWindow.columnconfigure(5, weight=1)
        mainWindow.columnconfigure(6, weight=1)
        mainWindow.columnconfigure(7, weight=1)
        mainWindow.columnconfigure(8, weight=1)
        mainWindow.columnconfigure(9, weight=1)
        mainWindow.columnconfigure(10, weight=1)
        mainWindow.rowconfigure(0, weight=1)
        mainWindow.rowconfigure(1, weight=1)
        mainWindow.rowconfigure(2, weight=1)
        mainWindow.rowconfigure(3, weight=1)
        mainWindow.rowconfigure(4, weight=1)
        mainWindow.rowconfigure(5, weight=1)
        mainWindow.rowconfigure(6, weight=1)
        mainWindow.rowconfigure(7, weight=1)
        mainWindow.rowconfigure(8, weight=1)
        mainWindow.rowconfigure(9, weight=1)
        mainWindow.rowconfigure(10, weight=1)
        mainWindow.mainloop()
        # def test():
        #     mainWindowPUCountryChosenTextVar.set(japan)
        #     country_choose_toSup11(japan)


#       test()


# tests
file = "C:\\Temp\\Times Rent a Car Japan National One Ways_1.xlsx"
japan = Country("Japan", "Yenn")
times = Supplier("Times")
japan.add_supplier(times, file)

# japan._suppliers_station[times] = {
#     #     # drop off station
#     "tokyo - haneda airport":
#         {
#             "tokyo - haneda airport": 0,
#             "tokyo - narita airport": 8000,
#             "tokyo - sasazuka railway station": 0,
#             "tokyo - fuchu railway station": 4000,
#             "tokyo - ebisu": 0,
#             "tokyo - shiyomi railway station": 0,
#             "tokyo - terace nagatacho railway station": 0,
#             "osaka - kansai international airport": 44000,
#             "osaka - higashi osaka nagata": 40000,
#             "osaka - kitahama": 40000,
#             "kyoto - shikanseh railway station": 40000,
#             "kyoto - fushimi shinhorikawa": 40000,
#             "kyoto - karasuma train station": 40000,
#             "kanazawa - kanazawa kanda ciy center": 36000,
#             "kanazawa - kanazawa railway station": 36000
#
#         },
#     "tokyo - narita airport":
#         {
#             "tokyo - haneda airport": 8000,
#             "tokyo - narita airport": 0,
#             "tokyo - sasazuka railway station": 8000,
#             "tokyo - fuchu railway station": 8000,
#             "tokyo - ebisu": 8000,
#             "tokyo - shiyomi railway station": 8000,
#             "tokyo - terace nagatacho railway station": 8000,
#             "osaka - kansai international airport": 48000,
#             "osaka - higashi osaka nagata": 44000,
#             "osaka - kitahama": 48000,
#             "kyoto - shikanseh railway station": 40000,
#             "kyoto - fushimi shinhorikawa": 40000,
#             "kyoto - karasuma train station": 44000,
#             "kanazawa - kanazawa kanda ciy center": 40000,
#             "kanazawa - kanazawa railway station": 40000
#         },
#     "tokyo - sasazuaka railway station":
#         {
#             "tokyo - haneda airport": -1,
#             "tokyo - narita airport": -1,
#             "tokyo - sasazuka railway station": 0,
#             "tokyo - fuchu railway station": -1,
#             "tokyo - ebisu": -1,
#             "tokyo - shiyomi railway station": -1,
#             "tokyo - terace nagatacho railway station": -1,
#             "osaka - kansai international airport": -1,
#             "osaka - higashi osaka nagata": -1,
#             "osaka - kitahama": -1,
#             "kyoto - shikanseh railway station": -1,
#             "kyoto - fushimi shinhorikawa": -1,
#             "kyoto - karasuma train station": -1,
#             "kanazawa - kanazawa kanda ciy center": -1,
#             "kanazawa - kanazawa railway station": -1
#         },
#     "tokyo - fuchu railway station": {
#         "tokyo - haneda airport": -1,
#         "tokyo - narita airport": -1,
#         "tokyo - sasazuka railway station": -1,
#         "tokyo - fuchu railway station": 0,
#         "tokyo - ebisu": -1,
#         "tokyo - shiyomi railway station": -1,
#         "tokyo - terace nagatacho railway station": -1,
#         "osaka - kansai international airport": -1,
#         "osaka - higashi osaka nagata": -1,
#         "osaka - kitahama": -1,
#         "kyoto - shikanseh railway station": -1,
#         "kyoto - fushimi shinhorikawa": -1,
#         "kyoto - karasuma train station": -1,
#         "kanazawa - kanazawa kanda ciy center": -1,
#         "kanazawa - kanazawa railway station": -1},
#     "tokyo - ebisu": {
#         "tokyo - haneda airport": -1,
#         "tokyo - narita airport": -1,
#         "tokyo - sasazuka railway station": -1,
#         "tokyo - fuchu railway station": -1,
#         "tokyo - ebisu": 0,
#         "tokyo - shiyomi railway station": -1,
#         "tokyo - terace nagatacho railway station": -1,
#         "osaka - kansai international airport": -1,
#         "osaka - higashi osaka nagata": -1,
#         "osaka - kitahama": -1,
#         "kyoto - shikanseh railway station": -1,
#         "kyoto - fushimi shinhorikawa": -1,
#         "kyoto - karasuma train station": -1,
#         "kanazawa - kanazawa kanda ciy center": -1,
#         "kanazawa - kanazawa railway station": -1
#     },
#     "tokyo - shiyomi railway station":
#         {
#             "tokyo - haneda airport": 0,
#             "tokyo - narita airport": 8000,
#             "tokyo - sasazuka railway station": 0,
#             "tokyo - fuchu railway station": 4000,
#             "tokyo - ebisu": 0,
#             "tokyo - shiyomi railway station": 0,
#             "tokyo - terace nagatacho railway station": 0,
#             "osaka - kansai international airport": 48000,
#             "osaka - higashi osaka nagata": 44000,
#             "osaka - kitahama": 44000,
#             "kyoto - shikanseh railway station": 40000,
#             "kyoto - fushimi shinhorikawa": 40000,
#             "kyoto - karasuma": 52000,
#             "kanazawa - kanazawa kanda ciy center": 40000,
#             "kanazawa - kanazawa railway station": 40000
#         },
#     "tokyo - terace nagatacho railway station": {
#         "tokyo - haneda airport": -1,
#         "tokyo - narita airport": -1,
#         "tokyo - sasazuka railway station": -1,
#         "tokyo - fuchu railway station": -1,
#         "tokyo - ebisu": -1,
#         "tokyo - shiyomi railway station": -1,
#         "tokyo - terace nagatacho railway station": 0,
#         "osaka - kansai international airport": -1,
#         "osaka - higashi osaka nagata": -1,
#         "osaka - kitahama": -1,
#         "kyoto - shikanseh railway station": -1,
#         "kyoto - fushimi shinhorikawa": -1,
#         "kyoto - karasuma train station": -1,
#         "kanazawa - kanazawa kanda ciy center": -1,
#         "kanazawa - kanazawa railway station": -1
#     },
#     "kanazawa - kanazawa kanda ciy center": {
#         "tokyo - haneda airport": 40000,
#         "tokyo - narita airport": 36000,
#         "tokyo - sasazuka railway station": 36000,
#         "tokyo - fuchu railway station": 36000,
#         "tokyo - ebisu": 36000,
#         "tokyo - shiyomi railway station": 40000,
#         "tokyo - terace nagatacho railway station": 36000,
#         "osaka - kansai international airport": 28000,
#         "osaka - higashi osaka nagata": 24000,
#         "osaka - kitahama": 24000,
#         "kyoto - shikanseh railway station": 20000,
#         "kyoto - fushimi shinhorikawa": 20000,
#         "kyoto - karasuma train station": 20000,
#         "kanazawa - kanazawa kanda ciy center": 0,
#         "kanazawa - kanazawa railway station": 0
#     },
#     "kanazawa - kanazawa railway station": {
#         "tokyo - haneda airport": -1,
#         "tokyo - narita airport": -1,
#         "tokyo - sasazuka railway station": -1,
#         "tokyo - fuchu railway station": -1,
#         "tokyo - ebisu": -1,
#         "tokyo - shiyomi railway station": -1,
#         "tokyo - terace nagatacho railway station": -1,
#         "osaka - kansai international airport": -1,
#         "osaka - higashi osaka nagata": -1,
#         "osaka - kitahama": -1,
#         "kyoto - shikanseh railway station": -1,
#         "kyoto - fushimi shinhorikawa": -1,
#         "kyoto - karasuma train station": -1,
#         "kanazawa - kanazawa kanda ciy center": -1,
#         "kanazawa - kanazawa railway station": 0
#     },
#     "osaka - kansai international airport": {
#         "tokyo - haneda airport": -1,
#         "tokyo - narita airport": -1,
#         "tokyo - sasazuka railway station": -1,
#         "tokyo - fuchu railway station": -1,
#         "tokyo - ebisu": -1,
#         "tokyo - shiyomi railway station": -1,
#         "tokyo - terace nagatacho railway station": -1,
#         "osaka - kansai international airport": 0,
#         "osaka - higashi osaka nagata": -1,
#         "osaka - kitahama": -1,
#         "kyoto - shikanseh railway station": -1,
#         "kyoto - fushimi shinhorikawa": -1,
#         "kyoto - karasuma train station": -1,
#         "kanazawa - kanazawa kanda ciy center": -1,
#         "kanazawa - kanazawa railway station": -1
#     },
#     "osaka - kitahama": {
#         "tokyo - haneda airport": -1,
#         "tokyo - narita airport": -1,
#         "tokyo - sasazuka railway station": -1,
#         "tokyo - fuchu railway station": -1,
#         "tokyo - ebisu": -1,
#         "tokyo - shiyomi railway station": -1,
#         "tokyo - terace nagatacho railway station": -1,
#         "osaka - kansai international airport": -1,
#         "osaka - higashi osaka nagata": -1,
#         "osaka - kitahama": 0,
#         "kyoto - shikanseh railway station": -1,
#         "kyoto - fushimi shinhorikawa": -1,
#         "kyoto - karasuma train station": -1,
#         "kanazawa - kanazawa kanda ciy center": -1,
#         "kanazawa - kanazawa railway station": -1
#     },
#     "osaka - higashi osaka nagata": {
#         "tokyo - haneda airport": 40000,
#         "tokyo - narita airport": 44000,
#         "tokyo - sasazuka railway station": 40000,
#         "tokyo - fuchu railway station": 40000,
#         "tokyo - ebisu": 40000,
#         "tokyo - shiyomi railway station": 44000,
#         "tokyo - terace nagatacho railway station": 40000,
#         "osaka - kansai international airport": 2000,
#         "osaka - higashi osaka nagata": 0,
#         "osaka - kitahama": 0,
#         "kyoto - shikanseh railway station": 4000,
#         "kyoto - fushimi shinhorikawa": 4000,
#         "kyoto - karasuma train station": 4000,
#         "kanazawa - kanazawa kanda ciy center": 24000,
#         "kanazawa - kanazawa railway station": 24000
#     },
#     "kyoto - shikanseh railway station": {
#         "tokyo - haneda airport": -1,
#         "tokyo - narita airport": -1,
#         "tokyo - sasazuka railway station": -1,
#         "tokyo - fuchu railway station": -1,
#         "tokyo - ebisu": -1,
#         "tokyo - shiyomi railway station": -1,
#         "tokyo - terace nagatacho railway station": -1,
#         "osaka - kansai international airport": -1,
#         "osaka - higashi osaka nagata": -1,
#         "osaka - kitahama": -1,
#         "kyoto - shikanseh railway station": 0,
#         "kyoto - fushimi shinhorikawa": -1,
#         "kyoto - karasuma train station": -1,
#         "kanazawa - kanazawa kanda ciy center": -1,
#         "kanazawa - kanazawa railway station": -1
#     },
#     "kyoto - fushimi shinhorikawa": {
#         "tokyo - haneda airport": 40000,
#         "tokyo - narita airport": 44000,
#         "tokyo - sasazuka railway station": 40000,
#         "tokyo - fuchu railway station": 40000,
#         "tokyo - ebisu": 40000,
#         "tokyo - shiyomi railway station": 44000,
#         "tokyo - terace nagatacho railway station": 40000,
#         "osaka - kansai international airport": 2000,
#         "osaka - higashi osaka nagata": 0,
#         "osaka - kitahama": 0,
#         "kyoto - shikanseh railway station": 4000,
#         "kyoto - fushimi shinhorikawa": 4000,
#         "kyoto - karasuma train station": 4000,
#         "kanazawa - kanazawa kanda ciy center": 24000,
#         "kanazawa - kanazawa railway station": 24000
#     },
#     "kyoto - karasuma train station": {
#         "tokyo - haneda airport": -1,
#         "tokyo - narita airport": -1,
#         "tokyo - sasazuka railway station": -1,
#         "tokyo - fuchu railway station": -1,
#         "tokyo - ebisu": -1,
#         "tokyo - shiyomi railway station": -1,
#         "tokyo - terace nagatacho railway station": -1,
#         "osaka - kansai international airport": -1,
#         "osaka - higashi osaka nagata": -1,
#         "osaka - kitahama": -1,
#         "kyoto - shikanseh railway station": -1,
#         "kyoto - fushimi shinhorikawa": -1,
#         "kyoto - karasuma train station": 0,
#         "kanazawa - kanazawa kanda ciy center": -1,
#         "kanazawa - kanazawa railway station": -1
#     }
# }

# for key in sorted(nationalOneWayData.keys()):
#     print("{} - {}".format(key, nationalOneWayData.get(key)))
# japan._suppliers_station[times];

# sorted(japan._suppliers_station.keys())
# for sup in japan._suppliers_station.keys():
#     print(sup, end=":")
#     for key in japan._suppliers_station[sup]:
#         print(key,end=",")
#     print()

data = Data()
# germany = Country("Germany", "Euro")
# france = Country("France", "Euro")
# budget = Supplier("Budget")
# ec = Supplier("Europcar")
# budget.add_sippCode("CDAR")
# budget.add_sippCode("CDMR")
# budget.add_sippCode("UCBWBF")
# munich = "Munich airport"
# frankfurt = "Frankfurt airport"
# nice = "Nice airport"
# germany.add_station(munich)
# germany.add_station(frankfurt)
# france.add_station(nice)
# germany.add_supplier(budget)
# # germany.add_supplier(ec)
# # france.add_supplier(budget)
# # germany.add_suplier_station(munich, budget)
# # germany.add_suplier_station(frankfurt, budget)
# # france.add_suplier_station(nice, budget)
data.addCountry(japan)
# data.addCountry(germany)
# # data.addCountryToGo(germany, japan)
# # data.addCountryToGo(germany, france)
# data.addCountry(france)
# # data.addCountryToGo(germany, france)
# # list1 = list("Spain", "Portugal", "Poland", "Italy", "United Kingdom")
# # list2 = list()
# # for string in list1:
# #     list2.append(Country(list1[string]))
# print(data.getAllCountries())
# # fountry = data.getCountry(0)
