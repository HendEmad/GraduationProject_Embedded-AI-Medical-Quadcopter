import math
import random
import numpy as np
import server5


# A class to represent a node in the RRT* tree.
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = 0
        self.parent = None


# A class to represent the Informed RRT* algorithm.
class InformedRRTStar:
    def __init__(self, start, goal, x_min=1500, x_max=2000, y_min=-5000, y_max=-2000, max_iter=3000, step_size=200, goal_tol=50):
        self.start = Node(start[0], start[1])
        self.goal = Node(goal[0], goal[1])
        # self.obstacles = obstacles
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.max_iter = max_iter
        self.step_size = step_size
        self.goal_tol = goal_tol
        self.nodes = []
        self.path = []

    # Plan a path from the start to the goal using Informed RRT* algorithm.
    def plan(self):
        self.nodes.append(self.start)
        for i in range(self.max_iter):
            q_rand = self.get_random_node()
            q_near = self.get_nearest_node(q_rand)
            q_new = self.extend(q_near, q_rand)
            if q_new and not self.is_collision(q_near, q_new):
                self.nodes.append(q_new)
                self.rewire(q_new)
                if self.calculate_distance(q_new, self.goal) <= self.goal_tol:
                    self.path = self.get_path()
                    return self.path
        return None

    # Generate a random node within the state space using ellipse sampling.
    def get_random_node(self):
        if random.random() > 0.5:
            q_rand = Node(random.uniform(self.x_min, self.x_max), random.uniform(self.y_min, self.y_max))
        else:
            # Ellipse parameters
            a = self.calculate_distance(self.start, self.goal) / 2
            b = a / 2

            # Ellipse center
            xc = (self.start.x + self.goal.x) / 2
            yc = (self.start.y + self.goal.y) / 2

            # Angle of major axis
            theta = math.atan2(self.goal.y - self.start.y, self.goal.x - self.start.x)

            # Generate random point on ellipse
            t = 2 * math.pi * random.random()
            u = random.random() + random.random()
            r = u if u < 1 else 2 - u
            x = xc + r * a * math.cos(t) * math.cos(theta) - r * b * math.sin(t) * math.sin(theta)
            y = yc + r * a * math.cos(t) * math.sin(theta) + r * b * math.sin(t) * math.cos(theta)

            q_rand = Node(x, y)
        return q_rand

    # Get the nearest node in the tree to the randomly generated node.
    def get_nearest_node(self, q_rand):
        distances = [self.calculate_distance(q_rand, n) for n in self.nodes]
        min_index = distances.index(min(distances))
        return self.nodes[min_index]

    # Extend the tree towards the randomly generated node.
    def extend(self, q_near, q_rand):
        theta = math.atan2(q_rand.y - q_near.y, q_rand.x - q_near.x)
        q_new = Node(q_near.x + self.step_size * math.cos(theta), q_near.y + self.step_size * math.sin(theta))
        q_new.parent = q_near
        q_new.cost = q_near.cost + self.calculate_distance(q_near, q_new)
        return q_new

    # Rewire the tree if a new node provides a shorter path to its neighbors.
    def rewire(self, q_new):
        for node in self.nodes:
            if node == q_new or node.parent is q_new or self.is_collision(node, q_new):
                continue
            if self.calculate_distance(q_new, node) < self.step_size and node.cost > q_new.cost + self.calculate_distance(q_new, node):
                node.parent = q_new
                node.cost = q_new.cost + self.calculate_distance(q_new, node)

    # Return the optimal path from the start to the goal.
    def get_path(self):
        path = []
        node = self.nodes[-1]
        while node.parent is not None:
            path.append([node.x, node.y])
            node = node.parent
        path.append([self.start.x, self.start.y])
        path.reverse()
        return path

    # Check if the path between two nodes collides with any obstacles.
    def is_collision(self, q1, q2):
        return False
        '''
        for obstacle in self.obstacles:
            if self.line_rectangle_intersect(q1.x, q1.y, q2.x, q2.y, obstacle):
                return True
        return False
        '''

    # Check if a line segment intersects with a rectangle.
    def line_rectangle_intersect(self, x1, y1, x2, y2, rect):
        x_min, y_min, width, height = rect
        x_max = x_min + width
        y_max = y_min + height

        if x1 > x_max and x2 > x_max:
            return False
        if x1 < x_min and x2 < x_min:
            return False
        if y1 > y_max and y2 > y_max:
            return False
        if y1 < y_min and y2 < y_min:
            return False

        m = (y2 - y1) / (x2 - x1)
        y = m * (x_min - x1) + y1
        if y_min <= y <= y_max:
            return True

        y = m * (x_max - x1) + y1
        if y_min <= y <= y_max:
            return True

        x = (y_min - y1) / m + x1
        if x_min <= x <= x_max:
            return True

        x = (y_max - y1) / m + x1
        if x_min <= x <= x_max:
            return True

        return False

    # Calculate the Euclidean distance between two nodes.
    def calculate_distance(self, q1, q2):
        return math.sqrt((q1.x - q2.x) ** 2 + (q1.y - q2.y) ** 2)


start = (1991, -23)
goal_x = server5.x / 1000
goal_y = server5.y / 1000
goal = (goal_x, goal_y)
# obstacles = [(1000, -200, 20, 20)]
rrt = InformedRRTStar(start, goal)
path = rrt.plan()
if path is not None:
    print("First path: ", path)
    print("First path length = ", len(path))


    def smooth(path, weight_data=0.5, weight_smooth=0.1, tolerance=0.00001):
        newPath = [[0 for col in range(len(path[0]))] for row in range(len(path))]
        for i in range(len(path)):
            for j in range(len(path[0])):
                newPath[i][j] = path[i][j]

        change = 1
        while change > tolerance:
            change = 0
            for i in range(1, len(path) - 1):
                for j in range(len(path[0])):
                    ori = newPath[i][j]
                    newPath[i][j] = newPath[i][j] + weight_data * (path[i][j] - newPath[i][j])
                    newPath[i][j] = newPath[i][j] + weight_smooth * (
                            newPath[i + 1][j] + newPath[i - 1][j] - 2 * newPath[i][j])
                    change += abs(ori - newPath[i][j])
        return newPath


    smoothed_path = smooth(path)

    final_path = []
    for i in smoothed_path:
        i[0] /= 100
        i[1] /= 100
        final_path.append([i[0], i[1]])

    distance_togo = []
    for i in range(len(final_path)-1):
        distance = (float(final_path[i + 1][0]) - float(final_path[i][0]), float(final_path[i + 1][1]) - float(final_path[i][1]))
        distance_togo.append(distance)

    print("Final distance = ", distance_togo)
    print(len(distance_togo))
else:
    print("no path found!")