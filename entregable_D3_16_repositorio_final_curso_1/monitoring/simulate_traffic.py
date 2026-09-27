import argparse
import random
import time

import requests


API_URL = "http://localhost:8000/predict"

CATEGORIES = {
    "gender": ["F", "M"],
    "region": ["Lima", "Norte", "Sur", "Centro"],
    "customer_segment": ["Mass", "Premium"],
    "contract_type": ["Monthly", "Annual"],
    "internet_service": ["Fiber", "DSL"],
    "tv_service": ["Yes", "No"],
    "streaming_service": ["Yes", "No"],
    "payment_method": ["Credit Card", "Bank Transfer"],
}


def clipped_gauss(mean, std, minimum, maximum):
    value = random.gauss(mean, std)
    return max(minimum, min(maximum, value))


def build_customer(index, scenario):
    if scenario == "normal":
        monthly_fee = clipped_gauss(80, 12, 40, 120)
        support_calls = round(clipped_gauss(1.5, 1, 0, 5))
        payment_delay = round(clipped_gauss(3, 3, 0, 15))
        digital_usage = clipped_gauss(8, 1, 4, 10)
    else:
        monthly_fee = clipped_gauss(135, 15, 90, 180)
        support_calls = round(clipped_gauss(6, 2, 2, 12))
        payment_delay = round(clipped_gauss(30, 12, 5, 60))
        digital_usage = clipped_gauss(3, 1.2, 1, 7)

    tenure = random.randint(6, 60)

    return {
        "customer_id": f"SIM-{scenario.upper()}-{index:04d}",
        "age": random.randint(20, 70),
        "tenure_months": tenure,
        "monthly_fee": round(monthly_fee, 2),
        "total_spent": round(monthly_fee * tenure, 2),
        "support_calls": support_calls,
        "complaints": random.randint(0, 2),
        "last_payment_delay": payment_delay,
        "digital_usage_score": round(digital_usage, 2),
        "marketing_score": round(
            clipped_gauss(65, 15, 1, 100),
            2,
        ),
        "preferred_contact_hour": random.randint(8, 20),
        "gender": random.choice(CATEGORIES["gender"]),
        "region": random.choice(CATEGORIES["region"]),
        "customer_segment": random.choice(
            CATEGORIES["customer_segment"]
        ),
        "contract_type": random.choice(
            CATEGORIES["contract_type"]
        ),
        "internet_service": random.choice(
            CATEGORIES["internet_service"]
        ),
        "tv_service": random.choice(CATEGORIES["tv_service"]),
        "streaming_service": random.choice(
            CATEGORIES["streaming_service"]
        ),
        "payment_method": random.choice(
            CATEGORIES["payment_method"]
        ),
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--scenario",
        choices=["normal", "drift"],
        required=True,
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=50,
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.05,
    )

    args = parser.parse_args()

    random.seed(42)

    successful = 0
    probabilities = []

    for index in range(1, args.requests + 1):
        customer = build_customer(index, args.scenario)

        response = requests.post(
            API_URL,
            json=customer,
            timeout=10,
        )
        response.raise_for_status()

        prediction = response.json()
        probabilities.append(
            prediction["churn_probability"]
        )
        successful += 1

        time.sleep(args.delay)

    average_probability = (
        sum(probabilities) / len(probabilities)
    )

    print(f"Scenario: {args.scenario}")
    print(f"Successful requests: {successful}")
    print(
        "Average churn probability: "
        f"{average_probability:.4f}"
    )


if __name__ == "__main__":
    main()
