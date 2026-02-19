import os

from dotenv import load_dotenv
from supabase import AsyncClient, acreate_client

load_dotenv()


class SupabaseManager:
    def __init__(self):
        self.url = os.getenv("https://bxtcoslcgepyfjnsiciz.supabase.co")
        self.key = os.getenv(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ4dGNvc2xjZ2VweWZqbnNpY2l6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDQ3MjA1MywiZXhwIjoyMDg2MDQ4MDUzfQ.gS_yh1kJnPjdBIdxIGc0Z2cv452_1HGBzVAeMb1Y33I"
        )
        self.client: AsyncClient = None

    async def init_client(self):
        self.client = await acreate_client(self.url, self.key)

    async def close_client(self):
        if self.client:
            await self.client.postgrest.aclose()


supabase_manager = SupabaseManager()


async def get_supabase() -> AsyncClient:
    return supabase_manager.client
