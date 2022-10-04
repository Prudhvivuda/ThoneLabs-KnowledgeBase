from lib.file import read_csv_universal_newline

cognition_keys = ['Dimensional Change Card Sort', 'Flanker Inhibitory Control and Attention',
                  'Pattern Comparison Processing Speed','Picture Sequence Memory',
                  'Picture Vocabulary']
cognition_out_keys = ['flexibility', 'attention','processing_speed','episodic_memory','vocabulary']

def cognition(cognition_data, source_file = 'data/NIH/cognition_standard_score_to_tscore.csv'): #already been age-corrected
    source_table = read_csv_universal_newline(source_file)
    header = source_table[0]
    body = source_table[1:]
    measured_stat = map(lambda x: int(x[0]), body)
    percentile = map(lambda x: float(x[1]), body)
    t_score = map(lambda x: int(x[2]), body)
    results = {}
    for index, key in enumerate(cognition_keys):
        measured_stat_value = max(59,min(140,int(round(cognition_data[key]))))
        measured_stat_index = measured_stat.index(measured_stat_value)
        results[cognition_out_keys[index]] = {'percentile':percentile[measured_stat_index],
                                              't_score':t_score[measured_stat_index]}
        print(index, key, measured_stat_value, measured_stat_index)

    return results
