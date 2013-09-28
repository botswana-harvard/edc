ARV_DRUG_LIST = (
    ('Nevirapine', 'NVP'),
    ('Kaletra', 'KAL'),
    ('Aluvia', 'ALU'),
    ('Truvada','TRV'),
    ('Tenoforvir', 'TDF',),
    ('Zidovudine', 'AZT'),
    ('Lamivudine', '3TC'),
    ('Efavirenz', 'EFV'),
    ('Didanosine', 'DDI'),
    ('Stavudine', 'D4T'),
    ('Nelfinavir', 'NFV'),
    ('Abacavir', 'ABC'),
    ('Combivir', 'CBV'),
    ('Ritonavir', 'RTV'),
    ('Trizivir', 'TZV'),
    ('Raltegravir', 'RAL'),
    ('Saquinavir,soft gel capsule', 'FOR'),
    ('Saquinavir,hard capsule', 'INV'),
    ('Kaletra or Aluvia', 'KAL or ALU'),
    ('Atripla', 'ATR'),
    ('HAART,unknown', 'HAART,unknown'),
)

ARV_MODIFICATION_REASON = (
    ('Initial dose', 'Initial dose'),
    ('Never started', 'Never started'),
    ('Toxicity decreased_resolved', 'Toxicity decreased/resolved'),
    ('Completed PMTCT intervention', 'Completed PMTCT intervention'),
    ('Completed postpartum tail', 'Completed postpartum "tail"'),
    ('Scheduled dose increase','Scheduled dose increase'),
    ('Confirmed infant HIV infection, ending study drug', 'Confirmed infant HIV infection, ending study drug'),
    ('completed protocol','Completion of protocol-required period of study treatment'),
    ('HAART not available', 'HAART not available'),
    ('Anemia', 'Anemia'),
    ('Bleeding', 'Bleeding'),
    ('CNS symptoms', 'CNS symptoms (sleep, psych, etc)'),
    ('Diarrhea', 'Diarrhea'),
    ('Fatigue', 'Fatigue'),
    ('Headache', 'Headache'),
    ('Hepatotoxicity', 'Hepatotoxicity'),
    ('Nausea', 'Nausea'),
    ('Neutropenia', 'Neutropenia'),
    ('Thrombocytopenia', 'Thrombocytopenia'),
    ('Vomiting', 'Vomiting'),
    ('Rash', 'Rash'),
    ('Rash resolved', 'Rash resolved'),
    ('Neuropathy', 'Neuropathy'),
    ('Hypersensitivity_allergic reaction', 'Hypersensitivity / allergic reaction'),
    ('Pancreatitis', 'Pancreatitis'),
    ('Lactic Acidiosis', 'Lactic Acidiosis'),
    ('Pancytopenia', 'Pancytopenia'), 
    ('Virologic failure', 'Virologic failure'),
    ('Immunologic failure', 'Immunologic failure(CD4)'),
    ('Clinical failure',  'Clinical failure'), 
    ('Clinician request', 'Clinician request, other reason (including convenience)'),
    ('Subject request', 'Subject request, other reason (including convenience)'), 
    ('Non-adherence with clinic visits', 'Non-adherence with clinic visits'),
    ('Non-adherence with ARVs', 'Non-adherence with ARVs'), 
    ('Death', 'Death'),
    ('OTHER', 'Other'),
)    

ARV_STATUS = (
    ('no_mod', '1. No modifications made to existing HAART treatment',),
    ('start', '2. Started antriretroviral treatment since last attended scheduled visit(including today)',),
    ('discontinued','3. Permanently discontinued antiretroviral treatment at or before last study visit',),
    ('modified', '4. Change in at least one antiretroviral medication since last attended scheduled visit (including today)(dose modification, permanent discontinuation, temporary hold, resumption / initiation after temporary hold)',),
)

ARV_STATUS_WITH_NEVER = (
    
    ('no_mod', '1. No modifications made since the last attended scheduled visit or today'),
    ('start', '2. Starting today or has started since last attended scheduled visit'),
    ('discontinued', '3. Permanently discontinued at or before the last attended scheduled visit'),
    ('never started', '4. Never started'),
    ('modified', '5. Change in at least one medication since the last attended scheduled visit or today'),
    ('N/A', 'Not applicable'),
)  

DOSE_STATUS = (
    ('New', 'New'),
    ('Permanently discontinued', 'Permanently discontinued'),
    ('Temporarily held', 'Temporarily held'),
    ('Dose modified', 'Dose modified'),
    ('Resumed', 'Resumed'),
    ('Not initiated', 'Not initiated'),
)



