import re
import pandas as pd
from typing import List
from openpyxl import load_workbook
from openpyxl.comments import Comment
from openpyxl.styles import Color, PatternFill, Font, Border


# sample_row = pd.read_csv("sample_100_rows.csv", usecols=['orderingcustomerdetails'])
# sample_row = pd.read_csv("data_mt103.csv", usecols=['orderingcustomerdetails', 'orderingcustomername'])
sample_row = pd.read_csv("sample_100_rows.csv", usecols=['orderingcustomerdetails', 'orderingcustomername','remittanceinformation'])


# Patterns
PATTERNS = {
    "descriptive": r'\b(Innovation|Limit|INDUSTRIAL|Creative|Supply|Digital|Future|Sustainable|Smart|Global|Advanced|Modern|Intelligent|Efficient|Reliable|Secure|Fast|Flexible|Dynamic|Agile|Strategic|Expert|Professional|Quality|Excellence|Prime|Elite|Superior|Premium|Unique|Vision|Insight|Focus|Nexus|Vertex|Synergy)\b',
    "sector": r'\b(Tech|IT|Software|Finance|Bank|Capital|Health|Med|Care|Pharma|Energy|Power|Green|Bio|Engineering|Construction|Manufacturing|Logistics|Shipping|Consulting|Marketing|Advertising|Media|Entertainment|Retail|E\-commerce|Food|Beverage|Hospitality|Tourism|Travel|Real\ Estate|Property|Investment|Insurance|Telecom|Communications)\b',
    "nordic": r'\b(Fjord|Viking|Aurora|Northern|Arctic|Midnight|Borealis|Nordic|Saga|Ice|Glacier|Winter|Forest|Wilderness|Fjell|Skog|Suomi)\b',
    "financial": r'\b(Bank | Trust | Credit\ Union | Savings | Insurance | Investment | Capital | Investments | PAYPAL | MASTERCARD)\b',
    "business_core": r'\b(LLC|ORG|LIMITED|BV|A\S|LTD|B\.V|Inc\.|INC\.|A\.S|INC|Corp\.|Ltd\.|AG|GmbH|S\.A\.|Pty\ Ltd\.|S\.p\.A\.|B\.V\.|N\.V\.|Co\.|LP|LLP|PC|SARL|SNC|Ltd\.\ Sti\.|Kft\.|Zrt\.|P\.L\.C\.|PLLC|CIC|SpA|Ltda\.|Lda\.|Bhd|AS|AB|ApS|Oy|Oyj|a\.s\.|s\.r\.o\.|d\.o\.o\.|a\.d\.|OU|SIA|UAB|Sarl|SARL|GmbH|PLC|CC|NV|SCA|EEIG|ULC|SAOC|WLL|KSC|PrJSC|PISC|JSC|Ltda|SP|NPO)\b',
    "business_aux1": r'\b(Solutions|Systems|Technologies|Resources|Management|Development|Innovations|Network|Operations|Strategy|Growth|Success|Leaders|Specialists|Experts|Advisors|Consultants|Partners|Associates|Team|Agency|Company|Firm|Business|Enterprise|Organization|Corporation)\b',
    "business_aux2": r'\b(Group|Holding|Consulting|Services|Solutions|Partners|Enterprises|Corporation|International|Ventures|Holdings|Ltd|Inc|PIc|LLC|LLP|AB|AS|Oy|Aps|hf)\b'
}


INDIVIDUAL_PATTERNS = [
    r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b',  # e.g., John Smith
    r'\b[A-Z][a-z]*\s[A-Z]\.\s?[A-Z][a-z]+\b',  # e.g., John M. Smith
    r'\b(Mr|Mrs|Ms|Dr|Prof|Sir)\.\s?[A-Z][a-z]+\s[A-Z][a-z]+\b',  # e.g., Dr. Jane Doe
    r'\b[A-Z][a-z]+\s[A-Z][a-z]+-[A-Z][a-z]+\b',  # e.g., Mary-Jane Watson
    r'\b[A-Z][a-z]+\s(?:Al|Bin|Ibn)\s[A-Z][a-z]+\b',  # e.g., Osama Bin Laden
    r'\b[A-Z][a-z]+\b',  # Single names (possible but less reliable, e.g., "Cher")
]


def identify_entity(text: str, pattern: str) -> str:
    if re.search(pattern, text, re.IGNORECASE):
        return "Yes"
    return "No"


def identify_individual(name: str) -> str:
    for pattern in INDIVIDUAL_PATTERNS:
        if re.search(pattern, name):
            return "Individual"
    return "No"


def extract_entity_name(text: str, pattern: str) -> str:
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return "Business Entity"
        # return match.group(0)
    return "Potential Individual/Financial Entity"


def get_full_entity(text:str, pattern:str) -> str:
    business_patterns = re.compile(pattern, re.IGNORECASE | re.UNICODE)
    removed_characters = text.splitlines(keepends=False)
    list_of_items = " ".join(removed_characters[1:2]) if len(removed_characters) > 1 else (removed_characters[0])
    return list_of_items if list_of_items != "" else ""


def save_to_excel(processed_data):
    with pd.ExcelWriter('output_sample.xlsx') as writer:
        processed_data.to_excel(writer, index=False)


def classify_all(data:pd.DataFrame):

    sample_row.loc[
        (sample_row["is_business_core"] == "No") & (sample_row["is_financial"] == "No"),
        "Classification"
    ] = "Individual/Non-Individual"

    sample_row.loc[
        sample_row["is_financial"] == "Yes",
        "Classification"
    ] = "FIN"

    sample_row.loc[
        ~sample_row["Classification"].isin(["FIN", "Individual/Non-Individual"]),
        "Classification"
    ] = "Business Entity"


for key, pattern in PATTERNS.items():
    sample_row[f'is_{key}'] = sample_row["orderingcustomerdetails"].apply(lambda x: identify_entity(x, pattern))


if __name__ == "__main__":

    # Applying patterns to dataframe

    sample_row["full_entity_name"] = sample_row["orderingcustomerdetails"].apply(lambda x: get_full_entity(x, pattern))
    # sample_row["is_individual"] = sample_row["orderingcustomerdetails"].apply(identify_individual)
    # sample_row["entity_names"] = sample_row["orderingcustomerdetails"].apply(lambda x: extract_entity_name(x, PATTERNS['business_core']))
    classify_all(sample_row)
    save_to_excel(sample_row)
