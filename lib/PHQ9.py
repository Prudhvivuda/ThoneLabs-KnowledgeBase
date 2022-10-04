from lib.helper import takeClosest
scorer = {
    "Not at all":0, 
    "Several days":1, 
    "More than half the days":2, 
    "Nearly every day":3
}

phq9_keys = ["doing_things", "feeling_down", "falling_asleep", "feeling_tired", 
             "poor_appetite", "feeling_bad", "trouble_concentrating", "moving_slowly",
             "thoughts_of_death"]
levels = [4,9,14,19,20]
level_comments = ["Minimal Depression", "Mild Depression", "Moderate Depression", "Moderately Severe Depression", "Severe Depression"]

def PHQ9(phq9_data):
    score = 0
    try:
        for key in phq9_keys:
            score = score + scorer[phq9_data[key]]
    except KeyError:
        for key in phq9_keys:
            try:
                subscore = round(phq9_data[key])
            except TypeError:
                print('patient data:', phq9_data[key])
                subscore = 'NA'
            if subscore in [0,1,2,3]:
                score = score + round(phq9_data[key])
            else:
                print(subscore)
                return {'error':'Missing Data'}
    except KeyError as e:
        print('key', key,) 
        print('phq9_data[key]', phq9_data[key],) 
        return {'error':'Missing Data'}
    return {'phq9_score':score,
            'interpretation':level_comments[takeClosest(levels, score, round = "up")]}
    
def NHANES_to_score(patient_data):
    phq9_data = {
        "doing_things": patient_data['DPQ010'],
        "feeling_down": patient_data['DPQ020'],
        "falling_asleep": patient_data['DPQ030'],
        "feeling_tired": patient_data['DPQ040'],
        "poor_appetite": patient_data['DPQ050'],
        "feeling_bad": patient_data['DPQ060'],
        "trouble_concentrating": patient_data['DPQ070'],
        "moving_slowly": patient_data['DPQ080'],
        "thoughts_of_death": patient_data['DPQ090']
    }
    return PHQ9(phq9_data)

phq9_vars_list = {'dbids':['DPQ010','DPQ020','DPQ030','DPQ040','DPQ050','DPQ060','DPQ070','DPQ080', 'DPQ090'],
                  'outputs':['phq9_score'],
                  'calc':NHANES_to_score}