class Instructor:
    
    def __init__(self, name):
        self.name = name
    
    def assign_grade(self, student, course, grade):
        student.assign_grade(course, grade)

    def __str__(self):
        return "{0}".format(self.name)

    def __repr__(self):
        return "<Instructor object: ({0})>".format(self.name)
