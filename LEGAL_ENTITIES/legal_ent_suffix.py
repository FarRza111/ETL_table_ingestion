import pandas as pd
import re

# The list of company types provided
company_types = [
    'A Limited Partnership', 'A.C.', 'A.G.', 'A.V.V.', 'AG', 'AGes.', 'AGmsZ', 'AISBL', 'ASBL', 'ASBL DPU', 'ASC',
    'AVV', 'An Incorporated Limited_x000D_Partnership', 'Assoc.', 'Association', 'B.V.', 'BO', 'BV', 'BV BVBA', 
    'BV CVA', 'BV CVBA', 'BV CVOA', 'BV GCV', 'BV LV', 'BV NV', 'BV PR', 'BV VOF', 'BVBA', 'BVBA SO', 'Bhd', 'C.E.R.', 
    'C.I.C.', 'C/A', 'CIC', 'CV', 'CV PR', 'CVA SO', 'CVBA', 'CVBA PR', 'CVBA SO', 'CVOA', 'CVOA CD', 'CVOA SO', 
    'Co-_x000D_operative', 'Co-_x000D_operative Ltd.', 'Co-_x000D_operative incorporated', 'Co-op', 'Co-op Limited', 
    'Co-opLtd.', 'Co-operative', 'Co-operative Inc', 'Co-operative Limited', 'Co-operative Ltd', 'Co-operative and Limited', 
    'Co-opérative and Limitée', 'Co.', 'Comm.V', 'Comm.VA', 'CommV', 'Community Interest Company', 'Compagnie de fiducie', 
    'Compagnie de prêt', 'Compagnie fiduciaire', 'Company', 'Condominium Corporation', 'Coop', 'Coop Limited', 'Coop Ltd.', 
    'Cooperative', 'Cooperative Inc.', 'Cooperative Limited', 'Cooperative Ltd.', 'Cooperative_x000D_incorporated', 
    'Coopérative', 'Coopérative Ltée', 'Coopérative limitée', 'Coopérative ltée', 'Corp.', 'Corporation', 'Corporation de fiducie', 
    'Corporation de prêt', 'Corporation_x000D_fiduciaire', 'Cía S. en C.', 'Cía SCA.', 'E.I.R.L', 'E.I.R.L.', 'E.U.', 'EBVBA', 
    'EBVBA SO', 'EESV', 'EGIU', 'EIRELI', 'EKG', 'EKGmsZ', 'ELP', 'ENT E', 'EP', 'EPP', 'ESV', 'ESV SO', 'ETSPUBLI', 'EU', 
    'EWIV', 'EoG', 'FONDPRIV', 'FUP', 'Fund.', 'GCW SO', 'GEIE', 'GIE', 'GIE FS', 'GIU', 'GVoRP', 'GaR', 'GbHsZ', 'Gen.', 
    'Gen.mbH', 'Gen.mubH', 'Ges.m.b.H.', 'GesbR', 'GmbH', 'GmuHGB', 'GuHsZ', 'I.L.P', 'ILP', 'ISBL', 'IVZW', 'IVoG', 'IZW', 
    'Inc', 'Inc.', 'Incorporated', 'Incorporee', 'Indigenous corporation', 'KEG', 'KG', 'KGaA', 'KGaAmsZ', 'KommG', 'LDC', 
    'LG', 'LLC', 'LLP', 'LP', 'LP.', 'LTDA.', 'LV', 'La Paroisse catholique ukrainienne de', 'Limited', 'Limited Liability Partnership', 
    'Limited Partnership', 'Limitee', 'Limitée', 'Loan Company', 'Loan Corp.', 'Loan Corporation', 'Lp', 'Lp.', 'Ltd', 'Ltd.', 
    'Ltda.', 'Ltee.', 'Ltée', 'Ltée.', 'MMC', 'MS', 'N.V.', 'NL', 'NV', 'NV PR', 'NV SO', 'No Liability', 'OEG', 'OFP', 'OG', 
    'OHG', 'OHGmsZ', 'OI', 'ONP', 'P.C.', 'PGmbH', 'PGmbHmA', 'PRIV ST.', 'PS', 'PTY', 'PTY LTD', 'PTY.', 'PTY. LTD.', 
    'PgbHsZ', 'PmbHsZ', 'Pool Limited', 'Pool_x000D_Ltd.', 'PrSt', 'Proprietary', 'Proprietary Limited', 'Proprietary Ltd', 
    'Pty Limited', 'Pty Ltd', 'Pty Ltd.', 'Pty.', 'Pty. Ltd.', 'Pty_x000D_Ltd', 'QSC', 'RNTBC', 'S. Agr.', 'S. Coop.', 'S. en C.', 
    'S.A.', 'S.A.M.', 'S.A.R.F.', 'S.A.S', 'S.A.U.', 'S.C.', 'S.C.A.', 'S.C.P.', 'S.C.S.', 'S.C.e I.', 'S.C.p.A.', 'S.E', 
    'S.E.C.', 'S.E.N.C.', 'S.E.N.C.R.L.', 'S.I.C.', 'S.L.', 'S.N.C.', 'S.R.L', 'S.R.L.', 'S/A', 'S/S', 'SA', 'SA DPU', 'SA FS', 
    'SASPJ', 'SAT', 'SC', 'SC DPU', 'SC SA', 'SC SAGR', 'SC SCA', 'SC SCRI', 'SC SCRL', 'SC SCS', 'SC SNC', 'SC SPRL', 'SCA', 
    'SCA FS', 'SCE', 'SCM', 'SCRI', 'SCRI CP', 'SCRI FS', 'SCRL', 'SCRL DPU', 'SCRL FS', 'SCS', 'SCS FS', 'SComm', 'SDC', 'SE', 
    'SENCRL', 'SEZC', 'SGR', 'SIC', 'SLM', 'SNC', 'SNC FS', 'SOCIETE EN COMMANDITE', 'SON', 'SPC', 'SPRL', 'SPRL FS', 'SPRLU', 
    'SPRLU FS', 'SRL', 'SRL DPU', 'Sdn Bhd', 'Soc.Col.', 'Society', 'Société de prêt', 'Société fiduciaire', 
    'Société à Responabilité Limitée', 'SpA', 'The Ukrainian Catholic Parish of', 'Trust Co.', 'Trust Company', 'Trust Corp.', 
    'Trust Corporation', 'Trustco', 'Trustee Company', 'Trustee Corp.', 'Trustee_x000D_Corporation', 'U.L.C.', 'ULC', 'UNP', 
    'Unlimited company', 'V.B.A.', 'V.O.F.', 'VBA', 'VOF', 'VOF SO', 'VVZRL', 'VZW', 'VZW PR', 'VoG', 'WIV', 'WIVmsZ', 'ZRG AG', 
    'ZRG EKG', 'ZRG KGaA', 'ZRG LG', 'ZRG OHG', 'ZvGGbH', 'ZvGGugcH', 'ZvGPgbH', 'a religious society', 'a.v.v.', 'avv', 'b.v.', 
    'bv', 'c.p.', 'caisee populaire ltée', 'caisee populaire_x000D_ltée', 'caisse populaire', 'caisse populaire limitée', 
    'caisse populaire_x000D_limitée', 'co-op', 'co-op. ltd.', 'communauté religieuse', 'coop', 'coopératif', 'coopération', 
    'coopérative', 'corp.', 'credit union', 'credit union Limited', 'credit union Ltd', 'credit union Ltd.', 'd.d.', 'd.o.o.', 
    'gnS', 'inc', 'inc.', 'j.d.o.o', 'j.t.d.', 'k.d.', 'limited by_x000D_guarantee', 'limited company', 
    'limited company and limited by_x000D_guarantee', 'limited liability partnership', 'limited partnership', 'limitée', 'ltd.', 
    'ltée', 'n.v.', 'nv', 's.a.', 's.r.l.', 'société d’intérêt_x000D_communautaire', 'stG', 't.p.', 'v.b.a.', 'v.o.f.', 
    'vba', 'vof', 'Ö.-r.AG', 'ÖE', 'ÖfrGmbH', 'ÖrGen.', 'ÖrGmbH', 'ÖrVohGza', 'ААТ', 'АДСИЦ', 'ДЗЗД', 'ЕАД', 'ЕД', 'ЕОИИ', 
    'ЕТ', 'ЗАО', 'ЗАТ', 'КД', 'КДА', 'ОАО', 'ОДО', 'ООО', 'С-ИЕ', 'С-ие', 'СД', 'ТАА', 'ТДА', 'УП', 'ذ.م.م'
]

# Create a regex pattern string by joining all company types with pipe "|"
pattern = r'(' + '|'.join([re.escape(ct) for ct in company_types]) + r')'

# Compile the pattern with IGNORECASE flag for case-insensitive matching
compiled_pattern = re.compile(pattern, re.IGNORECASE)

# Sample DataFrame
data = {'company_type': ['Ltd', 'B.V.', 'XYZ Corp.', 'Inc.', 'Cooperative Ltd.', 'n.v.', 'ÖrVohGza', 'j.t.d.', 'limited partnership']}
df = pd.DataFrame(data)

# Apply the regex pattern to match company types
df['matches'] = df['company_type'].apply(lambda x: bool(compiled_pattern.fullmatch(x)))

# print(df)

df





import re
import pandas as pd

# Lists of suffixes for business entities and financial institutions
business_suffixes = ['Ltd', 'Ltd.', 'Limited', 'LLC', 'Inc', 'Inc.', 'Corporation', 'Corp', 'Corp.', 'GmbH', 'S.A.', 'N.V.', 'B.V.']
financial_suffixes = ['Bank', 'Trust', 'Credit Union', 'Savings', 'Insurance', 'Investment', 'Capital']

# Compile regex patterns for suffixes
business_pattern = re.compile(r'\b(' + '|'.join(re.escape(suffix) for suffix in business_suffixes) + r')\b', re.IGNORECASE)
financial_pattern = re.compile(r'\b(' + '|'.join(re.escape(suffix) for suffix in financial_suffixes) + r')\b', re.IGNORECASE)

def classify_customer(ordering_customer_detail):
    """
    Classifies customers as Individual, Financial Institution, or Business Entity.
    
    Args:
        ordering_customer_detail (str): The ordering customer detail string.
        
    Returns:
        str: Classification as 'Individual', 'Financial', or 'Business Entity'.
    """
    # Check for Financial Institutions
    if financial_pattern.search(ordering_customer_detail):
        return 'Financial'
    
    # Check for Business Entities
    if business_pattern.search(ordering_customer_detail):
        return 'Business Entity'
    
    # Default to Individual if no matches found
    return 'Individual'

# Example DataFrame of ordering customer details
data = {
    'orderingCustomerDetail': [
        'John Doe', 
        'Acme Corp.', 
        'First National Bank', 
        'Jane Smith', 
        'Global Holdings Ltd.', 
        'Investment Trust Co.'
    ]
}
df = pd.DataFrame(data)

# Apply classification
df['CustomerType'] = df['orderingCustomerDetail'].apply(classify_customer)

# import ace_tools as tools; tools.display_dataframe_to_user(name="Customer Segmentation", dataframe=df)
df










