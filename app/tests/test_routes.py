import unittest
from app import create_app
from models import db, Timetable, Classes, Courses, Staff

class TestTimetableRoutes(unittest.TestCase):
    def setUp(self):
        """Set up a test client and an in-memory database."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Add sample data
            self.populate_sample_data()

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def populate_sample_data(self):
        """Populate the database with sample data for testing."""
        # Clear existing data
        db.session.query(Timetable).delete()
        db.session.query(Courses).delete()
        db.session.query(Classes).delete()
        db.session.query(Staff).delete()

        # Add sample staff
        staff1 = Staff(name="Dr. Alan Turing", email="alan.turing@example.com")
        staff2 = Staff(name="Dr. Grace Hopper", email="grace.hopper@example.com")
        db.session.add_all([staff1, staff2])

        # Add sample courses
        course1 = Courses(course_code="CS101", course_name="Intro to CS", classes_per_week=3, eligible_teachers="1,2")
        course2 = Courses(course_code="MATH101", course_name="Calculus I", classes_per_week=2, eligible_teachers="1")
        db.session.add_all([course1, course2])

        # Add sample classes
        class1 = Classes(class_name="BSc CS 1st Year", degree="BSc", semester=1, batch_number="A", default_room="Room 101")
        db.session.add(class1)

        # Add sample timetable entry
        timetable_entry = Timetable(class_id=1, day=0, period=1, course_id=1, staff_id=1)
        db.session.add(timetable_entry)

        db.session.commit()

    def test_generate_timetable(self):
        """Test the timetable generation route."""
        response = self.client.post('/timetable/generate-timetable')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Timetable generated successfully', response.get_data(as_text=True))

    def test_view_timetable(self):
        """Test fetching the timetable for a specific class."""
        response = self.client.get('/timetable/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('class_id', response.get_data(as_text=True))

    def test_export_timetable(self):
        """Test exporting the timetable as a CSV file."""
        response = self.client.get('/timetable/export/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Day,Period,Course ID,Staff ID', response.get_data(as_text=True))

    def test_add_timetable_entry(self):
        """Test adding a new timetable entry."""
        response = self.client.post('/timetable', json={
            'class_id': 1,
            'day': 0,
            'period': 2,
            'course_id': 1,
            'staff_id': 1
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Timetable entry added successfully', response.get_data(as_text=True))

    def test_add_duplicate_timetable_entry(self):
        """Test adding a duplicate timetable entry."""
        response = self.client.post('/timetable', json={
            'class_id': 1,
            'day': 0,
            'period': 1,
            'course_id': 1,
            'staff_id': 1
        })
        self.assertEqual(response.status_code, 409)
        self.assertIn('Timetable entry for this period already exists', response.get_data(as_text=True))

    def test_update_timetable_entry(self):
        """Test updating an existing timetable entry."""
        response = self.client.put('/timetable/1', json={
            'day': 1,
            'period': 3
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Timetable entry updated successfully', response.get_data(as_text=True))

    def test_delete_timetable_entry(self):
        """Test deleting a timetable entry."""
        response = self.client.delete('/timetable/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Timetable entry deleted successfully', response.get_data(as_text=True))

    def test_delete_nonexistent_entry(self):
        """Test deleting a non-existent timetable entry."""
        response = self.client.delete('/timetable/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Timetable entry not found', response.get_data(as_text=True))

    def test_add_timetable_entry_missing_fields(self):
        """Test adding a timetable entry with missing fields."""
        response = self.client.post('/timetable/', json={
            'class_id': 1,
            'day': 0,
            # 'period' is missing
            'course_id': 1,
            'staff_id': 1
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('All fields', response.json['message'])

    def test_delete_nonexistent_timetable_entry(self):
        """Test deleting a timetable entry that doesn't exist."""
        response = self.client.delete('/timetable/999')  # Non-existent ID
        self.assertEqual(response.status_code, 404)
        self.assertIn('Timetable entry not found', response.json['message'])


if __name__ == '__main__':
    unittest.main()