from requests import get as httpGet
from time import sleep
from typing import Any
from os import path
from json import load as readJsonFile

VACANCY_COUNT_PER_PAGE: int = 100
HEAD_HUNTER_API_URL: str = "https://api.hh.ru/vacancies"
SETTINGS_FILE_NAME: str = "settings.json"

class ParsingInformation:
    __title: str
    __keywords: str
    __company: str
    __experience: str
    __startSalaryValue: int
    __endSalaryValue: int
    __salaryCurrency: str

    def __init__(self, title: str, keywords: str, company: str, experience: str, 
                 startSalaryValue: int, endSalaryValue: int, salaryCurrency: str):
        self.__title = title
        self.__keywords = keywords
        self.__company = company
        self.__experience = experience
        self.__startSalaryValue = startSalaryValue
        self.__endSalaryValue = endSalaryValue
        self.__salaryCurrency = salaryCurrency

    @property
    def title(self):
        return self.__title
    
    @property
    def keywords(self):
        return self.__keywords
    
    @property
    def company(self):
        return self.__company
    
    @property
    def experience(self):
        return self.__experience
    
    @property
    def startSalaryValue(self):
        return self.__startSalaryValue
    
    @property
    def endSalaryValue(self):
        return self.__endSalaryValue
    
    @property
    def salaryCurrency(self):
        return self.__salaryCurrency

class Settings:
    __cityId: int
    __vacancies: list[str]
    __keywords: dict[str, str]
    __graphicNames: dict[str, str]
    __colors: dict[str, str]
    __needDrawPoints: dict[str, int]
    __minPayInMonthInRub: int
    __maxPayInMonthInRub: int

    def __init__(self, cityId: int, vacancies: list[str], keywords: dict[str, str], 
                 graphicNames: dict[str, str], colors: dict[str, str], needDrawPoints: dict[str, int],
                 minPayInMonthInRub: int, maxPayInMonthInRub: int):
        
        self.__cityId = cityId
        self.__vacancies = vacancies
        self.__keywords = keywords
        self.__graphicNames = graphicNames
        self.__colors = colors
        self.__needDrawPoints = needDrawPoints
        self.__minPayInMonthInRub = minPayInMonthInRub
        self.__maxPayInMonthInRub = maxPayInMonthInRub

    @property
    def cityId(self):
        return self.__cityId
    
    @property
    def vacancies(self):
        return self.__vacancies
    
    @property
    def keywords(self):
        return self.__keywords
    
    @property
    def graphicNames(self):
        return self.__graphicNames
    
    @property
    def colors(self):
        return self.__colors
    
    @property
    def needDrawPoints(self):
        return self.__needDrawPoints
    
    @property
    def minPayInMonthInRub(self):
        return self.__minPayInMonthInRub
    
    @property
    def maxPayInMonthInRub(self):
        return self.__maxPayInMonthInRub

class ParserOfHeadHunterSite:
    __vacancyName: str
    __cityId: int
    __waitTime: float = 1.5

    def __init__(self, vacancyName: str, cityId: int):
        self.__vacancyName = vacancyName
        self.__cityId = cityId

    @property
    def vacancyName(self):
        return self.__vacancyName
    
    @property
    def cityId(self):
        return self.__cityId
    
    def parse(self, keyword: str, pageCount: int):
        """
        Returns vacancy data by vacancy name
        @param 'keyword' is keyword for finding it in cells as 'title' and 'keywords'
        @param 'pageCount' is count of pages which need generate, if -1 returns all pages
        """

        page = 0
        vacanciesData = {}
        keyword = keyword.lower()

        while(True):
            vacanciesData = self.__getJsonVacancies(page)

            if(not vacanciesData.get("items")):
                yield ParsingInformation("", "", "", "", -1, -1, "")
                break

            for vacancyData in vacanciesData["items"]:
                parsingInformation = self.__getParsingInformation(vacancyData, keyword)
                if(parsingInformation != None):
                    yield parsingInformation

            if(pageCount >= 0 and page >= pageCount-1):
                break

            elif(pageCount == -1 and page >= vacanciesData["pages"]-1):
                break

            page += 1
            self.__wait(self.__waitTime)

    def __getJsonVacancies(self, page: int) -> dict[str, Any]:
        url: str = HEAD_HUNTER_API_URL
        parameters = {
            "text": f"{self.__vacancyName}",
            "area": self.__cityId,
            "specialization": 1,
            "per-page": VACANCY_COUNT_PER_PAGE,
            "page": page
        }
        response = httpGet(url, params=parameters)
        response.raise_for_status()
        return response.json()
    
    def __getParsingInformation(self, vacancyData: dict[str, Any], keyword: str):
        title: str = f"{vacancyData['name']}"
        keywords: str = vacancyData["snippet"].get("requirement", "")
        company: str = vacancyData["employer"]["name"]
        experience: str = vacancyData["experience"].get("name", "")
        salary = vacancyData["salary"]

        titleLower: str = title.lower()
        keywordsLower = None
        if(keywords != None):
            keywordsLower = keywords.lower()

        if(salary != None and
           (titleLower.find(keyword) != -1 or
            (keywords != None and keywordsLower.find(keyword) != -1))):

            return ParsingInformation(title, keywords, company, experience, salary["from"], salary["to"], salary["currency"])
        
        return None
        
    def __wait(self, timeInS: float) -> None:
        return sleep(timeInS)
    
def getSettings() -> Settings:
    settingsPath = _getPathOfSettings()
    jsonSettings = _getJsonDataFile(settingsPath)
    settingAttributes: list[str] = list(vars(Settings(-1, ["a"], {"a":"b"}, {"a":"b"}, {"a":"b"}, {"a":0}, -1, -1)).keys())
    
    for attribute in settingAttributes:
        normalAttribute: str = attribute[11:]
        if(normalAttribute not in jsonSettings):
            raise AttributeError(f"In json settings have not attribute {normalAttribute}")
        
    return Settings(jsonSettings["cityId"], jsonSettings["vacancies"],
                    jsonSettings["keywords"], jsonSettings["graphicNames"], jsonSettings["colors"],
                    jsonSettings["needDrawPoints"], jsonSettings["minPayInMonthInRub"], jsonSettings["maxPayInMonthInRub"])

def _getJsonDataFile(fileName: str) -> dict[str, Any]:
    if(not path.exists(fileName)):
        raise FileExistsError(f"File not found: {fileName}")
    
    with open(fileName, "r", encoding="utf-8") as jsonFile:
        jsonData = readJsonFile(jsonFile)

    return jsonData

def _getPathOfSettings() -> str:
    currentDir = path.dirname(path.realpath(__file__))
    return path.join(currentDir, SETTINGS_FILE_NAME)

def parseEURValue() -> float:
    return _parseValuteValue("EUR")

def parseUSDValue() -> float:
    return _parseValuteValue("USD")

def _parseValuteValue(valute: str) -> float:
    data = httpGet("https://www.cbr-xml-daily.ru/daily_json.js").json()
    return data["Valute"][valute]["Value"]