import os

from supabase import Client, create_client

url: str = " "
key: str = " "
supabase: Client = create_client(url, key)
