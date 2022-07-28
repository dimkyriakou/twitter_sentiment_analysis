db_name = 'TWSDB'
words = ['BMW', 'FERRARI', 'MERCEDES']

def main_query(db_name, word):
    q =  "SELECT TEXT                 " \
         "     , DT_POSTED            " \
         "     , SENTIMENT            " \
         "     , SRCH_WRD             " \
        f" FROM {db_name}.TWEETS      " \
        f" WHERE SRCH_WRD = {word}    "
    return q

def pol_query(db_name, word):
    q = f"SELECT POLARITY AS POLARITY_{word}  " \
        f"FROM {db_name}.TWEETS               " \
        f"WHERE search_word = {word}          "
    return q

def subj_query(db_name, word):
    q = f"SELECT SUBJECTIVITY AS SUBJECTIVITY_{word}  " \
        f"FROM {db_name}.TWEETS                       " \
        f"WHERE search_word = {word}                  "
    return q