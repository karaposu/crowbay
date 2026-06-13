# filepath: src/schemas/task.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

# Filter schemas type the MVP subset of devdocs/filter_design.md while
# allowing unknown keys (extra="allow") so the full structure round-trips:
# filters arrive -> persist verbatim -> return unchanged.


class AgeRange(BaseModel):
    model_config = ConfigDict(extra="allow")
    min: int | None = Field(default=None, ge=0, le=130)
    max: int | None = Field(default=None, ge=0, le=130)


class LocationEntry(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str | None = None
    exceptions: dict | None = None


class LocationFilter(BaseModel):
    model_config = ConfigDict(extra="allow")
    raw_statement: str | None = None
    regions: list[LocationEntry] | None = None
    countries: list[LocationEntry] | None = None
    cities: list[LocationEntry] | None = None


class BasicFilters(BaseModel):
    model_config = ConfigDict(extra="allow")
    location_filter: LocationFilter | None = None
    age_range: AgeRange | None = None
    gender: str | None = None


class TaskFilters(BaseModel):
    model_config = ConfigDict(extra="allow")
    basic_filters: BasicFilters | None = None
    advanced_filters: dict | None = None


class TaskCreate(BaseModel):
    desc: str = Field(min_length=1, max_length=5000)
    total_budget: float = Field(gt=0)
    you_earn: float = Field(default=0.0, ge=0, description="Per-Jumper pay")
    num_jumpers: int = Field(default=1, ge=1, le=10_000)
    category: str | None = Field(default=None, max_length=50)
    accept_jumpers_manually: bool = False
    launcher_review: bool = False
    filters: TaskFilters | None = None
    operation_requirements: list[str] | None = None
    other_requirements: list[str] | None = None
    partition_deadline: datetime | None = None
    submission_deadline: datetime | None = None

    @model_validator(mode="after")
    def _budget_covers_payouts(self) -> "TaskCreate":
        if self.you_earn * self.num_jumpers > self.total_budget:
            raise ValueError("total_budget must cover you_earn x num_jumpers")
        return self


class AudiencePreviewRequest(BaseModel):
    filters: TaskFilters | None = None


class AudiencePreviewResponse(BaseModel):
    eligible_count: int | None  # None when below the privacy floor
    display: str  # "23" or "fewer than 10"
    warnings: list[str] = []


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    desc: str
    total_budget: float
    you_earn: float
    num_jumpers: int
    status: str
    category: str | None
    accept_jumpers_manually: bool
    launcher_review: bool
    filters: dict | None
    operation_requirements: list[str] | None
    other_requirements: list[str] | None
    creation_date: datetime
    partition_deadline: datetime | None
    submission_deadline: datetime | None


class JumpRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    jumper_id: int
    status: str
    created_at: datetime
    approved_at: datetime | None
    submitted_at: datetime | None
    resolved_at: datetime | None


class ParticipationRead(BaseModel):
    jump: JumpRead
    task: TaskRead
