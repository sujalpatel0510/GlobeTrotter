import unittest
from datetime import date
from app import create_app
from app.models import db
from app.models.user import User
from app.models.trip import Trip
from app.models.itinerary import ItinerarySection, ItineraryItem
from app.models.destination import Destination, Activity
from app.models.community import CommunityPost


class BackendTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation_and_auth(self):
        user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            username='testuser'
        )
        user.set_password('securepassword')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.check_password('securepassword'))
        self.assertFalse(user.check_password('wrongpassword'))
        self.assertEqual(user.full_name, 'Test User')
        self.assertEqual(user.initial, 'T')

    def test_trip_and_budget_calculations(self):
        user = User(first_name='Alex', email='alex@example.com')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        trip = Trip(
            owner=user,
            name='Nordic Tour',
            start_date=date(2026, 6, 1),
            end_date=date(2026, 6, 10),
            total_budget=2000.0,
            status='upcoming'
        )
        db.session.add(trip)
        db.session.commit()

        self.assertEqual(trip.duration_days, 10)
        self.assertEqual(trip.total_spent, 0.0)

        # Add section and items
        sec = ItinerarySection(trip=trip, title='Oslo', allocated_budget=1000.0)
        db.session.add(sec)
        db.session.commit()

        item1 = ItineraryItem(section=sec, title='Flight', category='transport', cost=300.0)
        item2 = ItineraryItem(section=sec, title='Hotel', category='stay', cost=500.0)
        item3 = ItineraryItem(section=sec, title='Dinner', category='meals', cost=100.0)
        db.session.add_all([item1, item2, item3])
        db.session.commit()

        self.assertEqual(trip.total_spent, 900.0)
        self.assertEqual(trip.budget_percentage, 45)
        self.assertFalse(trip.is_over_budget)

        breakdown = trip.budget_breakdown
        self.assertEqual(breakdown['transport']['spent'], 300.0)
        self.assertEqual(breakdown['stay']['spent'], 500.0)
        self.assertEqual(breakdown['meals']['spent'], 100.0)

    def test_destination_and_activity_search(self):
        dest = Destination(name='Kyoto', country='Japan', cost_index='medium')
        db.session.add(dest)
        db.session.commit()

        act = Activity(destination=dest, name='Temple Walk', category='Culture', price=25.0)
        db.session.add(act)
        db.session.commit()

        response = self.client.get('/search.html')
        self.assertEqual(response.status_code, 200)

        # Test API search
        api_res = self.client.get('/api/search?q=Kyoto')
        self.assertEqual(api_res.status_code, 200)
        data = api_res.get_json()
        self.assertTrue(any(d['name'] == 'Kyoto' for d in data['destinations']))

    def test_community_post(self):
        user = User(first_name='Sam', email='sam@example.com')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        post = CommunityPost(
            author=user,
            content='Great coffee in Lisbon!',
            tags='Lisbon,Coffee'
        )
        db.session.add(post)
        db.session.commit()

        self.assertIn('Coffee', post.tags_list)
        self.assertEqual(post.likes_count, 0)

        response = self.client.post(f'/community/{post.id}/like', headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.likes_count, 1)

    def test_all_pages_render(self):
        pages = [
            '/',
            '/index.html',
            '/register.html',
            '/dashboard.html',
            '/my-trips.html',
            '/create-trip.html',
            '/itinerary-builder.html',
            '/itinerary-view.html',
            '/search.html',
            '/community.html',
            '/calendar.html',
            '/profile.html',
            '/admin.html',
            '/shared-itinerary.html',
            '/base.html'
        ]
        for page in pages:
            res = self.client.get(page)
            self.assertEqual(res.status_code, 200, f"Page {page} failed with status {res.status_code}")

    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)


if __name__ == '__main__':
    unittest.main()
