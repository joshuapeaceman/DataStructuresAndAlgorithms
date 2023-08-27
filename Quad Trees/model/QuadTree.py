from PyQt6.QtCore import QObject, pyqtSignal


class QuadTree(QObject):
    devision = pyqtSignal(object)

    def __init__(self, type, root, boundary, depth, node_capacity) -> None:
        QObject.__init__(self, parent=None)
        self.type = type
        if type == 'root':
            self.root = self
        else:
            self.root = root
        self.capacity = node_capacity
        self.boundary = boundary
        self.points = []
        self.depth = depth
        self.devided = False
        self.nw = None
        self.sw = None
        self.ne = None
        self.se = None

        self.root.devision.emit(self)

    def has_capacity(self):
        if len(self.points) < self.capacity:
            return True
        else:
            return False

    def insert_point(self, point):
        if self.has_capacity() and not self.devided:
            print('inserting point at', self.depth, self.type)
            self.points.append(point)
        else:
            if not self.devided:
                self.devide()
            self.insert_into_sub(point)

    def insert_into_sub(self, point):
        if self.boundary.x <= point.x <= (self.boundary.dx / 2) and (
                self.boundary.dy / 2) <= point.y <= self.boundary.dy:
            self.nw.insert_point(point)
            return True
        elif self.boundary.x <= point.x <= (
                self.boundary.dx / 2) and self.boundary.y <= point.y <= (self.boundary.dy / 2):
            self.sw.insert_point(point)
            return True
        elif (self.boundary.dx / 2) <= point.x <= self.boundary.dx and (
                self.boundary.dy / 2) <= point.y <= self.boundary.dy:
            self.ne.insert_point(point)
            return True
        elif (self.boundary.dx / 2) <= point.x <= self.boundary.dx and self.boundary.y <= point.y <= (
                self.boundary.dy / 2):
            self.se.insert_point(point)
            return True
        else:
            print('insert didnt work', point.id)
            return False

    def devide(self):
        self.nw = QuadTree('nw', self.root,
                           Boundry(self.boundary.x, ((self.boundary.y + self.boundary.dy) / 2),
                                                    ((self.boundary.x + self.boundary.dx) / 2), self.boundary.dy),
                           self.depth + 1,
                           self.capacity)
        self.sw = QuadTree('sw', self.root,
                           Boundry(self.boundary.x, self.boundary.y, ((self.boundary.x + self.boundary.dx) / 2),
                                   ((self.boundary.y + self.boundary.dy) / 2)), self.depth + 1, self.capacity)
        self.ne = QuadTree('ne', self.root,
                           Boundry(((self.boundary.x + self.boundary.dx) / 2),
                                   ((self.boundary.y + self.boundary.dy) / 2),
                                   self.boundary.dx, self.boundary.dy), self.depth + 1, self.capacity)
        self.se = QuadTree('se', self.root,
                           Boundry(((self.boundary.x + self.boundary.dx) / 2), self.boundary.y, self.boundary.dx,
                                   ((self.boundary.y + self.boundary.dy) / 2)), self.depth + 1, self.capacity)

        self.devided = True

    def get_all_points_from_children(self, radius):
        points = []
        points.extend(self.points)
        if self.devided:
            # if quad in radius around the point
            points.extend(self.ne.get_all_points_from_children(0))
            points.extend(self.se.get_all_points_from_children(0))
            points.extend(self.nw.get_all_points_from_children(0))
            points.extend(self.sw.get_all_points_from_children(0))
        return points

    def search_for_point(self, point, distance):
        """if the point is in the current branch node check if the node has children. if it has children,
            retrieve all of the points of all of the children and childrens children"""

        points = []
        if point in self.points:
            print('Point:', point.id, 'found in', self.type, 'and depth:', self.depth)
            if self.devided:
                points.extend(self.get_all_points_from_children(0))
            else:
                points.extend(self.points)

        else:
            if self.devided:
                if self.boundary.x <= point.x <= self.boundary.dx / 2 and self.boundary.dy / 2 <= point.y <= self.boundary.dy:
                    p = self.nw.search_for_point(point, distance)
                    points.extend(p)

                elif self.boundary.x <= point.x <= self.boundary.dx / 2 and self.boundary.y <= point.y <= self.boundary.dy / 2:
                    p = self.sw.search_for_point(point, distance)
                    points.extend(p)

                elif self.boundary.dx / 2 <= point.x <= self.boundary.dx and self.boundary.dy / 2 <= point.y <= self.boundary.dy:
                    p = self.ne.search_for_point(point, distance)
                    points.extend(p)

                elif self.boundary.dx / 2 <= point.x <= self.boundary.dx and self.boundary.y <= point.y <= self.boundary.dy / 2:
                    p = self.se.search_for_point(point, distance)
                    points.extend(p)

        return points

    def extended_search(self, distance):
        pass


class Boundry():
    """this is the area of the Quad"""

    def __init__(self, x, y, dx, dy) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        self.cx = (x + dx) / 2
        self.cy = (y + dy) / 2

        # print('new devision', self.x, self.cx, self.dx, self.y, self.cy, self.dy)


class Point():
    def __init__(self, id=None, x=0, y=0) -> None:
        self.id = id

        self.x = x
        self.y = y
