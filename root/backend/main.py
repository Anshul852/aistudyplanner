from typing import List, Optional

from app.api.institutional import router as institutional_router
from app.services.bandit import scheduler_bandit
from app.services.spacing import GeneticSyllabusOptimizer
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AdaptiveLabs AI Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(institutional_router)


class TopicItem(BaseModel):
    id: str
    name: str
    weight: int
    description: Optional[str] = None


class OptimizationRequest(BaseModel):
    topics: List[TopicItem]
    days: int
    velocity: str = "Medium"


class FeedbackRequest(BaseModel):
    arm_index: int
    reward: float


BANDIT_ARMS = [
    {"population_size": 30, "mutation_rate": 0.10},
    {"population_size": 50, "mutation_rate": 0.15},
    {"population_size": 80, "mutation_rate": 0.20},
]


@app.get("/")
async def root():
    return {
        "status": "Online",
        "core": "AdaptiveLabs AI",
        "node": "Sastra University Lab",
        "documentation": "/docs",
    }


@app.post("/api/v1/optimize-personal-roadmap")
async def optimize_roadmap(data: OptimizationRequest):
    try:
        topic_dicts = [t.model_dump() for t in data.topics]

        arm_index = scheduler_bandit.choose_arm()
        config = BANDIT_ARMS[arm_index]

        optimizer = GeneticSyllabusOptimizer(
            population_size=config["population_size"],
            mutation_rate=config["mutation_rate"],
        )

        winning_roadmap = optimizer.solve(topic_dicts, data.days, data.velocity)

        return {
            "status": "Success",
            "roadmap": winning_roadmap,
            "metadata": {
                "generated_at": "2026-02-19",
                "cycle_count": len(winning_roadmap),
                "arm_index": arm_index,
                "population_size": config["population_size"],
                "mutation_rate": config["mutation_rate"],
            },
        }
    except Exception as e:
        print(f"GA Error: {e}")
        raise HTTPException(
            status_code=500, detail="The AI failed to evolve your schedule."
        )


@app.post("/api/v1/feedback")
async def submit_feedback(data: FeedbackRequest):
    if data.arm_index < 0 or data.arm_index >= len(BANDIT_ARMS):
        raise HTTPException(status_code=400, detail="Invalid arm_index.")

    try:
        scheduler_bandit.update(data.arm_index, data.reward)
        return {"status": "Feedback accepted"}
    except Exception as e:
        print(f"Feedback Error: {e}")
        raise HTTPException(status_code=500, detail="Could not apply feedback.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
