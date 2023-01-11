SELECT first_name, last_name FROM formd_firmformdrelationship
LEFT JOIN (
    SELECT formd_firmformdvalue.*, merge_form_d.cik_no, merge_form_d.crd_no, merge_form_d.name FROM formd_firmformdvalue
    LEFT JOIN (
        SELECT form_d.*, firms_firm.cik_no, firms_firm.crd_no, firms_firm.name
        FROM (
            SELECT * FROM firms_regulatoryfirm WHERE form = 'D' OR form = 'D/A'
        ) form_d
        LEFT JOIN firms_firm ON form_d.firm_id = firms_firm.id
    ) merge_form_d
    ON merge_form_d.id = formd_firmformdvalue.regulatory_firm_id
) merge_form_d_firm
ON formd_firmformdrelationship.form_d_value_id = merge_form_d_firm.id
WHERE crd_no IS NULL
LIMIT 100