class Student:
    
    class_by_year = { 1: 'Freshman',
                      2: 'Sophomore',
                      3: 'Junior',
                      4: 'Senior' }
    
    def __init__(self, name, gtid, year=1):
        self.name = name
        self.gtid = gtid
        self.year = year
        self.courses = {}
    
    def get_real_year(self):
        return self.class_by_year[self.year]
    
    def in_dean_list(self):
        return self.calculate_gpa() >= 3
    
    def calculate_gpa(self):
        if not self.courses:
            return 0.0
        else:
            return self.get_total_quality_points() / self.get_total_credits()
    
    def get_total_credits(self):
        return sum([course.get_credits() for course, _ in self.courses.values()])
    
    def get_total_quality_points(self):
        return sum([course.get_credits() * grade for course, grade in self.courses.values()])
    
    def drop(self, course):
        if self.is_taking(course):
            del self.courses[course.get_code()]
            return True
        else:
            return False

    def register_many(self, courses):
        for course in courses:
            self.register(course)
    
    def register(self, course):
        if not self.is_taking(course):
            self.courses[course.get_code()] = [course, 0]
    
    def assign_grade(self, course, grade):
        if self.is_taking(course):
            if grade >= 4:
                self.courses[course.get_code()][1] = 4
            elif grade <= 0:
                self.courses[course.get_code()][1] = 4
            else:
                self.courses[course.get_code()][1] = grade
    
    def is_taking(self, course):
        return course.get_code() in self.courses
    
    def set_year(self, year):
        if year <= 1:
            self.year = 1
        elif year >= 4:
            self.year = 4
        else:
            self.year = year
        
    def __str__(self):
        return "({0}, {1}, {2})".format(self.name, self.get_real_year(), self.calculate_gpa())