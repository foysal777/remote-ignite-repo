import time
import json
import jwt

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async


class TimerConsumer(AsyncWebsocketConsumer):

    # ---------------- DB HELPERS ---------------- #

    @database_sync_to_async
    def get_user(self, user_id):
        User = get_user_model()
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def update_user_time(self, user_id, new_time):
        User = get_user_model()
        return User.objects.filter(id=user_id).update(total_time=new_time)

    def is_admin_user(self):
        return getattr(self.user, "role", "user") == "admin"

    # ---------------- CONNECT ---------------- #

    async def connect(self):
        print("\n================ CONNECT EVENT ================")

        # ---- Get token from query string ----
        query_string = self.scope["query_string"].decode()
        token = None

        if "token=" in query_string:
            token = query_string.split("token=")[-1]

        if not token:
            print("❌ No token provided")
            await self.close()
            return

        # ---- Decode JWT ----
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            self.user = await self.get_user(user_id)
        except Exception as e:
            print(f"❌ Invalid token: {e}")
            await self.close()
            return

        # ---- Role check ----
        self.is_admin = self.is_admin_user()
        self.old_total_time = int(self.user.total_time)

        print(f"User: {self.user.email}")
        print(f"Role: {self.user.role}")
        print(f"Stored total_time: {self.old_total_time}s")

        # ---- Non-admin: block if no time ----
        if not self.is_admin and self.old_total_time <= 0:
            print("❌ No remaining time. Connection closed.")
            await self.close()
            return

        # ---- Start timer ----
        self.start_time = time.time()
        await self.accept()

        # ---- WS response ----
        await self.send(json.dumps({
            "message": "Timer started",
            "remaining_time": -1 if self.is_admin else self.old_total_time,
            "is_unlimited": self.is_admin,
            "role": self.user.role,
            "user_type": self.user.plan_type,
        }))

        print("✅ WebSocket connected")
        print("=================================================\n")

    # ---------------- DISCONNECT ---------------- #

    async def disconnect(self, close_code):
        print("\n================ DISCONNECT EVENT ================")

        if not hasattr(self, "start_time"):
            print("No valid session found.")
            return

        session_time = int(time.time() - self.start_time)

        # ---- Admin: unlimited, no DB update ----
        if self.is_admin:
            print(f"User: {self.user.email} (ADMIN)")
            print(f"Session time: {session_time}s")
            print("✅ Unlimited user — no DB update")
            return

        # ---- Normal user: deduct time ----
        new_total_time = self.old_total_time - session_time
        if new_total_time < 0:
            new_total_time = 0

        await self.update_user_time(self.user.id, new_total_time)

        print(f"User: {self.user.email}")
        print(f"Session used: {session_time}s")
        print(f"Remaining time: {new_total_time}s")
        print("✅ Time updated in DB")

        # Optional send (socket may already be closed)
        try:
            await self.send(json.dumps({
                "message": "Timer stopped",
                "session_time": session_time,
                "remaining_time": new_total_time,
                "is_unlimited": False,
            }))
        except:
            pass

