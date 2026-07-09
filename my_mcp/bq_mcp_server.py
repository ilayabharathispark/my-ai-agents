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


@mcp.tool
def get_employee_salary(employee_id: int) -> str:
    """
    Returns only the salary details for a specific employee.

    Args:
        employee_id: Employee ID (INT64).
    """
    try:
        print(f"Retrieving salary for Employee ID: {employee_id}", file=sys.stderr)
        client = get_bq_client()
        query = f"""
        SELECT name, salary
        FROM `{FULL_TABLE_REF}`
        WHERE employee_id = @employee_id
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("employee_id", "INT64", employee_id)
            ]
        )
        query_job = client.query(query, job_config=job_config)
        rows = list(query_job.result())

        if not rows:
            return f"No employee found matching ID: {employee_id}."

        row = rows[0]
        return f"Name        : {row.name}\nSalary      : ${row.salary:,.2f}"

    except Exception:
        return traceback.format_exc()


@mcp.tool
def get_employee_details(employee_id: int) -> str:
    """
    Returns profile details (id, name, department, hire date, salary) for a specific employee.

    Args:
        employee_id: Employee ID (INT64).
    """
    try:
        print(f"Retrieving details for Employee ID: {employee_id}", file=sys.stderr)
        client = get_bq_client()
        query = f"""
        SELECT
            employee_id,
            name,
            department,
            hire_date,
            salary
        FROM `{FULL_TABLE_REF}`
        WHERE employee_id = @employee_id
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("employee_id", "INT64", employee_id)
            ]
        )
        query_job = client.query(query, job_config=job_config)
        rows = list(query_job.result())

        if not rows:
            return f"No employee found matching ID: {employee_id}."

        row = rows[0]
        return f"""
Employee ID : {row.employee_id}
Name        : {row.name}
Department  : {row.department}
Hire Date   : {row.hire_date}
Salary      : ${row.salary:,.2f}
"""

    except Exception:
        return traceback.format_exc()


@mcp.tool
def get_department_average_salary(department_name: str = None) -> str:
    """
    Returns average salary of a specific department or all departments if not specified.

    Args:
        department_name: Optional department name.
    """
    try:
        print(f"Calculating average salary for department: {department_name}", file=sys.stderr)
        client = get_bq_client()
        if department_name:
            query = f"""
            SELECT department, AVG(salary) AS avg_salary, COUNT(*) AS employee_count
            FROM `{FULL_TABLE_REF}`
            WHERE LOWER(department) LIKE @dept_pattern
            GROUP BY department
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("dept_pattern", "STRING", f"%{department_name.lower()}%")
                ]
            )
        else:
            query = f"""
            SELECT department, AVG(salary) AS avg_salary, COUNT(*) AS employee_count
            FROM `{FULL_TABLE_REF}`
            GROUP BY department
            ORDER BY avg_salary DESC
            """
            job_config = None

        query_job = client.query(query, job_config=job_config)
        rows = list(query_job.result())

        if not rows:
            return "No department matching filters found."

        output = []
        for row in rows:
            output.append(
                f"Department  : {row.department}\n"
                f"Avg Salary  : ${row.avg_salary:,.2f}\n"
                f"Total Staff : {row.employee_count}"
            )
        return "\n----------------------\n".join(output)

    except Exception:
        return traceback.format_exc()


@mcp.tool
def get_top_paid_employees(limit: int = 5) -> str:
    """
    Returns the top paid employees up to the specified limit.

    Args:
        limit: Maximum number of employees to return. Default is 5.
    """
    try:
        print(f"Retrieving top {limit} paid employees", file=sys.stderr)
        client = get_bq_client()
        query = f"""
        SELECT employee_id, name, department, salary
        FROM `{FULL_TABLE_REF}`
        ORDER BY salary DESC
        LIMIT @limit
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("limit", "INT64", limit)
            ]
        )
        query_job = client.query(query, job_config=job_config)
        rows = list(query_job.result())

        if not rows:
            return "No employee records found."

        output = []
        for row in rows:
            output.append(
                f"ID: {row.employee_id} | Name: {row.name} | Department: {row.department} | "
                f"Salary: ${row.salary:,.2f}"
            )
        return "\n".join(output)

    except Exception:
        return traceback.format_exc()


if __name__ == "__main__":
    mcp.run()