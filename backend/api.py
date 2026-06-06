from fastapi import FastAPI
from pydantic import BaseModel, Field

from BatMath.backend.Controller_Layer.StatcastControllerLayer import (
    add_data,
    calculate_dxba,
    clear_data,
)
from BatMath.backend.Models.DxBA import DxBARequest


app = FastAPI(title="BatMath API")


class HealthResponse(BaseModel):
    status: str


class DxBACalculateRequest(BaseModel):
    launch_angle: float
    exit_velocity: float
    spray_angle: float
    angle_forgiveness: float = Field(default=2)
    velocity_forgiveness: float = Field(default=2)
    launch_forgiveness: float = Field(default=2)


class DxBACalculateResponse(BaseModel):
    batting_average: float
    slugging: float
    samples: int


class DataOperationResponse(BaseModel):
    success: bool
    message: str
    rows_affected: int


@app.get("/api/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok")


@app.post("/api/dxba/calculate", response_model=DxBACalculateResponse)
def calculate_dxba_endpoint(request: DxBACalculateRequest):
    result = calculate_dxba(
        DxBARequest(
            launch_angle=request.launch_angle,
            exit_velocity=request.exit_velocity,
            spray_angle=request.spray_angle,
            angle_forgiveness=request.angle_forgiveness,
            velocity_forgiveness=request.velocity_forgiveness,
            launch_forgiveness=request.launch_forgiveness,
        )
    )

    return DxBACalculateResponse(
        batting_average=result.batting_average,
        slugging=result.slugging,
        samples=result.samples,
    )


@app.post("/api/data/reset", response_model=DataOperationResponse)
def reset_data_endpoint():
    result = clear_data()
    return DataOperationResponse(
        success=result.success,
        message=result.message,
        rows_affected=result.rows_affected,
    )


@app.post("/api/data/import", response_model=DataOperationResponse)
def import_data_endpoint():
    result = add_data()
    return DataOperationResponse(
        success=result.success,
        message=result.message,
        rows_affected=result.rows_affected,
    )
