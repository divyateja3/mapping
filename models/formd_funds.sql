SELECT firms_regulatoryfirm.firm_id AS "form_d_firm_id", formd_firmformdvalue.entity_name AS "form_d_funds", firms_regulatoryfirm.cik_no AS "cik_no_fund" FROM formd_firmformdvalue
LEFT JOIN (
    SELECT firms_regulatoryfirm.id, firms_regulatoryfirm.firm_id, firms_firm.cik_no, firms_firm.crd_no FROM firms_regulatoryfirm
    LEFT JOIN firms_firm
    ON firms_regulatoryfirm.firm_id = firms_firm.id
) firms_regulatoryfirm
ON formd_firmformdvalue.regulatory_firm_id = firms_regulatoryfirm.id