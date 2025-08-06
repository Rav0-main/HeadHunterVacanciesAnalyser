from parser import ParserOfHeadHunterSite
from parser import parseUSDValue as USD
from parser import parseEURValue as EUR

MIN_PAY_IN_MONTH_IN_RUB: int | None = None
MAX_PAY_IN_MONTH_IN_RUB: int | None = None
SCALE_OF_PAY = 1000
COUNT_WORKING_HOURS_IN_MONTH = 8 * 23

USD_RATE = USD()
EUR_RATE = EUR()

def setMinPayInMonthInRub(value: int) -> None:
    global MIN_PAY_IN_MONTH_IN_RUB
    MIN_PAY_IN_MONTH_IN_RUB = value

def setMaxPayInMonthInRub(value: int) -> None:
    global MAX_PAY_IN_MONTH_IN_RUB
    MAX_PAY_IN_MONTH_IN_RUB = value

def setPaysAndWorkTimesOf(parser: ParserOfHeadHunterSite, keyword: str, pays: list[int], workTimes: list[int]):
    pageCount: int = 0
    for information in parser.parse(keyword, -1):
        if(information.startSalaryValue == -1):
            break

        payIsSetted = _setPay(information.startSalaryValue, information.endSalaryValue, information.salaryCurrency, pays)
        if(payIsSetted):
            _setWorkTime(information.experience, workTimes)
            pageCount += 1
        
        yield pageCount

def _setPay(startSalaryValue: int | None, endSalaryValue: int | None, salaryCurrency: str, pays: list[int]) -> bool:
    resultSalaryValue: int | None = None
    if(startSalaryValue == None and endSalaryValue != None):
        resultSalaryValue = _translateToRubles(endSalaryValue, salaryCurrency)

    elif(endSalaryValue == None and startSalaryValue != None):
        resultSalaryValue = _translateToRubles(startSalaryValue, salaryCurrency)

    elif(endSalaryValue != None and startSalaryValue != None):
        resultSalaryValue = _translateToRubles((startSalaryValue+endSalaryValue)//2, salaryCurrency)

    return _addSalaryValueIn(pays, resultSalaryValue)
        

def _translateToRubles(value: float, currency: str) -> int:
    rates: dict[str, float] = {"USD": USD_RATE, "RUR": 1.0, "EUR": EUR_RATE}
    if(currency not in rates):
        raise Exception(f"Currency have not in rate: {currency}")
    
    return int(round(value * rates[currency]))

def _addSalaryValueIn(pays: list[int], salaryValue: int | None) -> bool:
    if(MIN_PAY_IN_MONTH_IN_RUB == None):
        raise NotImplementedError("Value of min pay in month in rubles not setted!")
    
    elif(MAX_PAY_IN_MONTH_IN_RUB == None):
        raise NotImplementedError("Value of max pay in month in rubles not setted!")
    
    if(salaryValue == None):
        return False
    
    elif(salaryValue > MIN_PAY_IN_MONTH_IN_RUB
       and salaryValue < MAX_PAY_IN_MONTH_IN_RUB):
        pays.append(salaryValue//SCALE_OF_PAY)
        return True
    
    elif(salaryValue < MIN_PAY_IN_MONTH_IN_RUB
        and salaryValue*COUNT_WORKING_HOURS_IN_MONTH < MAX_PAY_IN_MONTH_IN_RUB):
        pays.append((salaryValue*COUNT_WORKING_HOURS_IN_MONTH)//SCALE_OF_PAY)
        return True
    
    return False


def _setWorkTime(experience: str, workTimes: list[int]) -> None:
    valuesOfExperience: dict[str, int] = {
        "Не имеет значения": 8,
        "Более 6 лет": 7,
        "От 3 до 6 лет": 6,
        "От 1 года до 3 лет": 3,
        "Нет опыта": 1,
    }

    if(experience not in valuesOfExperience):
        raise Exception(f"Experience type not found: {experience}")

    workTimes.append(valuesOfExperience[experience])

def getMedianPaysByWorkTime(pays: list[int], workTimes: list[int]) -> dict[int, int]:
    avgValues: dict[int, int] = {}
    allPaysByWorkTime: dict[int, list[int]] = {}

    for i in range(0, len(workTimes)):
        if(workTimes[i] in allPaysByWorkTime):
            allPaysByWorkTime[workTimes[i]].append(pays[i])
        else:
            allPaysByWorkTime[workTimes[i]] = [pays[i]]
            avgValues[workTimes[i]] = -1
    
    differenceWorkTimes: list[int] = []
    for workTime in allPaysByWorkTime.keys():
        allPaysByWorkTime[workTime].sort()
        avgValues[workTime] = allPaysByWorkTime[workTime][len(allPaysByWorkTime[workTime])//2]
        differenceWorkTimes.append(workTime)

    differenceWorkTimes.sort()
    sortedAvgValues: dict[int, int] = {}
    for workTime in differenceWorkTimes:
        sortedAvgValues[workTime] = avgValues[workTime]

    return sortedAvgValues

"""
tuple[0] - list of x
tuple[1] - list of y
"""
def getYByX(xByY: dict[int, int]) -> tuple[list[int], list[int]]:
    y = [xByY[i] for i in xByY.keys()]
    x = [i for i in xByY.keys()]
    return (x, y)