from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


class DataSynthesizer:
    """Generate a synthetic employee dataset with SCD Type 2 history."""

    def __init__(self, rows: int = 100_000, historical_fraction: float = 0.30, seed: int = 42):
        self.rows = max(rows, 100_000)
        self.historical_fraction = max(0.0, min(historical_fraction, 1.0))
        self.seed = seed

    def generate_base_employee_data(self) -> pd.DataFrame:
        rng = np.random.default_rng(self.seed)
        fake = Faker()
        Faker.seed(self.seed)

        departments = [
            "Engineering",
            "Sales",
            "HR",
            "Finance",
            "Marketing",
            "Operations",
            "Supply Chain",
            "Customer Success",
        ]
        roles = {
            "Engineering": ["Software Engineer", "Senior Engineer", "Data Engineer", "Principal Engineer"],
            "Sales": ["Account Executive", "Sales Manager", "Business Development Rep"],
            "HR": ["HR Generalist", "HR Manager", "Talent Specialist"],
            "Finance": ["Financial Analyst", "Finance Manager", "Controller"],
            "Marketing": ["Marketing Analyst", "Brand Manager", "Growth Manager"],
            "Operations": ["Operations Analyst", "Operations Manager", "Project Coordinator"],
            "Supply Chain": ["Planner", "Logistics Manager", "Procurement Analyst"],
            "Customer Success": ["Customer Success Manager", "Support Engineer", "Account Manager"],
        }

        employee_ids = np.arange(1, self.rows + 1)
        departments_list = rng.choice(departments, size=self.rows)
        salary_base = {
            "Engineering": 95000,
            "Sales": 82000,
            "HR": 76000,
            "Finance": 86000,
            "Marketing": 78000,
            "Operations": 72000,
            "Supply Chain": 70000,
            "Customer Success": 74000,
        }

        records = []
        for idx in employee_ids:
            dept = departments_list[idx - 1]
            age = int(rng.integers(22, 62))
            base_salary = salary_base[dept] + int(rng.integers(-15000, 25000))
            performance_score = int(rng.integers(55, 99))
            tenure = int(rng.integers(0, 15))
            hire_date = pd.Timestamp.now().normalize() - pd.to_timedelta(rng.integers(180, 6200), unit="D")
            manager = int(rng.integers(1, max(2, self.rows // 50)))
            records.append(
                {
                    "employee_id": int(idx),
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "email": f"employee{idx}@example.com",
                    "department_name": dept,
                    "job_title": rng.choice(roles[dept]),
                    "age": age,
                    "salary": float(base_salary),
                    "performance_score": performance_score,
                    "years_experience": max(0, tenure),
                    "hire_date": hire_date,
                    "manager_id": manager,
                    "attrition_risk": int(rng.integers(0, 100)),
                }
            )

        df = pd.DataFrame(records)
        return df

    def generate_scd_type_2_history(self, base_df: pd.DataFrame) -> pd.DataFrame:
        historical_rows = []
        subset_size = max(1, int(len(base_df) * self.historical_fraction))
        subset = base_df.sample(n=subset_size, random_state=self.seed)

        for _, row in subset.iterrows():
            original_department = row["department_name"]
            original_title = row["job_title"]
            original_salary = row["salary"]
            current_date = pd.Timestamp.now().normalize()

            historical_rows.append(
                {
                    "employee_id": int(row["employee_id"]),
                    "department_name": original_department,
                    "job_title": original_title,
                    "salary": float(original_salary),
                    "start_date": current_date - pd.DateOffset(years=2),
                    "end_date": current_date,
                    "is_current": 0,
                    "effective_seq": 1,
                }
            )

            new_department = np.random.choice(["Engineering", "Finance", "Sales", "Operations", "HR", "Marketing"])
            new_title = f"Senior {row['job_title']}" if row["performance_score"] >= 75 else row["job_title"]
            new_salary = float(original_salary * (1.08 + np.random.random() * 0.12))

            historical_rows.append(
                {
                    "employee_id": int(row["employee_id"]),
                    "department_name": new_department,
                    "job_title": new_title,
                    "salary": new_salary,
                    "start_date": current_date,
                    "end_date": None,
                    "is_current": 1,
                    "effective_seq": 2,
                }
            )

        return pd.DataFrame(historical_rows)

    def export_to_csv(self, output_dir: str | Path | None = None) -> dict[str, Path]:
        base_dir = Path(output_dir) if output_dir else Path(__file__).resolve().parent.parent / "data"
        base_dir.mkdir(parents=True, exist_ok=True)

        employees = self.generate_base_employee_data()
        history = self.generate_scd_type_2_history(employees)

        employee_path = base_dir / "synthetic_employees.csv"
        history_path = base_dir / "employee_historical_scd2.csv"
        employees.to_csv(employee_path, index=False)
        history.to_csv(history_path, index=False)

        return {"employees": employee_path, "history": history_path}

    def print_summary(self) -> None:
        employees = self.generate_base_employee_data()
        history = self.generate_scd_type_2_history(employees)
        print(f"Generated {len(employees):,} employees")
        print(f"Generated {len(history):,} historical SCD rows")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic employee analytics data")
    parser.add_argument("--rows", type=int, default=100_000, help="Target row count for employee data")
    parser.add_argument("--historical-fraction", type=float, default=0.30, help="Fraction of employees with SCD history")
    parser.add_argument("--output-dir", type=str, default=None, help="Directory for generated CSV files")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    synthesizer = DataSynthesizer(rows=args.rows, historical_fraction=args.historical_fraction)
    files = synthesizer.export_to_csv(args.output_dir)
    print(f"Employee data saved to: {files['employees']}")
    print(f"SCD history saved to: {files['history']}")
