from .weightvaluesJSON import result_key
from .weight_percentiles import weight_percentiles
import bisect 

age_diff = [0, 18, 26, 36, 46, 56, 66, 80]
def get_diff(ls, val):
    for i in range(1, len(ls)):
        if ls[i-1] <= int(val) < ls[i]:
            return i-1
    return len(age_diff)-1


def get_percentile(age, gender, value):
    age_index = get_diff(age_diff, age)
    key = "gender_"+str(gender)+"_age_"+str(age_index)
    res_key = result_key[key]
    pos1 = bisect.bisect_right(res_key, float(value))-1
    pos2 = bisect.bisect(res_key, float(value))
    if abs(float(value)-res_key[pos1]) < abs(float(value)-res_key[pos2]):
        pos = pos1    
    else:
        pos = pos2
    if pos == 1001: return 99.9
    if pos == 0: return 0.1
    percentile_index = pos*16 + (age_index+1)
    if gender == 1:
        percentile_index += 8
    print(f"key is: {key}, pos is: {pos}, and value is: {res_key[pos]}, and percentile age_index is: {percentile_index}")
    percentile = weight_percentiles[str(percentile_index)]
    print("percentile is", percentile)
    if percentile == 100: return 99.9
    if percentile == 0: return 0.1
    
    return percentile

    

# weight is calculated in LBS