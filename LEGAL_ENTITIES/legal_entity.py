### Function to apply to column ### 
import re
import pandas as pd



import pandas as pd
import re




business_suffixes = [
    "LLC", "Inc.", "Corp.", "Ltd.", "AG", "GmbH", "S.A.", "Pty Ltd.", "S.p.A.", "B.V.", "N.V.", "Co.",
    "LP", "LLP", "PC", "SARL", "SNC", "Ltd. Şti.", "Ltd. Sti.", "Kft.", "Zrt.", "P.L.C.", "PLLC", "CIC",
    "SpA", "Ltda.", "Lda.", "Bhd", "AS", "AB", "ApS", "Oy", "Oyj", "a.s.", "s.r.o.", "d.o.o.", "a.d.",
    "OÜ", "SIA", "UAB", "Sarl", "SARL", "GmbH", "PLC", "CC", "NV", "SCA", "EEIG", "ULC", "SAOC", "WLL",
    "KSC", "PrJSC", "PJSC", "JSC", "Ltda", "SP", "NPO",
    "A/S", "S.A.S.", "S.R.L.", "S.A.C.", "EURL", "S.R.L.", "S.L.", "S.A.", "K.K.", "S.R.L.", "S.A.S.",
    "S.A.", "G.K.", "K.K.", "S.A.C.V.", "S.A.", "OÜ", "S.A.S.", "S.A.", "Ltda.", "S.A.", "S.A."
]

# Escape special regex characters in suffixes and join them into a pattern
escaped_suffixes = [re.escape(suffix) for suffix in business_suffixes]
pattern = r'\b(?:' + '|'.join(escaped_suffixes) + r')\b'

print(pattern)




def classify_entity(suffix):
    # Define regular expressions for business and financial entities
    business_pattern = re.compile(r'\b(?:Limited Partnership|Limited Liability Partnership|LLP|LLC|Ltd|Ltd\.|LTDA\.|S\.R\.L|S\.A\.|S\.A\.S|N\.V|B\.V|BVBA|S\.C\.A|S\.E|Corporation|Corp\.|Inc|Incorporated|A\.G|AG|GmbH|Co-op|Co-operative|Association|ASBL|Société|Coop|SPRL|VZW|Société à Responsabilité Limitée|Société en Commandite)\b', re.IGNORECASE)

    financial_pattern = re.compile(r'\b(?:Trust Co\.|Trust Company|Trust Corp\.|Trust Corporation|Trustee Company|Fund\.|FONDPRIV|GIE|GEIE|Bank|Loan|Investment|Financial|Asset|Société de Fiducie|Compagnie de Fiducie|Société de Prêt)\b', re.IGNORECASE)

    # Check which pattern matches
    if business_pattern.search(suffix):
        return 'Business Entity'
    elif financial_pattern.search(suffix):
        return 'Financial Institution'
    else:
        return 'Unknown'

# Sample DataFrame
data = {
    'suffixes': ['Ltd', 'LLC', 'N.V.', 'S.A.S', 'Trust Co.', 'Fund.', 'FONDPRIV', 'Bank', 'SPRL', 'GmbH']
}

df = pd.DataFrame(data)

# Apply the classification function to the 'suffixes' column
df['entity_type'] = df['suffixes'].apply(classify_entity)

# Display the DataFrame
print(df)







# Define the function to determine if a substring is an individual
def is_individual(name):
    # Common patterns to identify individuals
    individual_patterns = [
        r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b',  # e.g., John Smith
        r'\b[A-Z][a-z]*\s[A-Z]\.\s?[A-Z][a-z]+\b',  # e.g., John M. Smith
        r'\b(Mr|Mrs|Ms|Dr|Prof|Sir)\.\s?[A-Z][a-z]+\s[A-Z][a-z]+\b',  # e.g., Dr. Jane Doe
        r'\b[A-Z][a-z]+\s[A-Z][a-z]+-[A-Z][a-z]+\b',  # e.g., Mary-Jane Watson
        r'\b[A-Z][a-z]+\s(?:Al|Bin|Ibn)\s[A-Z][a-z]+\b',  # e.g., Osama Bin Laden
        r'\b[A-Z][a-z]+\b',  # Single names (possible but less reliable, e.g., "Cher")
    ]
    
    # Common patterns to identify business entities
    business_suffixes = [
        "LLC", "Inc.", "Corp.", "Ltd.", "AG", "GmbH", "S.A.", "Pty Ltd.", "S.p.A.", "B.V.", "N.V.", "Co.",
        "LP", "LLP", "PC", "SARL", "SNC", "Ltd. Şti.", "Ltd. Sti.", "Kft.", "Zrt.", "P.L.C.", "PLLC", "CIC",
        "SpA", "Ltda.", "Lda.", "Bhd", "AS", "AB", "ApS", "Oy", "Oyj", "a.s.", "s.r.o.", "d.o.o.", "a.d.",
        "OÜ", "SIA", "UAB", "Sarl", "SARL", "GmbH", "PLC", "CC", "NV", "SCA", "EEIG", "ULC", "SAOC", "WLL",
        "KSC", "PrJSC", "PJSC", "JSC", "Ltda", "SP", "NPO"
    ]

    # Check if the name matches any individual patterns
    for pattern in individual_patterns:
        if re.search(pattern, name):
            return True  # Likely an individual

    # Check if the name contains any business suffixes
    for suffix in business_suffixes:
        if suffix in name:
            return False  # Likely a business entity

    # Default to individual if no business suffix is found
    return True















def match_patterns(df, column, patterns):
    """
    This function matches a list of patterns against a DataFrame column.
    
    :param df: pandas DataFrame containing the data
    :param column: the name of the column to search for patterns
    :param patterns: list of regex patterns to search for
    :return: DataFrame with an additional column indicating if any pattern matched
    """
    # Combine all patterns into a single regular expression
    combined_pattern = '|'.join(f'({pattern})' for pattern in patterns)
    
    # Apply the pattern to the specified column and create a new column 'match'
    df['match'] = df[column].apply(lambda x: bool(re.search(combined_pattern, str(x))))
    
    return df

# Example DataFrame
df = pd.DataFrame({
    'company_name': [
        '(Guarantee) Ltd.',  # should match
        'Some Other Name',   # should not match
        '(유)',              # should match
        'Random Co.',        # should not match
        '(SPV) Ltd',         # should match
        'Sample (A)',        # should match
        'Not Applicable',    # should not match
        'Check (Guarantee) Ltd.'  # should match
    ]
})

# Patterns to search for
patterns = [
    r'\(Guarantee\) Ltd\.',  # exact match for "(Guarantee) Ltd."
    r'\(SPV\) Ltd',          # exact match for "(SPV) Ltd"
    r'\(유\)',                # exact match for "(유)"
    r'A'                     # match any occurrence of "A"
]

# Apply the pattern matching function
df = match_patterns(df, 'company_name', patterns)

# Print the DataFrame with the 'match' column
print(df)







# Pattern for business Entities
patterns = [
    r'\(Guarantee\) Ltd\.',
    r'\(SPV\) Ltd',
    r'\(SPV\) SPC',
    r'\(유\)',
    r'\(주\)',
    r'A',
    r'A Limited Partnership;An Incorporated Limited\rPartnership;LP;LP.;Lp.;Lp;I.L.P;ILP',
    r'A\. C\.',
    r'A\.C\.',
    r'A\.E\.I\.E\.',
    r'A\.F\.',
    r'A\.G\.',
    r'A\.I\.E\.',
    r'A/S',
    r'AA',
    r'AB',
    r'ABV',
    r'AEIE',
    r'AF',
    r'AG',
    r'AGes\.',
    r'AGmsZ',
    r'AISBL',
    r'AM',
    r'AMBA',
    r'ANS',
    r'APB',
    r'AS',
    r'ASA',
    r'ASBL',
    r'ASBL DPU',
    r'ASC',
    r'ASSEP',
    r'AVV;avv;A\.V\.V\.;a\.v\.v\.',
    r'Akc\. spol\.',
    r'Ambasciate',
    r'Ambassade',
    r'ApS',
    r'Assoc\.',
    r'Aus\. Unt\.',
    r'Ausl\. AG & LTD',
    r'Ausl\. Gen\. & GMBH',
    r'Ausl\. Rechtsform',
    r'AÜ',
    r'B\.T\.;BT',
    r'BA',
    r'BAB',
    r'BBL',
    r'BI',
    r'BN',
    r'BO',
    r'BR',
    r'BRF',
    r'BRL',
    r'BV',
    r'BV BVBA',
    r'BV CVA',
    r'BV CVBA',
    r'BV CVOA',
    r'BV GCV',
    r'BV LV',
    r'BV NV',
    r'BV PR',
    r'BV VOF',
    r'BV;bv;B\.V\.;b\.v\.',
    r'BVBA',
    r'BVBA SO',
    r'Banka - a\. s\.',
    r'Banka-štát\.peňaž\.ústav',
    r'BenCom',
    r'Botschaft',
    r'Branch RC',
    r'Bt\.',
    r'Bund',
    r'C\.E\.R\.',
    r'C\.R\.A\.',
    r'C/A',
    r'CB',
    r'CC',
    r'CCC;C\.C\.C\.',
    r'CCSDA',
    r'CEMIX',
    r'CIA LTDA',
    r'CIC',
    r'CLF',
    r'CLG',
    r'CNCOL',
    r'COOP',
    r'CORPORATION;COMPANY;LIMITED;CORP;INC;CO;LTD',
    r'CRC',
    r'CSL',
    r'CV',
    r'CV PR',
    r'CV;cv;C\.V\.;c\.v\.',
    r'CVA SO',
    r'CVBA',
    r'CVBA PR',
    r'CVBA SO',
    r'CVOA',
    r'CVOA CD',
    r'CVOA SO',
    r'Cant\. publ\. co\.',
    r'Canton',
    r'Cantonal administration',
    r'Cantone',
    r'Co-op',
    r'Co-op;C\.A\.',
    r'Co-op;Coop;Assoc\.;Assoc;Assn\.;Assn',
    r'Co-operative Limited;Cooperative Limited;Co-op Limited;Coop Limited;Co-\roperative Ltd\.;Cooperative Ltd\.;Co-opLtd\.;Coop Ltd\.;Co-\roperative;Cooperative;Co-op;Coop',
    r'Co-operative Ltd;Coopérative Ltée',
    r'Co-operative and Limited;Ltd\.;Co-opérative and Limitée;Ltée',
    r'Co-operative;Coopérative',
    r'Co\.;corp\.;inc\.;ltd\.',
    r'Comm\.V',
    r'Comm\.VA',
    r'CommV',
    r'Commune',
    r'Community Interest Company;société d’intérêt\rcommunautaire;C\.I\.C\.;CIC;S\.I\.C\.;SIC',
    r'Company;Co\.;Corporation;Corp\.;Incorporated;Inc\. Limited;Ltd\.',
    r'Company;Co\.;Corporation;Corp\.;Incorporated;Inc\. Limited;or Ltd\. Professional\rCorporation or P\.C\. for those rendering professional services\.',
    r'Company;Corporation;Corp\.;Incorporated;Inc\.',
    r'Comune',
    r'Condominium Corporation',
    r'Confederazione',
    r'Confédération',
    r'Coop & Sarl étranger',
    r'Coop\. & SAGL estero',
    r'Cooperative Limited;Cooperative Ltd\.;Cooperative Inc\.;Cooperative\rincorporated;Co-operative Limited;Co-operative Ltd;Co-operative Inc;Co-\roperative incorporated;Coopérative limitée;Coopérative ltée;Pool Limited;Pool\rLtd\.;Pool Inc\.;Pool incorporated;Co-op Limited;Co-op limitée;Co-op\rincorporated;Co-op incorporée;Co-op Inc\.',
    r'Cooperative;co-op',
    r'Cooperative;coop\.;co-operative;co-\rop;association;assn;company;co;incorporated;inc\.;corporation;corp\.',
    r'Cooperative;coop\.;co-operative;or co-op',
    r'Corp\.',
    r'Corp\. diritto pubb\.',
    r'Corp\. droit public',
    r'Corp\. publ\. co\.',
    r'Corp\.;Corp;Co\.;Co;Inc\.;Inc;Ltd\.;Ltd;Corporation;Company;Incorporated;Limited',
    r'Corp\.;Inc\.;Co\.;Ltd\.',
    r'Corp\.;Inc\.;Co\.;Ltd\.;P\.C\.;Chtd',
    r'Corp\.;Ltd\.;Inc\.',
    r'Corporation de fiducie;Compagnie de fiducie;Corporation\rfiduciaire;Compagnie fiduciaire;Société fiduciaire',
    r'Corporation de prêt;Société de prêt;Compagnie de prêt',
    r'Corporation;Company;Incorporated;Corp\.; Inc\.; Co;Chartered;P\.A\.',
    r'Corporation;Company;Incorporated;Incorporation;Limited;Corp;Co;Inc;Ltd',
    r'Corporation;Company;Incorporated;Limited;Corp;Co;Inc;Ltd',
    r'Corporation;Incorporated;Company;Limited',
    r'Corporation;Incorporated;Company;Limited;Corp\.;Inc\.;Co\.;Ltd\.',
    r'Corporation;Incorporated;Company;Limited;Corp;Inc\. Co\.;Ltd\.',
    r'Corporation;Incorporated;Company;Limited;Corp;Inc\.;Co\.;Ltd\.',
    r'Corporation;Incorporated;Corp\.;Inc\.',
    r'Cía S\. en C\.',
    r'Cía SCA\.',
    r'Cía\. S\. en C\.',
    r'Cía\., S\.C\.A\.',
    r'DA',
    r'DAC – \(limited by guarantee\)',
    r'DAC – \(limited by shares\)',
    r'DOO',
    r'District Improvement Company',
    r'Doplnková dôchod\.poisť\.',
    r'Družstevný podnik poľ\.',
    r'E\.E\.I\.G',
    r'E\.I\.R\.L',
    r'E\.I\.R\.L\.',
    r'E\.R\.L\.',
    r'E\.U',
    r'E\.U\.',
    r'EB',
    r'EBVBA',
    r'EBVBA SO',
    r'EE',
    r'EEIG',
    r'EESV',
    r'EGE',
    r'EGIU',
    r'EGIZ',
    r'EGTS',
    r'EHZS',
    r'EI',
    r'EIRELI',
    r'EIRL',
    r'EKB',
    r'EKG',
    r'EKGmsZ',
    r'EL
]


#### LIST WITH SPECIAL CHARACTERS ######


patterns = [
    r'\(Guarantee\) Ltd\.',
    r'\(SPV\) Ltd',
    r'\(SPV\) SPC',
    r'\(유\)',
    r'\(주\)',
    r'A',
    r'A Limited Partnership;An Incorporated Limited\rPartnership;LP;LP.;Lp.;Lp;I.L.P;ILP',
    r'A\. C\.',
    r'A\.C\.',
    r'A\.E\.I\.E\.',
    r'A\.F\.',
    r'A\.G\.',
    r'A\.I\.E\.',
    r'A/S',
    r'AA',
    r'AB',
    r'ABV',
    r'AEIE',
    r'AF',
    r'AG',
    r'AGes\.',
    r'AGmsZ',
    r'AISBL',
    r'AM',
    r'AMBA',
    r'ANS',
    r'APB',
    r'AS',
    r'ASA',
    r'ASBL',
    r'ASBL DPU',
    r'ASC',
    r'ASSEP',
    r'AVV;avv;A\.V\.V\.;a\.v\.v\.',
    r'Akc\. spol\.',
    r'Ambasciate',
    r'Ambassade',
    r'ApS',
    r'Assoc\.',
    r'Aus\. Unt\.',
    r'Ausl\. AG & LTD',
    r'Ausl\. Gen\. & GMBH',
    r'Ausl\. Rechtsform',
    r'AÜ',
    r'B\.T\.;BT',
    r'BA',
    r'BAB',
    r'BBL',
    r'BI',
    r'BN',
    r'BO',
    r'BR',
    r'BRF',
    r'BRL',
    r'BV',
    r'BV BVBA',
    r'BV CVA',
    r'BV CVBA',
    r'BV CVOA',
    r'BV GCV',
    r'BV LV',
    r'BV NV',
    r'BV PR',
    r'BV VOF',
    r'BV;bv;B\.V\.;b\.v\.',
    r'BVBA',
    r'BVBA SO',
    r'Banka - a\. s\.',
    r'Banka-štát\.peňaž\.ústav',
    r'BenCom',
    r'Botschaft',
    r'Branch RC',
    r'Bt\.',
    r'Bund',
    r'C\.E\.R\.',
    r'C\.R\.A\.',
    r'C/A',
    r'CB',
    r'CC',
    r'CCC;C\.C\.C\.',
    r'CCSDA',
    r'CEMIX',
    r'CIA LTDA',
    r'CIC',
    r'CLF',
    r'CLG',
    r'CNCOL',
    r'COOP',
    r'CORPORATION;COMPANY;LIMITED;CORP;INC;CO;LTD',
    r'CRC',
    r'CSL',
    r'CV',
    r'CV PR',
    r'CV;cv;C\.V\.;c\.v\.',
    r'CVA SO',
    r'CVBA',
    r'CVBA PR',
    r'CVBA SO',
    r'CVOA',
    r'CVOA CD',
    r'CVOA SO',
    r'Cant\. publ\. co\.',
    r'Canton',
    r'Cantonal administration',
    r'Cantone',
    r'Co-op',
    r'Co-op;C\.A\.',
    r'Co-op;Coop;Assoc\.;Assoc;Assn\.;Assn',
    r'Co-operative Limited;Cooperative Limited;Co-op Limited;Coop Limited;Co-\roperative Ltd\.;Cooperative Ltd\.;Co-opLtd\.;Coop Ltd\.;Co-\roperative;Cooperative;Co-op;Coop',
    r'Co-operative Ltd;Coopérative Ltée',
    r'Co-operative and Limited;Ltd\.;Co-opérative and Limitée;Ltée',
    r'Co-operative;Coopérative',
    r'Co\.;corp\.;inc\.;ltd\.',
    r'Comm\.V',
    r'Comm\.VA',
    r'CommV',
    r'Commune',
    r'Community Interest Company;société d’intérêt\rcommunautaire;C\.I\.C\.;CIC;S\.I\.C\.;SIC',
    r'Company;Co\.;Corporation;Corp\.;Incorporated;Inc\. Limited;Ltd\.',
    r'Company;Co\.;Corporation;Corp\.;Incorporated;Inc\. Limited;or Ltd\. Professional\rCorporation or P\.C\. for those rendering professional services\.',
    r'Company;Corporation;Corp\.;Incorporated;Inc\.',
    r'Comune',
    r'Condominium Corporation',
    r'Confederazione',
    r'Confédération',
    r'Coop & Sarl étranger',
    r'Coop\. & SAGL estero',
    r'Cooperative Limited;Cooperative Ltd\.;Cooperative Inc\.;Cooperative\rincorporated;Co-operative Limited;Co-operative Ltd;Co-operative Inc;Co-\roperative incorporated;Coopérative limitée;Coopérative ltée;Pool Limited;Pool\rLtd\.;Pool Inc\.;Pool incorporated;Co-op Limited;Co-op limitée;Co-op\rincorporated;Co-op incorporée;Co-op Inc\.',
    r'Cooperative;co-op',
    r'Cooperative;coop\.;co-operative;co-\rop;association;assn;company;co;incorporated;inc\.;corporation;corp\.',
    r'Cooperative;coop\.;co-operative;or co-op',
    r'Corp\.',
    r'Corp\. diritto pubb\.',
    r'Corp\. droit public',
    r'Corp\. publ\. co\.',
    r'Corp\.;Corp;Co\.;Co;Inc\.;Inc;Ltd\.;Ltd;Corporation;Company;Incorporated;Limited',
    r'Corp\.;Inc\.;Co\.;Ltd\.',
    r'Corp\.;Inc\.;Co\.;Ltd\.;P\.C\.;Chtd',
    r'Corp\.;Ltd\.;Inc\.',
    r'Corporation de fiducie;Compagnie de fiducie;Corporation\rfiduciaire;Compagnie fiduciaire;Société fiduciaire',
    r'Corporation de prêt;Société de prêt;Compagnie de prêt',
    r'Corporation;Company;Incorporated;Corp\.; Inc\.; Co;Chartered;P\.A\.',
    r'Corporation;Company;Incorporated;Incorporation;Limited;Corp;Co;Inc;Ltd',
    r'Corporation;Company;Incorporated;Limited;Corp;Co;Inc;Ltd',
    r'Corporation;Incorporated;Company;Limited',
    r'Corporation;Incorporated;Company;Limited;Corp\.;Inc\.;Co\.;Ltd\.',
    r'Corporation;Incorporated;Company;Limited;Corp;Inc\. Co\.;Ltd\.',
    r'Corporation;Incorporated;Company;Limited;Corp;Inc\.;Co\.;Ltd\.',
    r'Corporation;Incorporated;Corp\.;Inc\.',
    r'Cía S\. en C\.',
    r'Cía SCA\.',
    r'Cía\. S\. en C\.',
    r'Cía\., S\.C\.A\.',
    r'DA',
    r'DAC – \(limited by guarantee\)',
    r'DAC – \(limited by shares\)',
    r'DOO',
    r'District Improvement Company',
    r'Doplnková dôchod\.poisť\.',
    r'Družstevný podnik poľ\.',
    r'E\.E\.I\.G',
    r'E\.I\.R\.L',
    r'E\.I\.R\.L\.',
    r'E\.R\.L\.',
    r'E\.U',
    r'E\.U\.',
    r'EB',
    r'EBVBA',
    r'EBVBA SO',
    r'EE',
    r'EEIG',
    r'EESV',
    r'EGE',
    r'EGIU',
    r'EGIZ',
    r'EGTS',
    r'EHZS',
    r'EI',
    r'EIRELI',
    r'EIRL',
    r'EKB',
    r'EKG',
    r'EKGmsZ',
    r'EL'
]


##### List without Escaped Special Characters (for readability) ####

patterns = [
    '(Guarantee) Ltd.',
    '(SPV) Ltd',
    '(SPV) SPC',
    '(유)',
    '(주)',
    'A',
    'A Limited Partnership;An Incorporated Limited Partnership;






