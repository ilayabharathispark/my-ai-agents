import os
import sys
import traceback

from google.cloud import bigquery
from google.oauth2 import service_account
from fastmcp import FastMCP

# ===========================
# FastMCP Server
# ===========================
mcp = FastMCP("bq-salary-server")

# ===========================
# Configuration
# ===========================
PROJECT_ID = "ilaya-bharathi-murugan"
DATASET_ID = "bharathi"
TABLE_ID = "employee"

FULL_TABLE_REF = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

# Path to Service Account JSON
SERVICE_ACCOUNT_FILE = r"C:\\Users\\ILAYA BHARATHI M\\Downloads\\ilaya-bharathi-murugan-e7fa05858bec.json"

# ===========================
# BigQuery Client
# ===========================
def get_bq_client():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE
        )

        client = bigquery.Client(
            project=PROJECT_ID,
            credentials=credentials
        )

        return client

    except Exception:
        print(traceback.format_exc(), file=sys.stderr)
        raise


# ===========================
# MCP Tool
# ===========================
@mcp.tool
def get_employee_salary_details(employee_name: str) -> str:
    """
    Returns salary details for an employee.

    Args:
        employee_name: Employee name.
    """

    try:
        print(f"Searching employee: {employee_name}", file=sys.stderr)

        client = get_bq_client()

        query = f"""
        SELECT
            employee_id,
            name,
            department,
            hire_date,
            salary
        FROM `{FULL_TABLE_REF}`
        WHERE LOWER(name) LIKE @name_pattern
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    "name_pattern",
                    "STRING",
                    f"%{employee_name.lower()}%"
                )
            ]
        )

        query_job = client.query(query, job_config=job_config)

        rows = list(query_job.result())

        if not rows:
            return f"No employee found matching '{employee_name}'."

        output = []

        for row in rows:
            output.append(
                f"""
Employee ID : {row.employee_id}
Name        : {row.name}
Department  : {row.department}
Hire Date   : {row.hire_date}
Salary      : ${row.salary:,.2f}
"""
            )

        return "\n----------------------\n".join(output)

    except Exception:
        return traceback.format_exc()


if __name__ == "__main__":
    mcp.run()