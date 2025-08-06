import matplotlib.pyplot as plot

POINT_SENSITIVY: float = 0.4
LINE_POINT_SIZE: int = 6

def drawPoints(x: list[int], y: list[int], name: str | None=None, color: str | None=None) -> None:
    if(name == None):
        plot.scatter(x, y, edgecolors=color, alpha=POINT_SENSITIVY)
    elif(color == None):
        plot.scatter(x, y, label=name, alpha=POINT_SENSITIVY)
    elif(name == None and color == None):
        plot.scatter(x, y, alpha=POINT_SENSITIVY)
    else:
        plot.scatter(x, y, label=name, edgecolors=color, alpha=POINT_SENSITIVY, c=color)

def drawLine(x: list[int], y: list[int], color: str | None=None, name: str | None=None) -> None:
    if(color == None):
        plot.plot(x, y, label=name, marker="o", markersize=LINE_POINT_SIZE)
    elif(name == None):
        plot.plot(x, y, color=color, marker="o", markersize=LINE_POINT_SIZE)
    elif(name == None and color == None):
        plot.plot(x, y, marker="o", markersize=LINE_POINT_SIZE)
    else:
        plot.plot(x, y, label=name, color=color, marker="o", markersize=LINE_POINT_SIZE)

def setGraphicName(name: str):
    plot.title(name)

def setXName(name: str):
    plot.xlabel(name)

def setYName(name: str):
    plot.ylabel(name)

def showLegend():
    plot.legend(loc="best")

def onDisplay():
    plot.show()