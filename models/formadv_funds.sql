SELECT form_adv_formadvfirm.firm_id, form_adv_privatemasterfund.name AS "form_adv_funds", form_adv_formadvfirm.crd_no AS "crd_no_fund" FROM form_adv_privatemasterfund
LEFT JOIN form_adv_formadvfirm
ON form_adv_privatemasterfund.form_adv_firm_id = form_adv_formadvfirm.id