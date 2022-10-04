def chol_hdl(vitals_data):
    try:
        return {'chol_hdl_score':(float(vitals_data['cholesterol'])/float(vitals_data['hdl']))}
    except:
        return {'error':'missing data'}

def NHANES_to_chol_hdl(patient_data):
    return chol_hdl({'cholesterol':patient_data['LBXTC'],
                      'hdl':patient_data['LBXHDD']})

chol_hdl_vars_list = {'dbids':['LBXTC','LBXHDD'],
                      'outputs':['chol_hdl'],
                      'calc':NHANES_to_chol_hdl}


def vldl(vitals_data):
    return float(vitals_data['triglycerides'])/5.0