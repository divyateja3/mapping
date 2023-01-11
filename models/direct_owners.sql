SELECT legal_name FROM form_adv_directowner
LEFT JOIN (
    SELECT cik_not_null.*, firms_firm.name, firms_firm.description
    FROM (
        SELECT * FROM form_adv_formadvfirm WHERE cik_no IS NULL
    ) cik_not_null
    LEFT JOIN firms_firm ON cik_not_null.firm_id = firms_firm.id
) merge_adv_formadvfirm
ON merge_adv_formadvfirm.id = form_adv_directowner.form_adv_firm_id