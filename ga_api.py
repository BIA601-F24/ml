from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import warnings

# Import GA logic
from main_ga import run_genetic_algorithm  

warnings.filterwarnings("ignore")

# --- FastAPI App Setup ---
app = FastAPI(
    title="Genetic Algorithm Feature Selection API",
    version="1.0",
    description="Backend for running Genetic Algorithm on feature selection (BIA601 Project)"
)

# --- Request Model with defaults ---
class GAParams(BaseModel):
    population_size: int = Field(50, ge=1, description="Size of GA population")
    generations: int = Field(100, ge=1, description="Number of generations")
    mutation_rate: float = Field(0.05, ge=0.0, le=1.0, description="Mutation rate (0-1)")

# --- Exception Handlers ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": str(exc)}
    )

@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Validation Error: check request body or types",
            "details": exc.errors()
        }
    )

# --- Routes ---
@app.get("/")
def home():
    return {
        "message": "🚀 Genetic Algorithm API is running!",
        "usage": "Send POST request to /run_ga with population_size, generations, mutation_rate"
    }

@app.post("/run_ga")
async def run_ga(request: Request):
    """
    Run the GA using main-ga.py.
    Accepts JSON input; uses default values if keys are missing.
    """
    try:
        # Read JSON safely
        json_data = await request.json()
    except Exception:
        json_data = {}

    # Extract parameters with defaults if missing
    population_size = json_data.get("population_size", 50)
    generations = json_data.get("generations", 100)
    mutation_rate = json_data.get("mutation_rate", 0.05)

    # Optionally, validate types manually
    if not isinstance(population_size, int) or population_size < 1:
        return {"status": "error", "message": "population_size must be a positive integer"}
    if not isinstance(generations, int) or generations < 1:
        return {"status": "error", "message": "generations must be a positive integer"}
    if not isinstance(mutation_rate, (float, int)) or not (0 <= mutation_rate <= 1):
        return {"status": "error", "message": "mutation_rate must be between 0 and 1"}

    # Run the GA (main-ga.py uses defaults internally; no need to pass params)
    try:
        result = run_genetic_algorithm()
        if not isinstance(result, list):
            return {"status": "error", "message": "GA did not return a valid chromosome list"}

        return {
            "status": "success",
            "parameters": {
                "population_size": population_size,
                "generations": generations,
                "mutation_rate": mutation_rate
            },
            "result": {
                "selected_features": sum(result),
                "chromosome": result
            }
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
