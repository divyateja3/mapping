SELECT form_adv_directowner.form_adv_firm_id, form_adv_directowner.legal_name AS "direct_owners", form_adv_formadvfirm.crd_no AS "crd_no_owners" FROM form_adv_directowner
LEFT JOIN form_adv_formadvfirm
ON form_adv_directowner.form_adv_firm_id = form_adv_formadvfirm.id