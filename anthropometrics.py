def absi(fit3d_data):
    try:
        return {'absi_score':(float(fit3d_data['waist_circumference']) / 
                          (pow(float(fit3d_data['bmi']),2.0/3.0) * pow(float(fit3d_data['height']),.5)))}
    except ValueError:
        return {'error':'no data'}
    
def NHANES_to_absi(patient_data):
    try:
        return absi({'waist_circumference':float(patient_data['BMXWAIST'])/100.0,
                     'bmi':patient_data['BMXBMI'],
                     'height':float(patient_data['BMXHT'])/100.0})
    except ValueError:
        return {'error':'no data'}

absi_vars_list = {'dbids':['BMXWAIST','BMXBMI','BMXHT'],
                  'outputs':['absi_score'],
                  'calc':NHANES_to_absi}

def sbsi(fit3d_data):
    return {'sbsi_score':((pow(float(fit3d_data['waist_circumference']),7.0/4.0)
                           *pow(float(fit3d_data['height']),5.0/6.0)) 
                          /(float(fit3d_data['body_surface_area']) 
                            * float(fit3d_data['vertical_trunk_circumference'])))}
    
# def NHANES_to_absi(patient_data):
#     return absi({'waist_circumference':patient_data['BMXWAIST'],
#                  'bmi':patient_data['BMXBMI'],
#                  'height':patient_data['BMXHT']})
# 
# sbsi_vars_list = {'dbids':['BMXWAIST','BMXBMI','BMXHT'],
#                   'outputs':['absi'],
#                   'calc':NHANES_to_absi}

def waist_to_hip_ratio(fit3d_data):
    return {'waist_to_hip_ratio_score':(float(fit3d_data['waist_circumference']) / float(fit3d_data['hip_circumference']))}

# def NHANES_to_absi(patient_data):
#     return absi({'waist_circumference':patient_data['BMXWAIST'],
#                  'bmi':patient_data['BMXBMI'],
#                  'height':patient_data['BMXHT']})
# 
# absi_vars_list = {'dbids':['BMXWAIST','BMXBMI','BMXHT'],
#                   'outputs':['absi'],
#                   'calc':NHANES_to_absi}

def trunk_to_leg_ratio(fit3d_data):
    return {'trunk_to_leg_ratio':(float(fit3d_data['trunk_volume']) 
                                  / (float(fit3d_data['right_leg_volume']) + float(fit3d_data['left_leg_volume'])))}
    
# anthropometric_vars = {'mean':{'sbsi_score':.107, 
#                                'waist_to_hip_ratio_score':.882, 
#                                'trunk_to_leg_volume_ratio':1.46},
#                        'sd':{'skeletal_muscle_mass':10, 
#                              'sbsi_score':.007, 
#                              'waist_to_hip_ratio_score':.11, 
#                              'trunk_to_leg_volume_ratio':.22},
#                        'outputs':['sbsi_score', 'waist_to_hip_ratio_score', 'trunk_to_leg_volume_ratio']}

# def NHANES_to_absi(patient_data):
#     return absi({'waist_circumference':patient_data['BMXWAIST'],
#                  'bmi':patient_data['BMXBMI'],
#                  'height':patient_data['BMXHT']})
# 
# absi_vars_list = {'dbids':['BMXWAIST','BMXBMI','BMXHT'],
#                   'outputs':['absi'],
#                   'calc':NHANES_to_absi}

def symmetry(anthropometric_data):
    results = {}
    for key, data in anthropometric_data.items():
        try:
            score = (float(anthropometric_data[key]['right'])-float(anthropometric_data[key]['left'])) \
                        /(float(anthropometric_data[key]['left'])+float(anthropometric_data[key]['right']))
        except ZeroDivisionError:
            score = 0.0
        print('score', score)
        if key in ['dexterity']: #high values are good for dexterity / strength
            results[key] =  {'symmetry_score':-1.0*score}
        else:
            results[key] =  {'symmetry_score':score}
    return results
        

# def symmetry(anthropometric_data):
#     if 'high_is_good' in anthropometric_data and anthropometric_data['high_is_good'] == False \
#         or anthropometric_data['high_is_good'] in ['false', 'False', 'f', 'F', '0']:
#         return {'symmetry_score':(anthropometric_data['left']-anthropometric_data['right']) \
#                 /(anthropometric_data['left']+anthropometric_data['right'])}
#     else:
#         return {'symmetry_score':(anthropometric_data['right']-anthropometric_data['left']) \
#                 /(anthropometric_data['left']+anthropometric_data['right'])}