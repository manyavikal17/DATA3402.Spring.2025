import math
class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x= int(slope * y)
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))
        
    def __repr__(self):
        return f"Canvas({self.width}, {self.height})"   

class Shape:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
    def paint(self, canvas):
        raise NotImplementedError("Subclasses must implement this method")

    def area(self):
        raise NotImplementedError("Subclasses must implement this method")
        
    def perimeter(self):
        raise NotImplementedError("Subclasses must implement this method")
        
    def circumference(self):
        raise NotImplementedError("Subclasses must implement this method")
       
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
        
    def set_x(self, x):
        self.__x = x
    
    def set_y(self, y):
        self.__y = y
    
    def parameters(self):
        raise NotImplementedError("Subclasses must implement this method")

    def is_inside(self, x, y):
        raise NotImplementedError("Subclasses must implement this method")
   
    def overlaps(self, other):
        for x, y in other.get_boundary_points():
            if self.is_inside(x, y):
                return True
        return False
    
        
class Circle(Shape):
    def __init__(self, radius, x, y):
        super().__init__(x,y)
        self.__radius = radius
        
    def get_radius(self):
        return self.__radius
    
    def set_radius(self, radius):
        if radius > 0:
            self.__radius = radius
        else: 
            raise ValueError("Radius must be a positive value.")
    
    def get_area(self):
        return 3.14 * self.__radius ** 2 
    
    def get_circumference(self):
        return 2 * 3.14 * self.__radius
    
    def get_boundary_points(self):
        points = []
        step = 360 // 16
        for i in range(16):
            angle = step * i
            x_offset = round(self.__radius * (angle % 4) / 2, 2)
            y_offset = round(self.__radius * ((angle + 90) % 4) / 2, 2)
            points.append((self.get_x() + x_offset, self.get_y() + y_offset))
        return points
    
    def is_inside(self, x, y):
        return (x - self.get_x())**2 + (y - self.get_y())**2 <= self.__radius**2
    
    def paint(self, canvas):
        r = self.get_radius()
        cx = self.get_x()
        cy = self.get_y()
        for i in range(-r, r + 1):
            for j in range(-r, r + 1):
                if math.sqrt(i**2 + j**2) <= r:
                    canvas.set_pixel(cx + i, cy + j, '*')
                    
    def __repr__(self):
        return f"Circle({self.get_radius()}, {self.get_x()}, {self.get_y()})"

    
class Rectangle(Shape):
    def __init__(self, length, width, x, y):
        super().__init__(x,y)
        self.__length = length
        self.__width = width
        
    def get_length(self):
        return self.__length
    
    def get_width(self):
        return self.__width
    
    def set_length(self, length):
        if length > 0:
            self.__length = length
        else: 
            raise ValueError("Length must be a positive value.")
    
    def set_width(self, width):
        if width > 0:
            self.__width = width
        else: 
            raise ValueError("Width must be a positive value.")
    
    def get_area(self):
        return self.__length * self.__width
    
    def get_perimeter(self):
        return 2 * (self.__length + self.__width)
    
    def get_boundary_points(self):
        points = []
        step_x = self.__length / 4
        step_y = self.__width / 4
        for i in range(4):
            points.append((self.get_x() + i * step_x, self.get_y()))
            points.append((self.get_x() + i * step_x, self.get_y() + self.__width))
            points.append((self.get_x(), self.get_y() + i * step_y))
            points.append((self.get_x() + self.__length, self.get_y() + i * step_y))
        return points[:16]
    
    def is_inside(self,x, y):
        return self.get_x() <= x <= self.get_x() + self.__length and self.get_y() <= y <= self.get_y() + self.__width
    
    def paint(self, canvas):
        x = self.get_x()
        y = self.get_y()
        length = self.get_length()
        width = self.get_width()
        for i in range(min(length, canvas.width - x)): 
            for j in range(min(width, canvas.height - y)):
                canvas.set_pixel(x + i, y + j, '*')
   
    def __repr__(self):
        return f"Rectangle({self.get_length()}, {self.get_width()}, {self.get_x()}, {self.get_y()})" 

    
class Triangle(Shape):
    def __init__(self, base, height, side1, side2, side3, x, y):
        super().__init__(x,y)
        self.__base = base
        self.__height = height
        self.__side1 = side1
        self.__side2 = side2
        self.__side3 = side3
        
    def get_base(self):
        return self.__base
    
    def get_height(self):
        return self.__height
    
    def get_sides(self):
        return self.__side1, self.__side2, self.__side3
    
    def set_base(self, base):
        if base > 0:
            self.__base = base
        else:
            raise ValueError("Base must be a positive value.")
    
    def set_height(self, height):
        if height > 0:
            self.__height = height
        else:
            raise ValueError("Height must be a positive value.")
            
    def set_sides(self, side1, side2, side3):
        if side1 > 0 and side2 > 0 and side3 > 0:
            self.__side1 = side1
            self.__side2 = side2
            self.__side3 = side3
        else:
            raise ValueError("All sides must be positive values.")
            
    def area(self):
        return 0.5 * self.__base * self.__height
    
    def perimeter(self):
        return self.__side1 + self.__side2 + self.__side3
    
    def get_boundary_points(self):
        points = [(self.get_x(), self.get_y()),
                (self.get_x() + self.__base, self.get_y()),
                (self.get_x() + self.__base / 2, self.get_y() + self.__height)]
        step = self.__base // 5
        for i in range(1, 5):
            points.append((self.get_x() + i * step, self.get_y()))
        step = self.__height // 5
        for i in range(1, 5):
            points.append((self.get_x() + self.__base / 2, self.get_y() + i * step))
        return points[:16]
    
    def is_inside(self, x, y):
        area_total = self.area()
        area1 = 0.5 * abs(self.get_x() * (self.get_y() + self.__height - y) + (self.get_x() + self.__base / 2) * (y - self.get_y()) + x * (self.get_y() - (self.get_y() + self.__height)))
        area2 = 0.5 * abs(x * (self.get_y() + self.__height - self.get_y()) + (self.get_x() + self.__base / 2) * (self.get_y() - y) + self.get_x() * (y - (self.get_y() + self.__height)))
        area3 = 0.5 * abs(self.get_x() * (self.get_y() - y) + x * ((self.get_y() + self.__height) - self.get_y()) + (self.get_x() + self.__base / 2) * (y - self.get_y()))
        return round(area1 + area2 + area3, 5) == round(area_total, 5)
    
    def paint(self, canvas):
        x = self.get_x()
        y = self.get_y()
        height = self.get_height()  
        for i in range(height):
           for j in range(i + 1):
                canvas.set_pixel(x + j, y + i, '*')
                
    def __repr__(self): 
        s1, s2, s3 = self.get_sides()
        return f"Triangle({self.get_base()}, {self.get_height()}, {s1}, {s2}, {s3}, {self.get_x()}, {self.get_y()})"
   
 
class CompoundShape(Shape):
    def __init__(self, shapes=None):
        super().__init__(0, 0)
        self.shapes = shapes if shapes is not None else []
    
    def add_shape(self, shape):
        self.shapes.append(shape)
    
    def paint(self, canvas):
        for shape in self.shapes:
            if hasattr(shape, 'paint'):
                shape.paint(canvas)
            else:
                raise AttributeError(f"{type(shape).__name__} object has no attribute 'paint'")