import math

#ethnicity, gender
ASCVD_coefficients = {'LN Age (y)':{'AA':{'M':2.469,
                                          'F': 17.114},
                                    'WH':{'M':12.344,
                                          'F':-29.799}},
                      'Ln Age, Squared':{'AA':{'M':0,
                                               'F':0},
                                         'WH':{'M':0,
                                               'F':4.884}},
                      'Ln Total Cholesterol (mg/dL)':{'AA':{'M':0.302,
                                                            'F':0.940},
                                                      'WH':{'M':11.853,
                                                            'F':13.540}},
                      'Ln Age x Ln Total Cholesterol':{'AA':{'M':0,
                                                             'F':0},
                                                       'WH':{'M':-2.664,
                                                             'F':-3.114}},
                      'Ln HDL-C (mg/dL)':{'AA':{'M':-0.307,
                                                 'F':-18.920},
                                           'WH':{'M':-7.990,
                                                 'F':-13.578}},
                      'Ln Age x Ln HDL-C':{'AA':{'M':0,
                                                 'F':4.475},
                                           'WH':{'M':1.769,
                                                 'F':3.149}},
                      'Ln Treated Systolic BP (mmHg)':{'AA':{'M':1.916,
                                                             'F':29.291},
                                                       'WH':{'M':1.797,
                                                             'F':2.019}},
                      'Ln Age x Ln Treated Systolic BP':{'AA':{'M':0,
                                                               'F':-6.432},
                                                         'WH':{'M':0,
                                                               'F':0}},
                      'Ln Untreated Systolic BP (mmHg)':{'AA':{'M':1.809,
                                                               'F':27.820},
                                                         'WH':{'M':1.764,
                                                               'F':1.957}},
                      'Ln Age x Ln Untreated Systolic BP':{'AA':{'M':0,
                                                                 'F':-6.087},
                                                           'WH':{'M':0,
                                                                 'F':0}},
                      'Current Smoker (1=Yes, 0=No)':{'AA':{'M':0.549,
                                                            'F':0.691},
                                                      'WH':{'M':7.837,
                                                            'F':7.574}},
                      'Ln Age x Current Smoker':{'AA':{'M':0,
                                                       'F':0},
                                                 'WH':{'M':-1.795,
                                                       'F':-1.665}},
                      'Diabetes (1=Yes, 0=No)':{'AA':{'M':0.645,
                                                      'F':0.874},
                                                'WH':{'M':0.658,
                                                      'F':0.661}},
                      'Mean (Coefficient x Value)':{'AA':{'M':19.54,
                                                          'F':86.61},
                                                    'WH':{'M':61.18,
                                                          'F':-29.18}},
                      'Baseline Survival':{'AA':{'M':0.8954,
                                                 'F':0.9533},
                                           'WH':{'M':0.9144,
                                                 'F':0.9665}}
                      }


def _ASCVD_10_year_risk_calc_(Ethnicity, Gender, Age, Chol, HDL, SysBP, BP_treated, Smoker, Diabetes):
    cum_sum = 0.0
    cum_sum += ASCVD_coefficients['LN Age (y)'][Ethnicity][Gender]*math.log(Age)
    cum_sum += ASCVD_coefficients['Ln Age, Squared'][Ethnicity][Gender]*math.pow(math.log(Age),2.0)
    cum_sum += ASCVD_coefficients['Ln Total Cholesterol (mg/dL)'][Ethnicity][Gender]*math.log(Chol)
    cum_sum += ASCVD_coefficients['Ln Age x Ln Total Cholesterol'][Ethnicity][Gender]*math.log(Age)*math.log(Chol)
    cum_sum += ASCVD_coefficients['Ln HDL-C (mg/dL)'][Ethnicity][Gender]*math.log(HDL)
    cum_sum += ASCVD_coefficients['Ln Age x Ln HDL-C'][Ethnicity][Gender]*math.log(Age)*math.log(HDL)
    cum_sum += ASCVD_coefficients['Ln Treated Systolic BP (mmHg)'][Ethnicity][Gender]*math.log(SysBP)*BP_treated
    cum_sum += ASCVD_coefficients['Ln Age x Ln Treated Systolic BP'][Ethnicity][Gender]*math.log(Age)*math.log(SysBP)*BP_treated
    cum_sum += ASCVD_coefficients['Ln Untreated Systolic BP (mmHg)'][Ethnicity][Gender]*math.log(SysBP)*(1-BP_treated)
    cum_sum += ASCVD_coefficients['Ln Age x Ln Untreated Systolic BP'][Ethnicity][Gender]*math.log(Age)*math.log(SysBP)*(1-BP_treated)
    cum_sum += ASCVD_coefficients['Current Smoker (1=Yes, 0=No)'][Ethnicity][Gender]*Smoker
    cum_sum += ASCVD_coefficients['Ln Age x Current Smoker'][Ethnicity][Gender]*math.log(Age)*Smoker
    cum_sum += ASCVD_coefficients['Diabetes (1=Yes, 0=No)'][Ethnicity][Gender]*Diabetes
    year_10_risk = 1-math.pow(ASCVD_coefficients['Baseline Survival'][Ethnicity][Gender],
                              math.exp(cum_sum - ASCVD_coefficients['Mean (Coefficient x Value)'][Ethnicity][Gender]))
    return year_10_risk

gender_lookup = {1:'M', 2:'F'}
def ASCVD(Ethnicity = None, Gender = None, Age = None, Cholesterol = None, HDL = None, SysBP = None,
          BP_treated = None, Smoker = None, Diabetes = None):
    comments = []
    risk = "NA"
    if Ethnicity  is None or not Ethnicity in ['WH', 'AA']:
        comments.append('Ethnicity unspecified. Use "AA" for African American, and "WH" for white or other. Results assume WH.')
        Ethnicity = 'WH'

    if Gender is None or not Gender in ['M', 'F']:
        if Gender in [1,2]:
            Gender = gender_lookup[Gender]
        else:
            Gender = 'M'
            comments.append['Gender Unspecified. Use "M" or 1 for male, and "F" or 2 for female. Results assume Male']

    if Age is None:
        comments.append['Age unspecified. Generating score for 40 year old.']
        Age = 40
    elif Age < 40.0 or Age >= 80.0:
        comments.append('Risk calculator is only valid for individuals between 40 to 79 years of age.')
        return risk, comments

    if Cholesterol is None:
        comments.append('Cholesterol level unspecified. Assuming optimal Cholesterol level (170 mg/Dl)')
        Cholesterol = 170.0
    elif Cholesterol < 130.0 or Cholesterol > 320.0:
        comments.append('Cholesterol out of range - enter a value between 130 and 320')
        Cholesterol = max(130, min(HDL, 320))

    if HDL is None:
        comments.append('HDL-Cholesterol level unspecificed. Assuming optimal. (50 mg/Dl)')
        HDL = 50.0
    elif HDL < 20 or HDL > 100:
        comments.append('HDL-Cholesterol out of range - enter a value between 20 and 100')
        HDL = max(20, min(HDL, 100))

    if SysBP  is None:
        comments.append('Systolic Blood Pressue unspecified. Assuming optimal. (110 mm Hg)')
        SysBP = 110.0
    elif SysBP < 90 or SysBP > 200:
        comments.append("Systolic Blood Pressure out of range - enter a value between 90 and 200")
        SysBP = max(90, min(SysBP, 200))

    if BP_treated  is None:
        comments.append('Please specify if medication is being taken to reduce blood pressure. Assuming No.')
        BP_treated = 0
    elif not BP_treated in [0,1]:
        comments.append('BP_treated should be 0 for no treatment and 1 for being treated. Result uses 0.')
        BP_treated = 0

    if Smoker  is None:
        comments.append('Please specify if subject is a smoker. Assuming non-smoker.')
        Smoker = 0
    elif not Smoker in [0,1]:
        comments.append("Smoker should be 0 for non-smoker, 1 for smoker. Assuming non-smoker")
        Smoker = 0

    if Diabetes  is None:
        comments.append("Please specify if subject has diabetes. Assuming non-diabetic")
        Diabetes = 0
    elif not Diabetes in [0,1]:
        comments.append("Diabetes should be 0 for non-diabetic, 1 for diabetic. Assuming non-diabetic.")
        Diabetes = 0

    risk = _ASCVD_10_year_risk_calc_(Ethnicity, Gender, Age, Cholesterol, HDL, SysBP, BP_treated, Smoker, Diabetes)
    return risk, comments
