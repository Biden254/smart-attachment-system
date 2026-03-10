from fastapi import APIRouter, Query, HTTPException
from app.services.jsearch_service import fetch_internships

router = APIRouter(prefix="/internships", tags=["internships"])


@router.get("/search")
async def search_internships(
    query: str = Query(..., description="Field of study or job title"),
    location: str = Query(None, description="Preferred location"),
    page: int = Query(1, ge=1),
):
    """
    Public endpoint — no auth required.
    Both guest and logged-in users can call this.
    """
    try:
        results = await fetch_internships(
            query=query,
            location=location,
            page=page,
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch listings: {str(e)}")


@router.get("/match")
async def match_internships(
    field: str = Query(...),
    skills: str = Query(None, description="Comma-separated skills"),
    location: str = Query(None),
    page: int = Query(1, ge=1),
):
    """
    Smart match endpoint — builds a richer query from profile data.
    Called automatically for logged-in users using their saved profile.
    """
    query_parts = [field]
    if skills:
        # Take first 3 skills
        top_skills = ", ".join(skills.split(",")[:3])
        query_parts.append(top_skills)

    query = " ".join(query_parts)

    try:
        results = await fetch_internships(
            query=query,
            location=location,
            page=page,
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch matches: {str(e)}")