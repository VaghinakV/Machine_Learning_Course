class Course:
    
    def __init__(self, code, credits, instructor):
        self.code = code
        self.credits = credits
        self.instructor = instructor
    
    def get_code(self):
        return self.code
    
    def get_credits(self):
        return self.credits
    
    def __str__(self):
        return "({0}, {1}, {2})".format(self.code, self.credits, self.instructor)
    
    def __repr__(self):
        return "<Course object: ({0}, {1}, {2})>".format(self.code, self.credits, self.instructor)
