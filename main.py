from parser import (ParserOfHeadHunterSite,
                    getSettings,
                    Settings)

from graphicsetter import (setPaysAndWorkTimesOf,
                           getMedianPaysByWorkTime,
                           getYByX,
                           setMinPayInMonthInRub,
                           setMaxPayInMonthInRub,
                           SCALE_OF_PAY)

from math import (ceil,
                  log10)

from datetime import date
import graphic

DASH_STRING = "----------------------------------------------------------------"

def main():
    graphic.setGraphicName(f"Promising IT professions on {_getStrTodayDate()}(yyyy-mm-dd)")
    graphic.setXName("Work experience, years")
    graphic.setYName(f"Get paycheck, 10^{int(ceil(log10(SCALE_OF_PAY)))} rubles")

    settings = getSettings()
    checkAllVacanciesAttribute(settings)

    setMinPayInMonthInRub(settings.minPayInMonthInRub)
    setMaxPayInMonthInRub(settings.maxPayInMonthInRub)

    cityId: int = settings.cityId
    for vacancyName in settings.vacancies:
        vacancyParser = ParserOfHeadHunterSite(vacancyName, cityId)
        needDrawPoints: bool = False if settings.needDrawPoints[vacancyName] == 0 else True
        parseVacancy(vacancyParser, settings.keywords[vacancyName],
                      settings.graphicNames[vacancyName], settings.colors[vacancyName],
                      vacancyName, needDrawPoints)
        
    graphic.showLegend()
    graphic.onDisplay()

def _getStrTodayDate() -> str:
    return date.today().__str__()
        
def checkAllVacanciesAttribute(settings: Settings):
    for vacancyName in settings.vacancies:
        _checkVacancyAttributes(vacancyName, settings)
        
def _checkVacancyAttributes(vacancyName: str, settings: Settings):
    settingAttributes: list[str] = list(vars(Settings(-1, ["a"], {"a":"b"}, {"a":"b"}, {"a":"b"}, {"a":0}, -1, -1)).keys())
    for vacancyAttribute in settingAttributes:
        normalAttribute: str = vacancyAttribute[11:]

        attributeValue = settings.__getattribute__(normalAttribute)
        attributeValueType = type(attributeValue).__name__
        if(attributeValueType in ["list", "dict"] and vacancyName not in attributeValue):
            raise AttributeError(f"Vacancy name '{vacancyName}' have not value of attribute '{normalAttribute}'")

def parseVacancy(parser: ParserOfHeadHunterSite, keyword: str, graphicName: str, color: str, vacancyName: str, needDrawPoints: bool = True):
    print("THEMA: "+vacancyName.upper())
    print(DASH_STRING)
    pays: list[int] = []
    workTimes: list[int] = []

    print(f"Parsing vacancies of {vacancyName} from hh.ru:")
    vacancyCount: int = 0
    for vacancyNumber in setPaysAndWorkTimesOf(parser, keyword, pays, workTimes):
        print('{} vacancies'.format(vacancyNumber), end='\r')
        vacancyCount += 1

    print(f"Count of checked vacancies: {vacancyCount}")

    print(f"Finding of {vacancyName} median pays...")
    medianPaysByWorkTime = getMedianPaysByWorkTime(pays, workTimes)

    if(needDrawPoints):
        print(f"Draw points of {vacancyName}...")
        graphic.drawPoints(workTimes, pays, graphicName, color)

    medianX, medianY = getYByX(medianPaysByWorkTime)

    print(f"Draw median pays line of {vacancyName}...")

    if(not needDrawPoints):
        graphic.drawLine(medianX, medianY, color, graphicName + " median pays")
    else:
        graphic.drawLine(medianX, medianY, color)

    print(f"Parsing of {vacancyName} is finished!")
    print(DASH_STRING)

if __name__ == "__main__":
    main()