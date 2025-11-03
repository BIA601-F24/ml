from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import warnings

from main_ga import run_genetic_algorithm

warnings.filterwarnings("ignore")

app = FastAPI(
    title="Genetic Algorithm Feature Selection API",
    version="1.0",
    description="Backend for running GA on feature selection (BIA601 Project)"
)

class GAParams(BaseModel):
    population_size: int = Field(50, ge=1)
    generations: int = Field(50, ge=1)
    mutation_rate: float = Field(0.1, ge=0.0, le=1.0)


@app.get("/")
def home():
    return {
        "message": "🚀 Genetic Algorithm API is running!",
        "usage": "Send POST request to /run_ga with population_size, generations, mutation_rate"
    }


@app.post("/run_ga")
async def run_ga(params: GAParams):
    try:
        result = run_genetic_algorithm(
            population_size=params.population_size,
            num_generations=params.generations,
            mutation_rate=params.mutation_rate
        )

        return {
            "status": "success",
            "parameters": {
                "population_size": params.population_size,
                "generations": params.generations,
                "mutation_rate": params.mutation_rate
            },
            "result": {
                "chromosome": result["chromosome"],
                "selected_count": result["selected_count"],
                "selected_features": result["selected_features"],
                "best_fitness": result["best_fitness"]
            }
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
