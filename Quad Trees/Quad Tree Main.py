import random

import json

class DataFrame():
    def __init__(self, size_square, number_of_points, node_capacity):
        size_x = size_square
        size_y = size_x

        self.quadTree = QuadTree('root',Boundry(0,0, size_x, size_y), 0, node_capacity)
        self.dataPoints =[]
        #create the points and insert them into the quad tree data structure
        for n in range(0, number_of_points):
            point =Point(id=n,                       
                         x=random.randint(1, size_x), 
                         y=random.randint(1, size_y)
                         )
            self.quadTree.insert_point(point=point)
            self.dataPoints.append(point) 

class Boundry():
    """this is the area of the Quad"""
    def __init__(self, x, y, dx, dy) -> None:
        self.x = x        
        self.y = y
        self.dx = dx
        self.dy = dy
        
        self.cx = (x+dx)/2
        self.cy = (y+dy)/2


class Point():
    def __init__(self, id=None, x=0, y=0) -> None:
        self.id = id
        self.x = x
        self.y = y


class QuadTree():
    def __init__(self, type, boundry, depth, node_capacity) -> None:
        self.type = type
        self.capacity = node_capacity
        self.boundry = boundry
        self.points = []
        self.depth = depth
        self.devided = False
        self.nw = None
        self.sw = None
        self.ne = None
        self.se = None

    def has_capacity(self):
        if len(self.points)<self.capacity:
            return True
        else:
            return False

    def insert_point(self, point):         
        if self.has_capacity() and not self.devided:            
            self.points.append(point)              
        else:    
            if not self.devided:
                self.devide()    
            self.insert_into_sub(point)         
    
    def insert_into_sub(self, point):        
        if  point.x >= self.boundry.x and point.x <= (self.boundry.dx/2) and point.y >= (self.boundry.dy/2) and point.y <= self.boundry.dy:        
            self.nw.insert_point(point)
            return True
        elif point.x >= self.boundry.x and point.x <= (self.boundry.dx/2) and point.y >= self.boundry.y and point.y <= (self.boundry.dy/2):             
            self.sw.insert_point(point)
            return True
        elif point.x >= (self.boundry.dx/2) and point.x <= self.boundry.dx and point.y >= (self.boundry.dy/2) and point.y <= self.boundry.dy:            
            self.ne.insert_point(point)
            return True
        elif point.x >= (self.boundry.dx/2) and point.x <= self.boundry.dx and point.y >= self.boundry.y and point.y <= (self.boundry.dy/2):             
            self.se.insert_point(point)
            return True     
        else:
            print('insert didnt work', point.id)
            return False         

    def devide(self):  
        self.nw = QuadTree('nw',Boundry(self.boundry.x, ((self.boundry.y + self.boundry.dy)/2), ((self.boundry.x+self.boundry.dx)/2), self.boundry.dy), self.depth + 1, self.capacity)
        self.sw = QuadTree('sw',Boundry(self.boundry.x, self.boundry.y, ((self.boundry.x+self.boundry.dx)/2), ((self.boundry.y + self.boundry.dy)/2)), self.depth + 1, self.capacity) 
        self.ne = QuadTree('ne',Boundry(((self.boundry.x+self.boundry.dx)/2), ((self.boundry.y + self.boundry.dy)/2), self.boundry.dx, self.boundry.dy), self.depth + 1, self.capacity)
        self.se = QuadTree('se',Boundry(((self.boundry.x+self.boundry.dx)/2), self.boundry.y, self.boundry.dx, ((self.boundry.y + self.boundry.dy)/2)), self.depth + 1, self.capacity)    

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
                if point.x >= self.boundry.x and point.x <= self.boundry.dx/2 and point.y >= self.boundry.dy/2 and point.y <= self.boundry.dy:               
                    p = self.nw.search_for_point(point, distance)
                    points.extend(p)                    
                            
                elif point.x >= self.boundry.x and point.x <= self.boundry.dx/2 and point.y >= self.boundry.y and point.y <= self.boundry.dy/2:
                    p= self.sw.search_for_point(point, distance)
                    points.extend(p)                    

                elif point.x >= self.boundry.dx/2 and point.x <= self.boundry.dx and point.y >= self.boundry.dy/2 and point.y <= self.boundry.dy:
                    p =self.ne.search_for_point(point, distance)
                    points.extend(p)                   
            
                elif point.x >= self.boundry.dx/2 and point.x <= self.boundry.dx and point.y >= self.boundry.y and point.y <= self.boundry.dy/2: 
                    p = self.se.search_for_point(point, distance)
                    points.extend(p)  

        return points        

    def extended_search(self, distance):
        pass

        
            
    def find_quad_closer_than_distance(self, point, distance):           
        # print('Find quads closer than distance in', self.type, 'depth', self.depth)
        if self.type == 'root' and not self.devided:
            return []
        elif self.type == 'root' and self.devided:
            return self.check_quads(point, distance)
        elif self.type == 'ne':
            if self.devided:
                return self.check_quads(point, distance)
            else: 
                return []
        elif self.type == 'se':
            if self.devided:
                return self.check_quads(point, distance)
            else: 
                return []
        elif self.type == 'nw':
            if self.devided:
                return self.check_quads(point, distance)
            else: 
                return []
        elif self.type == 'sw':
            if self.devided:
                return self.check_quads(point, distance)     
            else: 
                return []
        else:
            return []
        
        
    def check_quads(self, point, distance):   
        # print('Check quads', self.type, 'depth', self.depth)
        points = []
        if point.x <= self.boundry.dx/2 and point.y <= self.boundry.dy/2:
            #print('The point is located in SW')
            dif_x = self.boundry.dx/2 - point.x
            dif_y = self.boundry.dy/2 - point.y

            if dif_x <= distance and dif_y <= distance:
                # print('Check: NW, NE, SE')
                points.extend(self.nw.search_for_point(point, distance))
                points.extend(self.ne.search_for_point(point, distance))
                points.extend(self.se.search_for_point(point, distance))
                return points

            elif dif_x <= distance and not dif_y <= distance:
                # print('Check: SE')
                points.extend(self.se.search_for_point(point, distance))
                return points

            elif not dif_x <= distance and dif_y <= distance:
                # print('Check NW')
                points.extend(self.nw.search_for_point(point, distance))
                return points
            else:
                return self.points

        elif point.x <= self.boundry.dx/2 and point.y >= self.boundry.dy/2:
            # print('The point is located in NW')
            dif_x = self.boundry.dx/2 - point.x 
            dif_y = point.y - self.boundry.dy/2

            if dif_x <= distance and dif_y <= distance:
                # print('Check: SW, NE, SE')
                points.extend(self.sw.search_for_point(point, distance))
                points.extend(self.ne.search_for_point(point, distance))
                points.extend(self.se.search_for_point(point, distance))
                return points

            elif dif_x <= distance and not dif_y <= distance:
                #print('Check: NE')
                points.extend(self.ne.search_for_point(point, distance))
                return points
            
            elif not dif_x <= distance and dif_y <= distance:
                # print('Check SW')
                points.extend(self.sw.search_for_point(point, distance))
                return points    
            else:
                return self.points      
        
        elif point.x >= self.boundry.dx/2 and point.y <= self.boundry.dy/2:
            # print('The point is located in SE')
            dif_x = point.x - self.boundry.x
            dif_y = self.boundry.dy/2 - point.y

            if dif_x <= distance and dif_y <= distance:
                # print('Check: NW, NE, SW')
                points.extend(self.nw.search_for_point(point, distance))
                points.extend(self.ne.search_for_point(point, distance))
                points.extend(self.sw.search_for_point(point, distance))
                return points
            
            elif dif_x <= distance and not dif_y <= distance:
                # print('Check: SW')
                points.extend(self.sw.search_for_point(point, distance))
                return points
            
            elif not dif_x <= distance and dif_y <= distance:
                # print('Check NE')
                points.extend(self.ne.search_for_point(point, distance))
                return points
            else:
                return self.points
        
        
        elif point.x >= self.boundry.dx/2 and point.y >= self.boundry.dy/2:
            # print('The point is located in NE')
            dif_x = point.x - self.boundry.x  
            dif_y = point.y - self.boundry.y

            if dif_x <= distance and dif_y <= distance:
                # print('Check: SW, SE, SW')
                points.extend(self.sw.search_for_point(point, distance))
                points.extend(self.se.search_for_point(point, distance))
                points.extend(self.sw.search_for_point(point, distance))
                return points
            
            elif dif_x <= distance and not dif_y <= distance:
                # print('Check: SE')
                points.extend(self.se.search_for_point(point, distance))
                return points

            elif not dif_x <= distance and dif_y <= distance:
                # print('Check NW')                                       
                points.extend(self.nw.search_for_point(point, distance))
                return points
            else:
                return self.points
        else:
                return []



if __name__ == "__main__":    
    """this simple programm creats a number of points in a 2d space and saves them in a quad tree data structure.
        afterwards it will pick a random point and traverse the quad tree structur to find the specific point + 
        all of the points that are in the children and childrens children nodes and in neighboring quads that are 
        not children of the main node
        
        because I am using computer generated random numbers I run the program multiple times to test it"""


    import sys
    sys.setrecursionlimit(3000)
    print(sys.getrecursionlimit())
    file = {}
    
    num_of_experiments = 100
    number_of_points_in_area = 10000
    size_of_square_area = 10000
    node_capacity = 25
    search_radius = 100

    # run number of experiments and save results to json file
    for n in range(0, num_of_experiments):       
        dataframe = DataFrame(size_of_square_area, number_of_points_in_area, node_capacity)

        random_point_id_search = random.randint(0,number_of_points_in_area-1) 
        
        title = 'Experiment: ' + str(n) +' search point no: ' + str(random_point_id_search) + \
                ' point id: ' + str(dataframe.dataPoints[random_point_id_search].id) + ' Coordinates: [' +\
                str(dataframe.dataPoints[random_point_id_search].x) + ',' + str(dataframe.dataPoints[random_point_id_search].y) + ']'
        
        data_points = dataframe.quadTree.search_for_point(dataframe.dataPoints[random_point_id_search], 50)
        
        data = []
        for x in data_points:
            data.append('ID: '+str(x.id) + ' Coordinates [' +str(x.x)+ ' , '+ str(x.y)+ ']')
            
        file.update({title: data})
    
    with open('log.json', 'w',encoding='utf-8') as f:
        json.dump(file, f, ensure_ascii=False, indent=4)
