
#calculate absi. Unused except for finding absi values from nhanes data, but absi got cut
def absi(fit3d_data):
    try:
        return {'absi_score':(float(fit3d_data['waist_circumference']) /
                          (pow(float(fit3d_data['bmi']),2.0/3.0) * pow(float(fit3d_data['height']),.5)))}
    except ValueError:
        return {'error':'no data'}

#get absi from nhanes
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

#get sbsi score wc^(5/6)*height^(7/4) / (bsa * vtc)
def sbsi(fit3d_data):
    return {'sbsi_score':((pow(float(fit3d_data['waist_circumference']),5.0/6.0)
                           *pow(float(fit3d_data['height']),7.0/4.0))
                          /(float(fit3d_data['body_surface_area'])
                            * float(fit3d_data['vertical_trunk_circumference'])))}
#waist to hip ratio calc
def waist_to_hip_ratio(fit3d_data):
    return {'waist_to_hip_ratio_score':(float(fit3d_data['waist_circumference']) / float(fit3d_data['hip_circumference']))}


def trunk_to_leg_ratio(fit3d_data):
    return {'trunk_to_leg_ratio':(float(fit3d_data['trunk_volume'])
                                  / (float(fit3d_data['right_leg_volume']) + float(fit3d_data['left_leg_volume'])))}


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

