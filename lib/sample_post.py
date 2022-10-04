#this is a sample_post used for testing purposes and for seeing an example data structure for the derived variables functionality
sample_post = \
    {"dsq":
        #All frequency values are in times per month
        {"age": 30,
         "sex": 1,
         "cereal":
            {"cereals":
                [{
                    "freq": .10,
                    "name": "Cheerios",
                    "type": "all"
                    },
                 {
                    "freq": .25,
                    "name": "Branola",
                    "type": "all"
                    },
                 {
                    "freq": .5,
                    "name": "Fruit Harvest",
                    "type": "all"
                    },
                 {
                    "freq": .5,
                    "name": "Oat bran cereal, cooked, fat not added in cooking",
                    "type": "all"
                    }
                    ]
                    },
         "milk":{"freq":"1.0"},
         "soda":{"freq":"0.133"},
         "fruit_juice":{"freq":"0.1"},
         "coffee":{"freq":0},
         "sweet_drinks":{"freq":0},
         "fruit":{"freq":"0.133"},
         "salad":{"freq":"0.714"},
         "potatoes_fried":{"freq":"0.266"},
         "dry_beans":{"freq":"0.133"},
         "potatoes_other":{"freq":"0.2"},
         "grains":{"freq":"0.133"},
         "vegetables":{"freq":"1.0"},
         "salsa":{"freq":"0.166"},
         "pizza":{"freq":"0.0"},
         "tomato_sauce":{"freq":"0.166"},
         "cheese":{"freq":"0.286"},
         "red_meat":{"freq":"0.286"},
         "proc_meat":{"freq":"0.1"},
         "bread":{"freq":"0"},
         "candy":{"freq":0},
         "doughnuts":{"freq":"0.0333"},
         "cookies":{"freq":"0.133"},
         "desserts":{"freq":"0.0"},
         "popcorn":{"freq":"0.0666"},
         },
#          {"age": 30,
#          "sex": 1,
#          "cereal":
#             {"cereals":
#                 [{"freq":0.0/30,
#                   "name":"Oatmeal",
#                   "type":"hot"},
#                  {"freq":0.0/30,
#                   "name":"JA",
#                   "type":"cold"}]
#                     },
#          "milk":
#             {"freq":0.0/30},
#          "soda":{"freq":0.0},
#          "fruit_juice":{"freq":0.0/30},
#          "coffee":{"freq":0.0/7},
#          "sweet_drinks":{"freq":0.0/30},
#          "fruit":{"freq":0.0/30},
#          "salad":{"freq":0.0/30},
#          "potatoes_fried":{"freq":0.0/30},
#          "dry_beans":{"freq":0},
#          "potatoes_other":{"freq":0.0/30.0},
#          "grains":{"freq":0/30},
#          "vegetables":{"freq":0/7},
#          "salsa":{"freq":0/30.0},
#          "pizza":{"freq":0.0},
#          "tomato_sauce":{"freq":0/30},
#          "cheese":{"freq":0/30},
#          "red_meat":{"freq":0.0/30},
#          "proc_meat":{"freq":.0/30},
#          "bread":{"freq":0/30},
#          "candy":{"freq":0.0/30},
#          "doughnuts":{"freq":0/30},
#          "cookies":{"freq":0/30},
#          "desserts":{"freq":0},
#          "popcorn":{"freq":0/30},
#          },
     "acvsd":{"Ethnicity":"WH", #Either WH for white or AA for african american
              "Gender":"M",
              "Age":55,
              "Cholesterol":213,
              "HDL": 50,
              "SysBP" : 120,
              "BP_treated" : 0,
              "Smoker" : 0,
              "Diabetes" : 0},
     "ipaq":{"vigorous_days" : "3",
             "vigorous_hours": "0",
             "vigorous_mins" : "30",
             "moderate_days" : "2",
             "moderate_hours":"0",
             "moderate_mins" : "22",
             "walking_days" : "5",
             "walking_hours":"1",
             "walking_mins" : "0",
             #"sit_min" : 10
             },
#      "nih_motor":{"ethnicity":"African", #None, African, White, Hispanic, or Multi (if child)
#             "age": 24,
#             "male": 1,
#             "education": 12,
#             "endurance":500.0,
#             "lo4mt_usual_pace": 1.7,
#             "lo4mt_fast_pace": 2.3,
#             "dx9h_dominant": 22.0,
#             "dx9h_non_dominant": 21.0,
#             "msgs_dominant": 68.0,
#             "msgs_non_dominant": 68.0,
#             "bam_theta": 0.45
#             },
    "nih_motor":{"ethnicity":5,
                 "age": 68,
                 "gender": 1,
                 "education": 21,
                 #"endurance":500.0,
                 #"lo4mt_usual_pace": 1.7,
                 #"lo4mt_fast_pace": 2.3,
                 "handedness":"right",
                 "grip_strength_right": 84.2,
                 "grip_strength_left": 80.5,
                 "dexterity_right": 24.24,
                 "dexterity_left": 31.0,
                 #"bam_theta": 0.45
                 },
"phq9": {
                            "doing_things": "Several days",
                            "feeling_down": "Not at all",
                            "falling_asleep": "More than half the days",
                            "feeling_tired": "More than half the days",
                            "poor_appetite": "Several days",
                            "feeling_bad": "Not at all",
                            "trouble_concentrating": "Several days",
                            "moving_slowly": "Not at all",
                            "thoughts_of_death": "Not at all",
                            "things_at_home": "Not difficult at all"
                        },
     "psqi":{
                        "Question_1": "01:00:00",
                        "Question_2": "15",
                        "Question_3": "05:00:00",
                        "Question_4": "7.5",
                        "Question_5A": "Not during the past month",
                        "Question_5B": "Three or more times a week",
                        "Question_5C": "Less than once a week",
                        "Question_5D": "Less than once a week",
                        "Question_5E": "Once or twice a week",
                        "Question_5F": "Once or twice a week",
                        "Question_5G": "Once or twice a week",
                        "Question_5H": "Once or twice a week",
                        "Question_5I": "Once or twice a week",
                        "Question_5J": "Less than once a week",
                        "Question_6": "Fairly bad",
                        "Question_7": "Once or twice a week",
                        "Question_8": "Once or twice a week",
                        "Question_9": "Less than once a week"
                    },

     "cognition": {"Picture Sequence Memory": 50.63423,
                   "Picture Vocabulary": 49.31002,
                   "Pattern Comparison Processing Speed": 75.87053,
                   "Flanker Inhibitory Control and Attention": 48.64813,
                   "Dimensional Change Card Sort": 15.40689
                   },
     "blood_pressure":{"systolic blood pressure":150,
                       "diastolic blood pressure":85},
     "absi":{"waist_circumference":0.98044,#80cm, 32 in
             "bmi":26.1,
             "height":1.679956},#163 cm, 64 in
     "sbsi":{"waist_circumference":80,
             "vertical_trunk_circumference":90,
             "body_surface_area":200,
             "height":163},
     "waist_to_hip_ratio":{"waist_circumference":40,
                           "hip_circumference":40,},
     "trunk_to_leg_ratio":{"trunk_volume":50,
                           "right_leg_volume":25,
                           "left_leg_volume":25},
     "chol_hdl":{"cholesterol":102,
                 "hdl":22},
    "balance":{"balance_score":56,
               "balance_ratio_1":1.04,
               "balance_ratio_2":1.14,},
#      "symmetry":{"right":1.1,
#                  "left":1.05,
#                  "high_is_good":False},
     "symmetry": {
        "leanArm": {
            "right": "6.84",
            "left": "6.56",
        },
        "leanLeg": {
            "right": "25.29",
            "left": "24.16",
        },
        "fatArm": {
            "right": "0.0",
            "left": "0.0",
        },
        "fatLeg": {
            "right": "1.1",
            "left": "1.0",
        },
        "biceps": {
            "right": "342",
            "left": "322",
        },
        "forearm": {
            "right": "313",
            "left": "298",
        },
        "thigh": {
            "right": "619",
            "left": "608",
        },
        "calf": {
            "right": "427",
            "left": "419",
        },
        "strength": {
            "left": 80.643,
            "right": 65.334,
        },
        "dexterity": {
            "left": 23.643,
            "right": 23.334,
        }
    }
}

