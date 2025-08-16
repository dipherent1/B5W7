from dagster import Definitions
from .jobs import pipeline_job

defs = Definitions(
    jobs=[pipeline_job],
)
