from .waist_circumferencevaluesJSON import result_key
from .waist_circumference_percentiles import waist_circumference_percentiles
import bisect 

age_diff = [0, 18, 26, 36, 46, 56, 66, 80]
def get_diff(ls, val):
    for i in range(1, len(ls)):
        if ls[i-1] <= int(val) < ls[i]:
            return i-1
    return 7


def get_percentile(age, gender, value):
    age_index = get_diff(age_diff, age)
    key = "gender_"+str(gender)+"_age_"+str(age_index)
    res_key = result_key[key]
    pos =  bisect.bisect_left(res_key, float(value))
    percentile_index = pos*16 + (age_index+1)
    if gender == 1:
        percentile_index += 8
    print(f"key is: {key}, pos is: {pos}, and value is: {res_key[pos]}, and percentile age_index is: {percentile_index}")

    return waist_circumference_percentiles[str(percentile_index)]

# waist_circumference_percentiles inches