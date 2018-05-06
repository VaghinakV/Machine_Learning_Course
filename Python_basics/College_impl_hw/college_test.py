"""
Georgia Institute of Technology - CS1301
Basic unittest for student usage in college.py homework.
"""
import unittest
from student import *
from course import *
from instructor import *

__author__  = "Daniel Barrundia"
__version__ = "1.1"
__email__   = "dbarrundia3@gatech.edu"
__date__    = "Spring 2016"

class CollegeTest(unittest.TestCase):
    def setUp(self):
        self.my_student_1 = Student("Daniel","903054641")
        self.my_student_2 = Student("Sara", "9030012396",4)
        self.my_instructor_1 = Instructor("J. Summet")
        self.my_instructor_2 = Instructor("C. Simpkins")
        self.my_instructor_3 = Instructor("M. Sweat")
        self.my_instructor_4 = Instructor("M. McDaniel")
        self.my_course_1 = Course("CS1301", 3, self.my_instructor_1)
        self.my_course_2 = Course("CS1331", 3, self.my_instructor_2)
        self.my_course_3 = Course("CS1332", 4, self.my_instructor_3)
        self.my_course_4 = Course("CS1301", 3, self.my_instructor_4)
        # TODO add more test cases yourself

    def test_init_name(self):
        self.assertEqual(self.my_student_1.name, "Daniel",  msg = "A student should be initialized with a name.")

    def test_init_id(self):
        self.assertEqual(self.my_student_1.gtid, "903054641",  msg = "A student should be initialized with an id.")

    def test_default_year(self):
        self.assertEqual(self.my_student_1.year, 1, msg = "A student has default year of 1.")

    def test_init_year(self):
        self.assertEqual(self.my_student_2.year, 4, msg = "A student should be able to be initialized with a year from 1-4.")

    def test_empty_courses(self):
        self.assertDictEqual(self.my_student_1.courses, {}, msg = "A student should have courses initialized as an empty dictionary.")

    def test_calculate_gpa_1(self):
        self.assertEqual(self.my_student_1.calculate_gpa(), 0.0, msg = "Your calculate_gpa method fails when student has no register classes.")

    def test_calculate_gpa_2(self):
        self.my_student_1.register(self.my_course_1)
        self.my_instructor_1.assign_grade(self.my_student_1, self.my_course_1, 4)
        self.assertEqual(self.my_student_1.calculate_gpa(), 4.0, msg = "Your calculate_gpa method fails when student has register a class")

    def test_calculate_gpa_3(self):
        self.my_student_1.register_many([self.my_course_1, self.my_course_2, self.my_course_3])
        self.my_instructor_1.assign_grade(self.my_student_1, self.my_course_1, 4)
        self.my_instructor_1.assign_grade(self.my_student_1, self.my_course_2, 2)
        self.my_instructor_1.assign_grade(self.my_student_1, self.my_course_3, 3)
        self.assertEqual(self.my_student_1.calculate_gpa(), 3.0, msg = "Your calculate_gpa method fails when student has register many classes")

    def test_in_dean_list(self):
        self.assertFalse(self.my_student_1.in_dean_list(), msg = "A student with no classes should have GPA of 0.0, so no dean list.")

    def test_in_dean_list_2(self):
        self.my_student_1.register(self.my_course_1)
        self.my_instructor_1.assign_grade(self.my_student_1, self.my_course_1, 4)
        self.assertTrue(self.my_student_1.in_dean_list(), msg = "A student GPA is above 3.0, so should be in dean list.")

    def test_get_real_year(self):
        self.assertEqual(self.my_student_1.get_real_year(), "Freshman")

    def test_get_real_year_2(self):
        self.assertEqual(self.my_student_2.get_real_year(), "Senior")

    def test_set_year(self):
        self.my_student_1.set_year(2)
        self.assertEqual(self.my_student_1.year, 2)

    def test_init_course_code(self):
        self.assertEqual(self.my_course_1.code, "CS1301")

    def test_init_course_credits(self):
        self.assertEqual(self.my_course_1.credits, 3)

    def test_get_course_code(self):
        self.assertEqual(self.my_course_1.get_code(), "CS1301")

    def test_get_course_credits(self):
        self.assertEqual(self.my_course_1.get_credits(), 3)

    def test_init_course_instructor(self):
        self.assertEqual(self.my_course_1.instructor, self.my_instructor_1)

    def test_add_a_course(self):
        self.my_student_1.register(self.my_course_1)
        expected = {self.my_course_1.get_code():[self.my_course_1,0]}
        self.assertDictEqual(self.my_student_1.courses, expected)

    def test_add_a_duplicate_course(self):
        self.my_student_1.register(self.my_course_1)
        self.my_student_1.register(self.my_course_4)
        expected = {self.my_course_1.get_code():[self.my_course_1,0]}
        self.assertDictEqual(self.my_student_1.courses, expected)

    def test_add_many_courses(self):
        self.my_student_1.register_many([self.my_course_1,self.my_course_2, self.my_course_3])
        expected = {self.my_course_1.get_code():[self.my_course_1,0],
        self.my_course_2.get_code():[self.my_course_2,0],
        self.my_course_3.get_code():[self.my_course_3,0]}
        self.assertDictEqual(self.my_student_1.courses, expected)

    def test_add_many_courses_with_duplicates(self):
        self.my_student_1.register_many([self.my_course_1,self.my_course_2, self.my_course_3, self.my_course_4])
        expected = {self.my_course_1.get_code(): [self.my_course_1,0], self.my_course_2.get_code():[self.my_course_2,0], self.my_course_3.get_code():[self.my_course_3,0]}
        self.assertDictEqual(self.my_student_1.courses, expected)

    def test_get_total_credits(self):
        self.my_student_1.register(self.my_course_1)
        credits = self.my_student_1.get_total_credits()
        expected_credits = self.my_course_1.get_credits()
        self.assertEqual(credits, expected_credits)

    def test_get_total_credits_2(self):
        self.my_student_1.register_many([self.my_course_1,self.my_course_2, self.my_course_3])
        credits = self.my_student_1.get_total_credits()
        expected_credits = self.my_course_1.get_credits() + self.my_course_2.get_credits() + self.my_course_3.get_credits()
        self.assertEqual(credits, expected_credits)

    def test_get_total_credits_3(self):
        self.assertEqual(self.my_student_1.get_total_credits(), 0)

    def test_drop_course(self):
        self.my_student_1.register(self.my_course_1)
        effect = self.my_student_1.drop(self.my_course_1)
        self.assertDictEqual(self.my_student_1.courses, {})
        self.assertTrue(effect)

    def test_drop_course_2(self):
        self.my_student_1.register(self.my_course_1)
        effect = self.my_student_1.drop(self.my_course_2)
        expected = {self.my_course_1.get_code(): [self.my_course_1,0]}
        self.assertDictEqual(self.my_student_1.courses, expected)
        self.assertFalse(effect)

    def test_init_instructor(self):
        self.assertEqual(self.my_instructor_1.name, "J. Summet")

    def test_assign_overflow_grade(self):
        self.my_student_1.register(self.my_course_1)
        self.my_instructor_1.assign_grade(self.my_student_1, self.my_course_1, 10)
        self.assertEqual(self.my_student_1.courses[self.my_course_1.get_code()][1],4)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CollegeTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
