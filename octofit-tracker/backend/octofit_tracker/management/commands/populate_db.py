from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()



        # Insert users
        users = [
            {"username": "thundergod", "email": "thundergod@octofit.edu", "password": "thundergodpassword"},
            {"username": "metalgeek", "email": "metalgeek@octofit.edu", "password": "metalgeekpassword"},
            {"username": "zerocool", "email": "zerocool@octofit.edu", "password": "zerocoolpassword"},
            {"username": "crashoverride", "email": "crashoverride@octofit.edu", "password": "crashoverridepassword"},
            {"username": "sleeptoken", "email": "sleeptoken@octofit.edu", "password": "sleeptokenpassword"},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Insert teams
        blue_team = {"name": "Blue Team", "members": user_ids[:3]}
        gold_team = {"name": "Gold Team", "members": user_ids[3:]}
        team_ids = db.teams.insert_many([blue_team, gold_team]).inserted_ids

        # Insert activities
        activities = [
            {"user": user_ids[0], "activity_type": "Cycling", "duration": 60*60},
            {"user": user_ids[1], "activity_type": "Crossfit", "duration": 2*60*60},
            {"user": user_ids[2], "activity_type": "Running", "duration": 1*60*60+30*60},
            {"user": user_ids[3], "activity_type": "Strength", "duration": 30*60},
            {"user": user_ids[4], "activity_type": "Swimming", "duration": 1*60*60+15*60},
        ]
        db.activity.insert_many(activities)

        # Insert leaderboard
        leaderboard = [
            {"user": user_ids[0], "score": 100},
            {"user": user_ids[1], "score": 90},
            {"user": user_ids[2], "score": 95},
            {"user": user_ids[3], "score": 85},
            {"user": user_ids[4], "score": 80},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Insert workouts
        workouts = [
            {"name": "Cycling Training", "description": "Training for a road cycling event"},
            {"name": "Crossfit", "description": "Training for a crossfit competition"},
            {"name": "Running Training", "description": "Training for a marathon"},
            {"name": "Strength Training", "description": "Training for strength"},
            {"name": "Swimming Training", "description": "Training for a swimming competition"},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
