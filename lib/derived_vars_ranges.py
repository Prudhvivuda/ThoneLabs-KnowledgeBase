
derived_var_ranges = \
    {"dsq":
        #All frequency values are in times per month
        {"age": range(18,66,1),
         "sex": [1,2],
         "cereal":
            {"cereals":
                [{
                    "freq": range(0,2,.1),
                    "name": "Cheerios",
                    "type": "all"
                    },
                 {
                    "freq": range(0,2,.1),
                    "name": "Branola",
                    "type": "all"
                    },
                 {
                    "freq": range(0,2,.1),
                    "name": "Fruit Harvest",
                    "type": "all"
                    },
                 {
                    "freq": range(0,2,.1),
                    "name": "Oat bran cereal, cooked, fat not added in cooking",
                    "type": "all"
                    }
                    ]
                    },
         "milk":{"freq":range(0,2,.1)},
         "soda":{"freq":range(0,2,.1)},
         "fruit_juice":{"freq":range(0,2,.1)},
         "coffee":{"freq":range(0,2,.1)},
         "sweet_drinks":{"freq":range(0,2,.1)},
         "fruit":{"freq":range(0,2,.1)},
         "salad":{"freq":range(0,2,.1)},
         "potatoes_fried":{"freq":range(0,2,.1)},
         "dry_beans":{"freq":range(0,2,.1)},
         "potatoes_other":{"freq":range(0,2,.1)},
         "grains":{"freq":range(0,2,.1)},
         "vegetables":{"freq":range(0,2,.1)},
         "salsa":{"freq":range(0,2,.1),
         "pizza":{"freq":range(0,2,.1)},
         "tomato_sauce":{"freq":range(0,2,.1)},
         "cheese":{"freq":range(0,2,.1)},
         "red_meat":{"freq":range(0,2,.1)},
         "proc_meat":{"freq":range(0,2,.1)},
         "bread":{"freq":range(0,2,.1)},
         "candy":{"freq":range(0,2,.1)},
         "doughnuts":{"freq":range(0,2,.1)},
         "cookies":{"freq":range(0,2,.1)},
         "desserts":{"freq":range(0,2,.1)},
         "popcorn":{"freq":range(0,2,.1)},
         },
     "acvsd":{"Ethnicity":["WH",'AA'], #Either WH for white or AA for african american
              "Gender":["M",'F'],
              "Age":range(40,81,1),
              "Cholesterol":range(130,330,10),
              "HDL": range(20,110,10),
              "SysBP" : range(90,210,10),
              "BP_treated" : [0,1],
              "Smoker" : [0,1],
              "Diabetes" : [0,1]},
     "ipaq":{"vigorous_days" : range(0,8,1),
             "vigorous_hours": range(0,9,1),
             "vigorous_mins" : range(0,270,30),
             "moderate_days" : range(0,8,1),
             "moderate_hours":range(0,9,1),
             "moderate_mins" : range(0,270,30),
             "walking_days" : range(0,8,1),
             "walking_hours":range(0,9,1),
             "walking_mins" : range(0,270,30),
             },
    "nih_motor":{"ethnicity":range(1,8,1),,
                 "age": range(18,65,1),
                 "gender": [1,2],
                 "education": range(0,24,1),
                 "handedness": ["right", 'left'],
                 "grip_strength_right": range(0,300,10),
                 "grip_strength_left": range(0,300,10),
                 "dexterity_right": range(5,50,1),
                 "dexterity_left": range(5,50,1),
                 },
"phq9": {
                            "doing_things": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                            "feeling_down": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                            "falling_asleep": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                            "feeling_tired": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                            "poor_appetite": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                            "feeling_bad": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                            "trouble_concentrating": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                            "moving_slowly": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                            "thoughts_of_death": ["Not at all", "Several days", "More than half the days", "Nearly every day"],
                            "things_at_home": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
                        },
     "psqi":{
                        "Question_1": ["010:00:00","01:00:00","02:00:00","03:00:00","04:00:00","05:00:00","06:00:00","07:00:00","08:00:00","09:00:00","10:00:00","11:00:00","12:00:00","13:00:00","14:00:00","15:00:00","16:00:00","17:00:00","18:00:00","19:00:00","20:00:00","21:00:00","22:00:00","23:00:00","24:00:00"],
                        "Question_2": [0,15,30,60,75],
                        "Question_3": ["010:00:00","01:00:00","02:00:00","03:00:00","04:00:00","05:00:00","06:00:00","07:00:00","08:00:00","09:00:00","10:00:00","11:00:00","12:00:00","13:00:00","14:00:00","15:00:00","16:00:00","17:00:00","18:00:00","19:00:00","20:00:00","21:00:00","22:00:00","23:00:00","24:00:00"],
                        "Question_4": [0,5,6,7,8],
                        "Question_5A": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_5B": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_5C": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_5D": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_5E": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_5F": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_5G": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_5H": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_5I": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_5J": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_6": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_7": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"]
                        "Question_8": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"],
                        "Question_9": ["Not during the past month","Less than once a week","Once or twice a week","Three or more times a week","Very good","Fairly good","Fairly bad","Very bad"]
                    },

     "cognition": {"Picture Sequence Memory": range(10,100,10),
                   "Picture Vocabulary": range(10,100,10),
                   "Pattern Comparison Processing Speed": range(10,100,10),
                   "Flanker Inhibitory Control and Attention": range(10,100,10),
                   "Dimensional Change Card Sort": range(10,100,10)
                   }
}

