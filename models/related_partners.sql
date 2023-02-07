SELECT formd_firmformdrelationship.form_d_value_id, CONCAT(formd_firmformdrelationship.first_name, ' ', formd_firmformdrelationship.last_name) AS "related_partners", firms_regulatoryfirm.cik_no AS "cik_no_related_partners" FROM (
    SELECT formd_firmformdrelationship.form_d_value_id, formd_firmformdrelationship.first_name, formd_firmformdrelationship.last_name, formd_firmformdvalue.regulatory_firm_id FROM formd_firmformdrelationship
    LEFT JOIN formd_firmformdvalue
    ON formd_firmformdrelationship.form_d_value_id = formd_firmformdvalue.id
) formd_firmformdrelationship
LEFT JOIN (
    SELECT firms_regulatoryfirm.id, firms_firm.cik_no FROM (
        SELECT id, firm_id FROM firms_regulatoryfirm WHERE form = 'D' OR form = 'D/A'
    ) firms_regulatoryfirm
    LEFT JOIN firms_firm
    ON firms_regulatoryfirm.firm_id = firms_firm.id
) firms_regulatoryfirm
ON formd_firmformdrelationship.regulatory_firm_id = firms_regulatoryfirm.id