# generate_data.py
# Creates a made-up book of 70 accounts and saves it to data/accounts.csv.
# Every company and person in this file is fictional.
# Run it again any time: the "seed" below makes it produce the same data each time.

import os
import random
from datetime import date, timedelta

import pandas as pd

random.seed(42)  # same seed = same made-up data every run

# The date the data is "as of" (fixed so the data doesn't change day to day)
DATA_AS_OF = date(2026, 11, 24)

# How many accounts of each type
SEGMENT_COUNTS = {"AI Startup": 35, "Bank": 18, "Asset Manager": 17}

# Building blocks for fictional company names
NAME_PARTS = {
    "AI Startup": (
        ["Neural", "Vector", "Cortex", "Lumen", "Quanta", "Synth", "Helix", "Tensor",
         "Arc", "Nova", "Prism", "Echo", "Signal", "Latent", "Pixel", "Cipher"],
        ["Labs", "AI", "Systems", "Works", "Dynamics", "Intelligence", "Robotics", "Logic"],
    ),
    "Bank": (
        ["Harborstone", "Ridgeway", "Northgate", "Silverbrook", "Ironbridge", "Kestrel",
         "Oakmont", "Bayfield", "Crescent", "Westmarch", "Clearwater", "Stonehaven"],
        ["Bank", "Bancorp", "Financial", "Savings Bank", "Trust"],
    ),
    "Asset Manager": (
        ["Granite Peak", "Bluefin", "Summit Ridge", "Larchmont", "Evergreen", "Cobalt",
         "Meridian", "Highline", "Fairhaven", "Tidewater", "Aspen Rock", "Northstar"],
        ["Capital", "Asset Management", "Investors", "Partners", "Advisors"],
    ),
}

FIRST_NAMES = ["Maya", "Daniel", "Priya", "Jonas", "Elena", "Marcus", "Aisha", "Tom",
               "Sofia", "Kenji", "Rachel", "Omar", "Laura", "Victor", "Nina", "Sam"]
LAST_NAMES = ["Chen", "Okafor", "Patel", "Lindqvist", "Garcia", "Brennan", "Haddad",
              "Novak", "Rossi", "Tanaka", "Weiss", "Morales", "Fischer", "Kim", "Shah"]
SPONSOR_TITLES = {
    "AI Startup": ["CTO", "VP Engineering", "Head of AI", "CEO"],
    "Bank": ["Chief Data Officer", "CIO", "Head of AI Strategy", "COO"],
    "Asset Manager": ["Chief Investment Officer", "CTO", "Head of Research", "COO"],
}

# Short CSM notes, by how the account is really doing
NOTES = {
    "healthy": [
        "Expanding into a second team; asked about higher usage tiers.",
        "Sponsor shared a strong internal ROI story at the last QBR.",
        "Steady adoption, no open issues. Good candidate for a case study.",
        "Champion is pushing for an enterprise-wide rollout next year.",
    ],
    "watch": [
        "Adoption has flattened after the initial rollout.",
        "New procurement lead is reviewing all AI vendor spend.",
        "Usage is steady but concentrated in one team.",
        "Champion is engaged, but the sponsor hasn't joined a call in months.",
    ],
    "at_risk": [
        "Executive sponsor left; no replacement identified yet.",
        "Repeated latency complaints; escalated twice this quarter.",
        "Evaluating a competitor in a parallel pilot.",
        "Budget freeze announced; renewal under review.",
    ],
}


def make_company_name(segment, used_names):
    """Combine two name parts until we get a name not used yet."""
    first_parts, second_parts = NAME_PARTS[segment]
    while True:
        name = f"{random.choice(first_parts)} {random.choice(second_parts)}"
        if name not in used_names:
            used_names.add(name)
            return name


def pick_contract_type(segment):
    """AI startups lean toward usage contracts; financial firms lean toward seats."""
    if segment == "AI Startup":
        return random.choices(["Usage", "Mixed", "Seat"], weights=[50, 35, 15])[0]
    return random.choices(["Seat", "Mixed", "Usage"], weights=[50, 35, 15])[0]


def pick_arr(segment):
    """Annual contract value in US dollars, rounded to the nearest $5,000."""
    low, high = {"AI Startup": (50_000, 600_000),
                 "Bank": (300_000, 2_500_000),
                 "Asset Manager": (150_000, 1_500_000)}[segment]
    return round(random.uniform(low, high) / 5_000) * 5_000


def make_account(account_number, segment, used_names):
    """Build one made-up account. Its hidden health decides how its signals look."""
    # Hidden "true" health: about half healthy, 30% watch, 20% at risk
    health = random.choices(["healthy", "watch", "at_risk"], weights=[50, 30, 20])[0]

    contract_type = pick_contract_type(segment)
    arr = pick_arr(segment)

    # Seat signals (only for Seat and Mixed contracts)
    seats_purchased = None
    seats_active = None
    if contract_type in ("Seat", "Mixed"):
        seats_purchased = random.randint(50, 400) if segment == "AI Startup" else random.randint(200, 3000)
        use_rate = {"healthy": (0.75, 1.0), "watch": (0.5, 0.8), "at_risk": (0.2, 0.55)}[health]
        seats_active = int(seats_purchased * random.uniform(*use_rate))

    # Usage signals (only for Usage and Mixed contracts)
    usage_vs_commit_pct = None   # actual usage as % of what they committed to
    usage_trend_90d_pct = None   # change in usage over the last 90 days
    if contract_type in ("Usage", "Mixed"):
        usage_vs_commit_pct = round(random.uniform(*{
            "healthy": (90, 135), "watch": (65, 95), "at_risk": (25, 65)}[health]))
        usage_trend_90d_pct = round(random.uniform(*{
            "healthy": (5, 45), "watch": (-12, 8), "at_risk": (-55, -12)}[health]))

    # Support signals (last 90 days)
    open_tickets = random.randint(*{"healthy": (0, 3), "watch": (1, 6), "at_risk": (4, 14)}[health])
    sev1_tickets = random.randint(*{"healthy": (0, 0), "watch": (0, 1), "at_risk": (1, 4)}[health])

    # Relationship signals
    sponsor_status = random.choices(
        ["Engaged", "Quiet", "Left company"],
        weights={"healthy": [85, 15, 0], "watch": [40, 55, 5], "at_risk": [15, 45, 40]}[health])[0]
    survey_score = random.randint(*{"healthy": (8, 10), "watch": (6, 8), "at_risk": (2, 6)}[health])
    days_since_qbr = random.randint(*{"healthy": (10, 80), "watch": (60, 150), "at_risk": (100, 240)}[health])

    # Dates
    renewal_date = DATA_AS_OF + timedelta(days=random.randint(7, 365))
    contract_start = renewal_date - timedelta(days=365 * random.randint(1, 3))

    return {
        "account_id": f"ACC-{account_number:03d}",
        "account_name": make_company_name(segment, used_names),
        "segment": segment,
        "contract_type": contract_type,
        "arr_usd": arr,
        "contract_start": contract_start,
        "renewal_date": renewal_date,
        "seats_purchased": seats_purchased,
        "seats_active": seats_active,
        "usage_vs_commit_pct": usage_vs_commit_pct,
        "usage_trend_90d_pct": usage_trend_90d_pct,
        "open_tickets": open_tickets,
        "sev1_tickets_90d": sev1_tickets,
        "exec_sponsor": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "exec_sponsor_title": random.choice(SPONSOR_TITLES[segment]),
        "sponsor_status": sponsor_status,
        "last_survey_score": survey_score,
        "last_qbr_date": DATA_AS_OF - timedelta(days=days_since_qbr),
        "csm_note": random.choice(NOTES[health]),
    }


# Build all accounts, then shuffle so segments are mixed together
segments = [seg for seg, count in SEGMENT_COUNTS.items() for _ in range(count)]
random.shuffle(segments)
used_names = set()
accounts = [make_account(i + 1, seg, used_names) for i, seg in enumerate(segments)]

# Turn the list into a table and save it
table = pd.DataFrame(accounts)
table["seats_purchased"] = table["seats_purchased"].astype("Int64")  # whole numbers, blanks allowed
table["seats_active"] = table["seats_active"].astype("Int64")
table["usage_vs_commit_pct"] = table["usage_vs_commit_pct"].astype("Int64")
table["usage_trend_90d_pct"] = table["usage_trend_90d_pct"].astype("Int64")

os.makedirs("data", exist_ok=True)
table.to_csv("data/accounts.csv", index=False)
print(f"Saved {len(table)} fictional accounts to data/accounts.csv (data as of {DATA_AS_OF})")
