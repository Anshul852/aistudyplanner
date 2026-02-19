from fastapi import APIRouter, Depends, HTTPException

from ..core.supabase_client import get_supabase

router = APIRouter(prefix="/api/v1/institutional", tags=["institutional"])


@router.get("/sync")
async def sync_university_data(supabase=Depends(get_supabase)):
    """
    Fetches academic events from Supabase to anchor the roadmap.
    """
    try:
        events_res = supabase.table("academic_events").select("*").execute()
        return {"status": "Sync Complete", "data": events_res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase sync failed: {e}")
