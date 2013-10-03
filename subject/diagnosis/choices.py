STATUS = (
    ('1', 'New'),
    ('2', 'Resolved'),
    ('3', 'New and resolved in same interval'),
    ('4', 'Ongoing, but severity grade increased or decreased'),
    ('5', 'History/Entry'),
    )

GRADE = (
    ('1', 'Mild'),
    ('2', 'Moderate'),
    ('3', 'Severe'),
    ('4', 'Life-threatening'),
    )

METHOD = (
    ('1', 'Culture'),
    ('2', 'Antigen Assay'),
    ('3', 'Antibody'),
    ('4', 'Micropscopy/Pathology'),
    ('5', 'Suspicion by radiology'),
    ('6', 'Clinical diagnosis'),
    ('OTHER_LAB', 'Laboratory, other'),
    ('OTHER', 'Other'),
)
