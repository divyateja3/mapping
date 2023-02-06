import pandas as pd


def _preprocess_formd_funds(dataFrame):
    def _transform_formd_funds(value):
        value = value.upper()
        remove_terms = {
            'LLC', 'LP', 'LTD', 'INC', 'CO', 'CORP'
        }
        newVal = []
        for name in value.split():
            if name in remove_terms:
                continue
            alphaName = filter(lambda x: not x.isdigit(), name)
            alphaName = ''.join(alphaName).strip()
            newVal.append(alphaName)
        return ' '.join(newVal)

    # Transform form_d_funds
    dataFrame.form_d_funds = dataFrame.form_d_funds.str.replace('(', '', regex=False)
    dataFrame.form_d_funds = dataFrame.form_d_funds.str.replace(')', '', regex=False)
    dataFrame.form_d_funds = dataFrame.form_d_funds.str.replace(',', '', regex=False)
    dataFrame.form_d_funds = dataFrame.form_d_funds.str.replace('.', '', regex=False)
    dataFrame.form_d_funds = dataFrame.form_d_funds.str.replace('@', '', regex=False)
    dataFrame.form_d_funds = dataFrame.form_d_funds.str.replace('/', ' ', regex=False)
    dataFrame.form_d_funds = dataFrame.form_d_funds.str.replace('-', ' ', regex=False)
    dataFrame.form_d_funds = dataFrame.form_d_funds.apply(_transform_formd_funds)
    dataFrame.form_d_funds = dataFrame.form_d_funds.str.title()

    return dataFrame


def _preprocess_formadv_funds(dataFrame):

    def _transform_formadv_funds(value):
        value = value.upper()
        remove_terms = {
            'LLC', 'LP', 'LTD', 'INC', 'CO', 'CORP', 'LLLP', 'LLLC'
        }
        newVal = []
        for name in value.split():
            if name in remove_terms:
                continue
            alphaName = filter(lambda x: not x.isdigit(), name)
            alphaName = ''.join(alphaName).strip()
            newVal.append(alphaName)
        return ' '.join(newVal)

    # Transform form_adv_funds
    dataFrame.form_adv_funds = dataFrame.form_adv_funds.str.replace('(', '', regex=False)
    dataFrame.form_adv_funds = dataFrame.form_adv_funds.str.replace(')', '', regex=False)
    dataFrame.form_adv_funds = dataFrame.form_adv_funds.str.replace(',', '', regex=False)
    dataFrame.form_adv_funds = dataFrame.form_adv_funds.str.replace('.', '', regex=False)
    dataFrame.form_adv_funds = dataFrame.form_adv_funds.str.replace('@', '', regex=False)
    dataFrame.form_adv_funds = dataFrame.form_adv_funds.str.replace('/', ' ', regex=False)
    dataFrame.form_adv_funds = dataFrame.form_adv_funds.str.replace('-', ' ', regex=False)
    dataFrame.form_adv_funds = dataFrame.form_adv_funds.apply(_transform_formadv_funds)
    dataFrame.form_adv_funds = dataFrame.form_adv_funds.str.title()

    return dataFrame


def _preprocess_related_partners(dataFrame):
    def _transform_related_partners(value):
        value = value.upper()
        remove_terms = {
            'LLC', 'LTD', 'INC', 'NA', 'NONE'
        }
        newVal, dupCheck = list(), set()
        for name in value.split():
            if name in remove_terms:
                continue
            alphaName = filter(lambda x: not x.isdigit(), name)
            alphaName = ''.join(alphaName).strip()
            if alphaName not in dupCheck:
                newVal.append(alphaName)
                dupCheck.add(alphaName)

        return ' '.join(newVal)

    # Transform related_partners
    dataFrame.related_partners = dataFrame.related_partners.str.replace('(', '', regex=False)
    dataFrame.related_partners = dataFrame.related_partners.str.replace(')', '', regex=False)
    dataFrame.related_partners = dataFrame.related_partners.str.replace(',', '', regex=False)
    dataFrame.related_partners = dataFrame.related_partners.str.replace('.', '', regex=False)
    dataFrame.related_partners = dataFrame.related_partners.str.replace('@', '', regex=False)
    dataFrame.related_partners = dataFrame.related_partners.str.replace('/', ' ', regex=False)
    dataFrame.related_partners = dataFrame.related_partners.str.replace('-', ' ', regex=False)
    dataFrame.related_partners = dataFrame.related_partners.apply(_transform_related_partners)
    dataFrame.related_partners = dataFrame.related_partners.str.title()

    return dataFrame


def _preprocess_direct_owners(dataFrame):
    def _transform_direct_owners(value):
        value = value.upper()
        remove_terms = {
            'LLC', 'LTD', 'INC', 'NA', 'NONE'
        }
        newVal, dupCheck = list(), set()
        for name in value.split():
            if name in remove_terms:
                continue
            alphaName = filter(lambda x: not x.isdigit(), name)
            alphaName = ''.join(alphaName).strip()
            if alphaName not in dupCheck:
                newVal.append(alphaName)
                dupCheck.add(alphaName)

        return ' '.join(newVal)

    # Transform direct_owners
    dataFrame.direct_owners = dataFrame.direct_owners.str.replace('(', '', regex=False)
    dataFrame.direct_owners = dataFrame.direct_owners.str.replace(')', '', regex=False)
    dataFrame.direct_owners = dataFrame.direct_owners.str.replace(',', '', regex=False)
    dataFrame.direct_owners = dataFrame.direct_owners.str.replace('.', '', regex=False)
    dataFrame.direct_owners = dataFrame.direct_owners.str.replace('@', '', regex=False)
    dataFrame.direct_owners = dataFrame.direct_owners.str.replace('/', ' ', regex=False)
    dataFrame.direct_owners = dataFrame.direct_owners.str.replace('-', ' ', regex=False)
    dataFrame.direct_owners = dataFrame.direct_owners.apply(_transform_direct_owners)
    dataFrame.direct_owners = dataFrame.direct_owners.str.title()

    return dataFrame


def preprocess(dataframe: pd.DataFrame, **parm):

    if parm.get('formd_funds'):
        return _preprocess_formd_funds(dataframe)

    if parm.get('formadv_funds'):
        return _preprocess_formadv_funds(dataframe)

    if parm.get('related_partners'):
        return _preprocess_related_partners(dataframe)

    if parm.get('direct_owners'):
        return _preprocess_direct_owners(dataframe)

    return pd.DataFrame(dataframe)
