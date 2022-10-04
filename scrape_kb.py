import urllib, json, traceback

vars = {'phq9_score':2,
        'sleep_duration':0,
        'sleep_disturbance':0,
        'sleep_latency':2,
        'daytime_dysfunction_due_to_sleepiness':1,
        'sleep_efficiency':1,
        'overall_sleep_quality':1,
        'need_meds_to_sleep':1,
        'psqi_total_score':6,
        'total_energy_expenditure_in_activity':3573.0,
        'vocabulary':132.0/2.0,
        'attention':142/2.0,
        'flexibility':143/2.0,
        'processing_speed':149/2.0,
        'episodic_memory':124.0/2,
        'dominant_hand_dexterity':60,
        'non_dominant_hand_dexterity':52,
        'dominant_hand_grip_strength':64,
        'non_dominant_hand_grip_strength':62,
        'balance_score':51,
        'systolic_blood_pressure':129,
        'diastolic_blood_pressure':78,
        'heart_rate':65,
        'oxygen_saturation':100,
        'temperature':98.1,
        'absi_score':1,
        'sbsi_score':1,
        'trunk_to_leg_volume_ratio':1,
        'waist_to_hip_ratio_score':1,
        'skeletal_muscle_mass':117.1/234.6*100,
        'percent_body_fat':.126,
        'visceral_fat':.060,
        'albumin':4.3,
        'alkaline_phosphatase':79,
        'alanine_aminotransferase':30,
        'aspartate_aminotransferase':37,
        'blood_urea_nitrogen':18,
        'calcium':9.5,
        'chloride':100,
        'creatinine':1.5,
        'glucose':96,
        'potassium':4.1,
        'sodium':138,
        'total_bilirubin':0.9,
        'total_protein':8.0,
        'cholesterol':177,
        'hdl':77,
        'cholesterol_hdl':2.3,
        'ldl':91,
        'triglycerides':48,
        'vldl':10,
        'non_hdl_cholesterol':100,
        'weight':234.6}

if __name__ == '__main__':
    results = {}
    count = 0
    for var_name in vars.keys():
        try:
            url = "http://kb.lab100.org/normative_data/targets="+var_name+"+"+str(vars[var_name])+"&variables=gender+1,age+40,ethnicity+3"
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            results[var_name] = {}
            for key in ['interpretation', 'percentile']:
                if key in data[0]:
                    results[var_name][key] = data[0][key]
            count += 1
            print(count,'/',len(vars.keys()))
        except:
            count += 1
            print(count,'/',len(vars.keys()))
            print(var_name, 'did not finish')
            print(traceback.print_exc())
    print(json.dumps(results, indent=4, sort_keys=True))
    