class CourseNotFound(Exception):
    def __init__(self, course : str):
        self.course = course
        self.message = f"Course not found : {self.course}"
        super().__init__(self.message)
