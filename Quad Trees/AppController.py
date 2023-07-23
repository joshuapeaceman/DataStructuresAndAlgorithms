import pyqtgraph

from gui import MainWindow
from model.QuadTree import QuadTree, Boundry, Point
from model.Experiment import Experiment


class AppController:
    def __init__(self):
        self.mainWindow = MainWindow.MainWindow()
        self.experiment = Experiment(self.mainWindow.x.value(), self.mainWindow.y.value(),
                                     self.mainWindow.capacity.value())

        self.plt = self.mainWindow.getPlot()
        self.init_mainWindow()

        self.quadTree = QuadTree('root', 'root', Boundry(0, 0, self.experiment.x, self.experiment.y), 0,
                                 2)
        self.quadTree.devision.connect(self.draw_quads)

        self.mainWindow.show()

    def init_mainWindow(self):
        self.mainWindow.init.clicked.connect(self.setExperiment)
        self.mainWindow.graphWidget.scene().sigMouseClicked.connect(self.mouse_clicked)

        self.plt.plot([0, self.experiment.x, self.experiment.x, 0, 0],
                      [0, 0, self.experiment.y, self.experiment.y, 0],
                      pen='w', symbol='o', symbolPen='g',
                      symbolBrush=0.2)


    def setExperiment(self):
        self.experiment = Experiment(self.mainWindow.x.value(), self.mainWindow.y.value(),
                                     self.mainWindow.capacity.value())

    def mouse_clicked(self, event):

        vb = self.plt.plotItem.vb
        if self.mainWindow.graphWidget.sceneBoundingRect().contains(event.scenePos()):
            mouse_point = vb.mapSceneToView(event.scenePos())
            x, y = mouse_point.x(), mouse_point.y()

            if self.experiment.withinBoundraies(x, y):
                print(f'clicked plot X: {x}, Y: {y}, event: {event}, points are within boundaries')
                self.plt.plot([x], [y], pen='r', symbol='x', symbolPen='r',
                      symbolBrush=0.01)

                self.quadTree.insert_point(Point('id'+str(x)+str(y), x, y))


            else:
                print('points outside of boundaries')


    def draw_quads(self, data):

        x = [data.boundary.x, data.boundary.dx, data.boundary.dx, data.boundary.x]
        y = [data.boundary.y, data.boundary.y, data.boundary.dy, data.boundary.dy]
        print('deviding')
        self.plt.plot(x, y, pen='b', symbolBrush=0.1)
