
from copy import deepcopy

comments = {'Low': "Both quantity and quality of your daily physical activity need improvement. You should dedicate "+\
                    "150 to 300 minutes per week to moderate intensity physical activity to promote prevention of "+\
                    "cardiometabolic diseases and some cancers. In parallel, you also should reduce your sedentary "+\
                    "time. More than 7 hours per day of sedentary activity is associated with an increase of 60% in "+\
                    "the risk of death, compared to those total less than 1. An optimal target is to maintain daily "+\
                    "sedentary time below to 4 hours, even if this may not always be possible because of health and/or "+\
                    "job characteristics.",
            'Medium': "You have a normal amount of daily physical activity. In order to keep or improve it, it is "+\
                    "important to pay attention to both time dedicated to physical activities of moderate intensity, which "+\
                    "must not fall below 150 minutes per week, and time of inactivity, which must be kept below of 4 hours "+\
                    "per day. Both of these variables are independently correlated with health.",
            'High':"Your daily physical activity is qualitatively and quantitatively appropriate: both intensity "+\
                    "and duration of your daily physical activity fully meet the general guidelines for health. Remember "+\
                    "that both daily physical activity and sedentary time are independently correlated with health."
            }
def IPAQ (patient_data):
    pateitn_data = deepcopy(patient_data)
    for key in ['vigorous', 'moderate', 'walking']:
        if not key+'_days' in patient_data:
            patient_data[key+'_days'] = 0

    time_per_day = {'vigorous':(float(patient_data['vigorous_hours'])*60 if 'vigorous_hours' in patient_data else 0.0) + \
                                + (float(patient_data['vigorous_mins']) if 'vigorous_mins' in patient_data else 0.0),
                    'moderate':(float(patient_data['moderate_hours'])*60 if 'moderate_hours' in patient_data else 0.0) \
                                + (float(patient_data['moderate_mins']) if 'moderate_mins' in patient_data else 0.0),
                    'walking':(float(patient_data['walking_hours']) *60 if 'walking_hours' in patient_data else 0.0)\
                                + (float(patient_data['walking_mins']) if 'walking_mins' in patient_data else 0.0)}
    activity = {'vigorous':float(patient_data['vigorous_days']) * time_per_day['vigorous'],
                'moderate':float(patient_data['moderate_days']) * time_per_day['moderate'],
                'walking':float(patient_data['walking_days']) * time_per_day['walking']
                }

    totalPhysicalActivity = max(3.3 * activity['walking'] + 4.0 * activity['moderate'] + 8.0 * activity['vigorous'],.01)
    physlevel = 'High' if float(patient_data['vigorous_days']) >= 3.0 and totalPhysicalActivity > 1500 \
                    or (float(patient_data['vigorous_days'])+float(patient_data['moderate_days'])+float(patient_data['walking_days'])) >= 7.0 and totalPhysicalActivity >= 3000 \
                else \
                'Medium' if float(patient_data['vigorous_days']) >= 3.0 and time_per_day['vigorous'] >= 20 \
                    or float(patient_data['moderate_days']) >= 5.0 and time_per_day['moderate'] >= 30 \
                    or (((float(patient_data['moderate_days']) + float(patient_data['walking_days']) + \
                            float(patient_data['vigorous_days'])) >= 5.0) \
                        and totalPhysicalActivity >= 600) \
                else 'Low'
    physComment = comments[physlevel]

    return {'weekly_level': physlevel,
            'physComment':physComment,
            'met_minutes_per_week':totalPhysicalActivity,
            'vigorous_activity':{'met_minutes_per_week':8.0*activity['vigorous'],
                                 'percent_of_total':8.0*activity['vigorous']/totalPhysicalActivity*100.0},
            'moderate_activity':{'met_minutes_per_week':4.0*activity['moderate'],
                                 'percent_of_total':4.0*activity['moderate']/totalPhysicalActivity*100.0},
            'walking_activity':{'met_minutes_per_week':3.3*activity['walking'],
                                 'percent_of_total':3.3*activity['walking']/totalPhysicalActivity*100.0}}

