from datetime import date, datetime
from app.models import db
from app.models.user import User
from app.models.trip import Trip
from app.models.itinerary import ItinerarySection, ItineraryItem
from app.models.destination import Destination, Activity
from app.models.community import CommunityPost


def seed_database():
    """Seeds the database with complete sample data if not already populated."""
    if User.query.first():
        print("Database already contains data. Skipping seeding.")
        return

    print("Seeding database with sample users, destinations, trips, and community posts...")

    # 1. Create Users
    maya = User(
        first_name='Maya',
        last_name='Rao',
        username='maya.wanders',
        email='maya@example.com',
        phone='+91 98765 43210',
        city='Ahmedabad',
        country='India',
        about='Slow traveler, street food enthusiast, and lover of mountain trails.',
        avatar_url='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
        is_admin=False
    )
    maya.set_password('password123')

    diego = User(
        first_name='Diego',
        last_name='Martins',
        username='diego.m',
        email='diego@example.com',
        phone='+55 11 98765-4321',
        city='São Paulo',
        country='Brazil',
        about='Photographer exploring historic towns and coastal islands.',
        avatar_url='https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
        is_admin=False
    )
    diego.set_password('password123')

    priya = User(
        first_name='Priya',
        last_name='Sharma',
        username='priya.travels',
        email='priya@example.com',
        phone='+91 99887 76655',
        city='Mumbai',
        country='India',
        about='Passionate hiker and solo female traveler.',
        avatar_url='https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80',
        is_admin=False
    )
    priya.set_password('password123')

    tomas = User(
        first_name='Tomás',
        last_name='Reyes',
        username='tomas.reyes',
        email='tomas@example.com',
        city='Madrid',
        country='Spain',
        about='Architecture lover and road trip veteran.',
        avatar_url='https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80',
        is_admin=False
    )
    tomas.set_password('password123')

    admin = User(
        first_name='Admin',
        last_name='GlobeTrotter',
        username='admin',
        email='admin@globetrotter.com',
        city='San Francisco',
        country='USA',
        about='Platform administrator account.',
        avatar_url='https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80',
        is_admin=True
    )
    admin.set_password('admin123')

    db.session.add_all([maya, diego, priya, tomas, admin])
    db.session.flush()

    # 2. Create Destinations
    dest_kyoto = Destination(name='Kyoto', country='Japan', cost_index='medium', image_pattern='', trips_count=412, trend='↑ 18%', description='Ancient capital of Japan with historic temples and gardens.')
    dest_lisbon = Destination(name='Lisbon', country='Portugal', cost_index='medium', image_pattern='pat-1', trips_count=301, trend='↑ 9%', description='Sunlit coastal city famous for historic trams and pastéis.')
    dest_cusco = Destination(name='Cusco', country='Peru', cost_index='low', image_pattern='pat-2', trips_count=244, trend='↑ 4%', description='Gateway to Machu Picchu and heart of Inca heritage.')
    dest_reykjavik = Destination(name='Reykjavík', country='Iceland', cost_index='high', image_pattern='', trips_count=198, trend='↓ 2%', description='Capital of fire and ice, hot springs and Northern Lights.')
    dest_pokhara = Destination(name='Pokhara', country='Nepal', cost_index='low', image_pattern='', trips_count=156, trend='↑ 12%', description='Lakeside Himalayan adventure haven.')
    dest_interlaken = Destination(name='Interlaken', country='Switzerland', cost_index='high', image_pattern='pat-1', trips_count=210, trend='↑ 7%', description='Swiss Alpine hub surrounded by peaks and lakes.')
    dest_oludeniz = Destination(name='Ölüdeniz', country='Türkiye', cost_index='medium', image_pattern='pat-2', trips_count=145, trend='↑ 15%', description='Turquoise coast famous for blue lagoon and paragliding.')
    dest_hanoi = Destination(name='Hanoi', country='Vietnam', cost_index='low', image_pattern='', trips_count=270, trend='↑ 11%', description='Vibrant street food, old quarters, and colonial architecture.')
    dest_chiangmai = Destination(name='Chiang Mai', country='Thailand', cost_index='low', image_pattern='pat-1', trips_count=235, trend='↑ 8%', description='Northern cultural center with mountain temples.')
    dest_ubud = Destination(name='Ubud', country='Indonesia', cost_index='low', image_pattern='pat-2', trips_count=180, trend='↑ 14%', description='Bali arts capital with lush terraced rice fields.')
    dest_siemreap = Destination(name='Siem Reap', country='Cambodia', cost_index='low', image_pattern='', trips_count=160, trend='↑ 5%', description='Home of the breathtaking Angkor Wat temple complex.')

    destinations = [
        dest_kyoto, dest_lisbon, dest_cusco, dest_reykjavik, dest_pokhara,
        dest_interlaken, dest_oludeniz, dest_hanoi, dest_chiangmai, dest_ubud, dest_siemreap
    ]
    db.session.add_all(destinations)
    db.session.flush()

    # 3. Create Activities
    activities = [
        Activity(destination=dest_pokhara, name='Tandem paragliding over Pokhara', category='Adventure', price=85.0, duration='45 min flight', description='includes pickup · from $85', stamp_color='coral', bookings_count=512),
        Activity(destination=dest_interlaken, name='Coastal paragliding, Interlaken', category='Adventure', price=180.0, duration='20 min flight', description='mountain landing · from $180', stamp_color='coral', bookings_count=380),
        Activity(destination=dest_hanoi, name='Night market street food crawl', category='Food & Drink', price=32.0, duration='3 hr walking tour', description='6 tastings · from $32', stamp_color='teal', bookings_count=987),
        Activity(destination=dest_kyoto, name='Old town walking tour with local guide', category='Culture', price=24.0, duration='2.5 hr', description='small groups · from $24', stamp_color='gold', bookings_count=1204),
        Activity(destination=dest_oludeniz, name='Sunset paragliding, Oludeniz', category='Adventure', price=95.0, duration='30 min flight', description='beach landing · from $95', stamp_color='coral', bookings_count=290),
        Activity(destination=dest_chiangmai, name='Temple hopping & sunrise cycling', category='Culture', price=45.0, duration='4 hr', description='includes temple passes · from $45', stamp_color='gold', bookings_count=640),
        Activity(destination=dest_ubud, name='Cooking class & organic farm tour', category='Food & Drink', price=40.0, duration='3.5 hr', description='hands-on workshop · from $40', stamp_color='teal', bookings_count=510),
        Activity(destination=dest_siemreap, name='Angkor Wat sunrise tuk-tuk tour', category='Culture', price=35.0, duration='Full day', description='guided exploration · from $35', stamp_color='gold', bookings_count=820),
        Activity(destination=dest_lisbon, name='Pastel de Nata bakery masterclass', category='Food & Drink', price=55.0, duration='2 hr', description='baking workshop · from $55', stamp_color='teal', bookings_count=430)
    ]
    db.session.add_all(activities)
    db.session.flush()

    # 4. Create Trips for Maya Rao
    
    # Trip 1: Japan Adventure (Ongoing)
    trip_japan = Trip(
        owner=maya,
        name='Japan Adventure',
        start_date=date(2026, 1, 16),
        end_date=date(2026, 1, 28),
        start_place='Tokyo',
        description='Tokyo → Kyoto → Osaka → Hakone. 12 days across 4 ancient and modern cities.',
        total_budget=5000.0,
        pattern='pat-1',
        status='ongoing',
        is_public=True
    )
    db.session.add(trip_japan)
    db.session.flush()

    # Japan Sections
    sec_tokyo = ItinerarySection(
        trip=trip_japan,
        section_order=1,
        title='Tokyo, Japan',
        description='Exploring Shinjuku, Shibuya, Asakusa, and digital arts.',
        date_range_text='Jan 16 → Jan 20',
        allocated_budget=2000.0
    )
    sec_kyoto = ItinerarySection(
        trip=trip_japan,
        section_order=2,
        title='Kyoto, Japan',
        description='Ryokan stay, traditional kaiseki, shrines, and bamboo forests.',
        date_range_text='Jan 20 → Jan 24',
        allocated_budget=1800.0
    )
    sec_osaka = ItinerarySection(
        trip=trip_japan,
        section_order=3,
        title='Osaka & Hakone',
        description='Street food tours and relaxing hot spring onsen views.',
        date_range_text='Jan 24 → Jan 28',
        allocated_budget=1200.0
    )
    db.session.add_all([sec_tokyo, sec_kyoto, sec_osaka])
    db.session.flush()

    # Japan Items
    japan_items = [
        # Day 1
        ItineraryItem(section=sec_tokyo, title='Arrive Tokyo Narita', description='Airport transfer to Shinjuku hotel', time_label='9:40 AM', category='transport', cost=38.0, day_number=1, order_index=1),
        ItineraryItem(section=sec_tokyo, title='Shibuya Crossing & Sky Deck', description='Sightseeing & observation deck', time_label='2:00 PM', category='activities', cost=14.0, day_number=1, order_index=2),
        ItineraryItem(section=sec_tokyo, title='Ramen dinner in Golden Gai', description='Food & drink', time_label='7:30 PM', category='meals', cost=22.0, day_number=1, order_index=3),
        # Day 2
        ItineraryItem(section=sec_tokyo, title='Senso-ji Temple, Asakusa', description='Culture', time_label='9:00 AM', category='activities', cost=0.0, day_number=2, order_index=4),
        ItineraryItem(section=sec_tokyo, title='TeamLab Planets', description='Experience', time_label='3:00 PM', category='activities', cost=32.0, day_number=2, order_index=5),
        ItineraryItem(section=sec_tokyo, title='Shinjuku Hotel 4-night stay', description='Central Shinjuku boutique accommodation', time_label='Check-in', category='stay', cost=920.0, day_number=1, order_index=6),
        ItineraryItem(section=sec_tokyo, title='Shinkansen Bullet Train Pass', description='Tokyo to Kyoto fast transit', time_label='10:00 AM', category='transport', cost=460.0, day_number=3, order_index=7),
        
        # Kyoto
        ItineraryItem(section=sec_kyoto, title='Fushimi Inari Shrine at sunrise', description='Culture', time_label='6:30 AM', category='activities', cost=0.0, day_number=5, order_index=8),
        ItineraryItem(section=sec_kyoto, title='Ryokan check-in & kaiseki dinner', description='Stay & food', time_label='5:00 PM', category='stay', cost=700.0, day_number=5, order_index=9),
        ItineraryItem(section=sec_kyoto, title='Arashiyama Bamboo Grove & Tea House', description='Culture & Matcha tasting', time_label='11:00 AM', category='activities', cost=24.0, day_number=6, order_index=10),
        ItineraryItem(section=sec_kyoto, title='Gion Evening Food Walk', description='Local izakaya tour', time_label='7:00 PM', category='meals', cost=160.0, day_number=6, order_index=11),
        ItineraryItem(section=sec_kyoto, title='Local Kyoto Transit Passes', description='Buses and subway', time_label='All days', category='transport', cost=80.0, day_number=5, order_index=12),
        
        # Osaka & Hakone
        ItineraryItem(section=sec_osaka, title='Dotonbori Street Food Feast', description='Takoyaki and okonomiyaki', time_label='6:00 PM', category='meals', cost=75.0, day_number=8, order_index=13),
        ItineraryItem(section=sec_osaka, title='Hakone Onsen & Mt Fuji Cable Car', description='Activities & scenic pass', time_label='1:00 PM', category='activities', cost=185.0, day_number=9, order_index=14),
        ItineraryItem(section=sec_osaka, title='Hakone Traditional Onsen Stay', description='Scenic hot spring resort', time_label='Check-in', category='stay', cost=800.0, day_number=9, order_index=15),
        ItineraryItem(section=sec_osaka, title='Return Airport Express', description='Hakone to Narita', time_label='12:00 PM', category='transport', cost=600.0, day_number=12, order_index=16),
    ]
    db.session.add_all(japan_items)

    # Trip 2: NYC Getaway (Upcoming)
    trip_nyc = Trip(
        owner=maya,
        name='NYC Getaway',
        start_date=date(2026, 9, 14),
        end_date=date(2026, 9, 19),
        start_place='New York City',
        description='5-day urban escape exploring Broadway, Central Park, and Brooklyn architecture.',
        total_budget=3000.0,
        pattern='',
        status='upcoming',
        is_public=False
    )
    db.session.add(trip_nyc)
    db.session.flush()

    sec_nyc = ItinerarySection(
        trip=trip_nyc,
        section_order=1,
        title='Manhattan & Brooklyn',
        description='City sightseeing, museums, and food tours.',
        date_range_text='Sep 14 → Sep 19',
        allocated_budget=3000.0
    )
    db.session.add(sec_nyc)
    db.session.flush()

    nyc_items = [
        ItineraryItem(section=sec_nyc, title='JFK AirTrain & Metro Pass', description='Transit to Manhattan', time_label='11:00 AM', category='transport', cost=40.0, day_number=1, order_index=1),
        ItineraryItem(section=sec_nyc, title='Midtown Boutique Hotel Stay', description='4 nights stay', time_label='Check-in', category='stay', cost=1100.0, day_number=1, order_index=2),
        ItineraryItem(section=sec_nyc, title='Broadway Show Tickets', description='Orchestra seating', time_label='7:00 PM', category='activities', cost=320.0, day_number=2, order_index=3),
        ItineraryItem(section=sec_nyc, title='Brooklyn Bridge & DUMBO Dining', description='Dinner and sunset walk', time_label='5:30 PM', category='meals', cost=280.0, day_number=3, order_index=4),
    ]
    db.session.add_all(nyc_items)

    # Trip 3: Southeast Asia Loop (Draft)
    trip_sea = Trip(
        owner=maya,
        name='Southeast Asia Loop',
        start_date=None,
        end_date=None,
        start_place='Hanoi, Vietnam',
        description='Add every stop as its own section — dates, budget, and activities live right where you can see them.',
        total_budget=2500.0,
        pattern='pat-1',
        status='draft',
        is_public=False
    )
    db.session.add(trip_sea)
    db.session.flush()

    sec_sea_1 = ItinerarySection(
        trip=trip_sea,
        section_order=1,
        title='Hanoi, Vietnam',
        description='All the necessary information about this section. This can be anything like a travel leg, hotel stay, or any other activity block.',
        date_range_text='Jun 10 → Jun 13',
        allocated_budget=420.0
    )
    sec_sea_2 = ItinerarySection(
        trip=trip_sea,
        section_order=2,
        title='Ha Long Bay, Vietnam',
        description='All the necessary information about this section. This can be anything like a travel leg, hotel stay, or any other activity block.',
        date_range_text='Jun 13 → Jun 15',
        allocated_budget=260.0
    )
    sec_sea_3 = ItinerarySection(
        trip=trip_sea,
        section_order=3,
        title='Chiang Mai, Thailand',
        description='All the necessary information about this section. This can be anything like a travel leg, hotel stay, or any other activity block.',
        date_range_text='Jun 15 → Jun 20',
        allocated_budget=510.0
    )
    db.session.add_all([sec_sea_1, sec_sea_2, sec_sea_3])

    # Trip 4: Paris Trip (Completed)
    trip_paris = Trip(
        owner=maya,
        name='Paris Trip',
        start_date=date(2026, 3, 10),
        end_date=date(2026, 3, 15),
        start_place='Paris, France',
        description='5 days in the city of light — art, bakeries, and riverside strolls.',
        total_budget=2000.0,
        pattern='',
        status='completed',
        is_public=True
    )
    db.session.add(trip_paris)
    db.session.flush()

    sec_paris = ItinerarySection(
        trip=trip_paris,
        section_order=1,
        title='Paris & Montmartre',
        description='Museums, walking tours, and culinary delights.',
        date_range_text='Mar 10 → Mar 15',
        allocated_budget=2000.0
    )
    db.session.add(sec_paris)
    db.session.flush()

    paris_items = [
        ItineraryItem(section=sec_paris, title='Flight & Airport Transfer', description='RER B Train & Flights', time_label='10:00 AM', category='transport', cost=340.0, day_number=1, order_index=1),
        ItineraryItem(section=sec_paris, title='Le Marais Hotel Stay', description='5 nights boutique stay', time_label='Check-in', category='stay', cost=1180.0, day_number=1, order_index=2),
        ItineraryItem(section=sec_paris, title='Louvre Museum & Seine Cruise', description='Timed entry ticket & cruise', time_label='9:00 AM', category='activities', cost=160.0, day_number=2, order_index=3),
        ItineraryItem(section=sec_paris, title='Montmartre Bistros & Cafes', description='Dining & wine', time_label='8:00 PM', category='meals', cost=400.0, day_number=3, order_index=4),
    ]
    db.session.add_all(paris_items)

    # Trip 5: Sardinia Sailing Week (Completed)
    trip_sardinia = Trip(
        owner=maya,
        name='Sardinia Sailing Week',
        start_date=date(2025, 7, 3),
        end_date=date(2025, 7, 10),
        start_place='Cagliari, Italy',
        description='Sailing coastal waters and secret coves around southern Sardinia.',
        total_budget=3500.0,
        pattern='pat-2',
        status='completed',
        is_public=True
    )
    db.session.add(trip_sardinia)
    db.session.flush()

    sec_sardinia = ItinerarySection(
        trip=trip_sardinia,
        section_order=1,
        title='Cagliari Coastline',
        description='Boat rental and seaside village visits.',
        date_range_text='Jul 03 → Jul 10',
        allocated_budget=3500.0
    )
    db.session.add(sec_sardinia)
    db.session.flush()

    sardinia_items = [
        ItineraryItem(section=sec_sardinia, title='Boat charter split', description='Sailing boat rental', time_label='Morning', category='activities', cost=1200.0, day_number=1, order_index=1),
        ItineraryItem(section=sec_sardinia, title='Coastal Villa Stay', description='7 nights share', time_label='Check-in', category='stay', cost=1400.0, day_number=1, order_index=2),
        ItineraryItem(section=sec_sardinia, title='Fresh Seafood Meals', description='Harbor restaurants', time_label='Evenings', category='meals', cost=450.0, day_number=2, order_index=3),
    ]
    db.session.add_all(sardinia_items)

    # 5. Create Community Posts
    posts = [
        CommunityPost(
            author=diego,
            trip=trip_japan,
            trip_name='Japan Adventure',
            content="Kyoto in cherry blossom season is worth every yen — but book the ryokan three months out or you'll be stuck paying double like I was.",
            tags='Japan,Budget tip',
            avatar_color_class='teal',
            likes_count=18,
            created_at=datetime(2026, 1, 20, 14, 30)
        ),
        CommunityPost(
            author=priya,
            trip=trip_sardinia,
            trip_name='Sardinia Sailing Week',
            content="Rented a small boat out of Cagliari instead of joining a group tour — cost about the same split three ways and we picked every stop ourselves.",
            tags='Italy,Sailing',
            avatar_color_class='gold',
            likes_count=24,
            created_at=datetime(2026, 1, 19, 10, 15)
        ),
        CommunityPost(
            author=tomas,
            trip=trip_paris,
            trip_name='Paris Trip',
            content="Skipped the Louvre queue entirely by booking the 9am timed slot — walked straight in while the line outside was already an hour long.",
            tags='France,Museums',
            avatar_color_class='coral',
            likes_count=31,
            created_at=datetime(2026, 1, 17, 8, 45)
        )
    ]
    db.session.add_all(posts)

    db.session.commit()
    print("Database seeded successfully with demo trips, users, and community data!")
