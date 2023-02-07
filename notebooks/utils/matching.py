import pandas as pd
from fuzzywuzzy import fuzz

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from ftfy import fix_text


def get_fuzzy_matches_df(matches_df, dataframe_a, dataframe_b):
    def _match_scores(data_a, data_b):

        left_values = list(set(data_a.related_partners))
        right_values = data_b.direct_owners.to_list()

        match_df = []

        for partner in left_values:
            best_owner, best_raio = None, 0
            for owner in right_values:
                ratio = fuzz.SequenceMatcher(None, partner, owner).ratio()
                if ratio > best_raio:
                    best_owner = owner
                    best_raio = ratio
            match_df.append((partner, best_owner, best_raio))

        return pd.DataFrame(match_df, columns=['related_partner', 'direct_owner', 'owners_ratio'])

    matches_list = []

    for idx, entry in matches_df.iterrows():
        cik_no_fund, crd_no_fund = entry.cik_no_fund, entry.crd_no_fund

        table_a = dataframe_a[dataframe_a.cik_no_related_partners == cik_no_fund]
        table_b = dataframe_b[dataframe_b.crd_no_owners == crd_no_fund]

        matches = _match_scores(table_a, table_b)
        matches.columns = ['related_partners', 'direct_owners_fund', 'owners_fund_ratio']

        matches['cik_no_fund'] = cik_no_fund
        matches['crd_no_fund'] = crd_no_fund

        matches_list.append(matches)

    matches = pd.DataFrame()

    for data in matches_list:
        if not data.empty:
            if not matches.empty:
                matches = pd.concat([matches, data], join='inner', ignore_index=True)
            else:
                matches = data

    return matches


def get_matches_df(dataframe_a, dataframe_b, **props):

    def _ngrams(string, n=2):
        string = str(string)
        string = fix_text(string)  # fix text
        n_grams = zip(*[string[i:] for i in range(n)])
        return [''.join(ngram) for ngram in n_grams]

    column_a, column_b = props.get('column_a'), props.get('column_b')
    map_from, map_to = props.get('map_from'), props.get('map_to')

    right_values = dataframe_b[column_b].unique()

    vectorizer = TfidfVectorizer(min_df=1, analyzer=_ngrams, lowercase=False)
    tfidf = vectorizer.fit_transform(right_values)
    nbrs = NearestNeighbors(n_neighbors=1, n_jobs=-1).fit(tfidf)

    # column to match against in the data
    left_values = set(dataframe_a[column_a])  # set used for increased performance

    # matching query
    def _getNearestN(query):
        queryTFIDF_ = vectorizer.transform(query)
        distances, indices = nbrs.kneighbors(queryTFIDF_)
        return distances, indices

    distances, indices = _getNearestN(left_values)

    left_values = list(left_values)  # need to convert back to a list

    matches = []
    for i, j in enumerate(indices):
        temp = [left_values[i], right_values[j][0], distances[i][0]]
        matches.append(temp)

    matches = pd.DataFrame(matches, columns=[f'{map_from}', f'matched_{map_to}', f'{map_to}_confidence'])

    return matches


def get_merged_matches(matches_dataframe, dataframe_a, dataframe_b, **props):

    column_a, column_b = props.get('column_a'), props.get('column_b')
    map_a, map_b = props.get('map_a'), props.get('map_b')
    map_from, map_to = props.get('map_from'), props.get('map_to')

    cik_col = dataframe_a.columns[-1]
    id_col = dataframe_a.columns[0]

    cik_dict = pd.Series(dataframe_a[cik_col].values, index=dataframe_a[map_a]).to_dict()
    id_dict = pd.Series(dataframe_a[id_col].values, index=dataframe_a[map_a]).to_dict()

    cik_matches = [cik_dict[value] for value in matches_dataframe[column_a]]
    id_matches = [id_dict[value] for value in matches_dataframe[column_a]]

    matches_dataframe = pd.concat([matches_dataframe, pd.Series(cik_matches, name=f'cik_no_{map_from}')], axis=1)
    matches_dataframe = pd.concat([matches_dataframe, pd.Series(id_matches, name=f'form_d_{map_from}_id')], axis=1)

    crd_col = dataframe_b.columns[-1]
    id_col = dataframe_b.columns[0]

    crd_dict = pd.Series(dataframe_b[crd_col].values, index=dataframe_b[map_b]).to_dict()
    id_dict = pd.Series(dataframe_b[id_col].values, index=dataframe_b[map_b]).to_dict()

    crd_matches = [crd_dict[value] for value in matches_dataframe[column_b]]
    id_matches = [id_dict[value] for value in matches_dataframe[column_b]]

    matches_dataframe = pd.concat([matches_dataframe, pd.Series(crd_matches, name=f'crd_no_{map_to}')], axis=1)
    matches_dataframe = pd.concat([matches_dataframe, pd.Series(id_matches, name=f'form_adv_{map_to}_id')], axis=1)

    return matches_dataframe
