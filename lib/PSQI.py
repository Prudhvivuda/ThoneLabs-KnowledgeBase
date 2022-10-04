from lib.helper import takeClosest
import time, datetime

#calculates PSQI score

quantifier = {"Not during the past month":0,
              "Less than once a week":1,
              "Once or twice a week":2,
              "Three or more times a week":3,
              "Very good":0,
              "Fairly good":1,
              "Fairly bad":2,
              "Very bad":3}
Q2_coder = lambda x: takeClosest([15.0,30.0,60.0,61.0], x, round = 'up')
Q4_coder = lambda x: takeClosest([7.0,6.0,5.0,0.0], x, round = 'down')
IHSE_coder = lambda x: takeClosest([0.0, 65.0, 75.0, 85.0], x, round = 'down')
Q5_coder = lambda x: takeClosest([0.0, 1.0, 10.0, 19.0], x, round = 'down')
latency_coder = lambda x: takeClosest([0.0, 1.0, 3.0, 5.0], x, round = 'down')
day_dysfunction_coder = lambda x: takeClosest([0.0, 1.0, 3.0, 5.0], x, round = 'down')
def bed_time(T1, T2, Q4):
    T1, T2 = map(lambda x: time.strptime(x,'%H:%M:%S'), [T1,T2])
    T1, T2 = map(lambda x: datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds(), [T1,T2])
    diffhour = abs(T2 - T1)/3600.0
    if diffhour > 24:
        diffhour = diffhour - 24
    tmpbse = (Q4 / diffhour) * 100
    return IHSE_coder(tmpbse)

def disturbance_coder(psqi_data):
    if psqi_data["Question_5J"] in ['', None, 'NA','Null']:
        psqi_data["Question_5J"] = "Not during the past month"
    subtotal = sum(map(lambda x: quantifier[psqi_data['Question_5'+x]], ['B', 'C', 'D', 'E', 'F', 'F', "H", 'I', 'J']))
    return Q5_coder(subtotal)

def PSQI(psqi_data):
    latency = latency_coder(Q2_coder(float(psqi_data["Question_2"]))+quantifier[psqi_data['Question_5A']])
    duration = Q4_coder(float(psqi_data["Question_4"]))
    efficiency = bed_time(psqi_data["Question_1"], psqi_data["Question_3"], float(psqi_data["Question_4"]))
    disturbance = disturbance_coder(psqi_data)
    day_dysfunction = day_dysfunction_coder(quantifier[psqi_data["Question_8"]]+quantifier[psqi_data["Question_9"]])
    quality = quantifier[psqi_data["Question_6"]]
    meds = quantifier[psqi_data["Question_7"]]
    PSQI = sum([latency, duration, efficiency, disturbance, day_dysfunction, quality, meds])
    interpretation = 'Good' if PSQI <= 5 else "Poor"
    return {'psqi_score':PSQI,
            'latency':latency,
            'duration':duration,
            'efficiency':efficiency,
            'disturbance':disturbance,
            'day_dysfunction':day_dysfunction,
            'quality':quality,
            'medication_requirement':meds,
            'interpretation':interpretation}

