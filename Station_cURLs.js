## Height
curl -X "POST" "http://10.0.20.10:3030/height/data" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "height": {
    "inches": 3,
    "feet": 6
  }
}'

## PHOTO
curl -X "POST" "http://10.0.20.10:3030/photos/upload" \
     -H "Content-Type: multipart/form-data; charset=utf-8; boundary=__X_PAW_BOUNDARY__" \
     -F "portrait="

## VITALS
curl -X "POST" "http://10.0.20.10:3030/vitals/data" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "temperature": "98.0",
  "hr": "54",
  "map": "96",
  "raw": true,
  "pain": null,
  "bmi": null,
  "respiration": null,
  "weight": null,
  "systolic": "118",
  "diastolic": "80",
  "height": null,
  "pulse": "54",
  "o2sat": "98"
}'

## blood - Lipids
curl -X "POST" "http://10.0.20.10:3030/blood_draw/data" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "LDL": "171",
  "TC/H": "4.2",
  "VLDL": "17",
  "TRIG": "83",
  "nHDLc": "188",
  "CHOL": "247",
  "HDL": "59"
}'

## blood - metabolic
curl -X "POST" "http://10.0.20.10:3030/blood_draw/data" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "BUN": "18",
  "CRE": "0.9",
  "GLU": "99",
  "NA+": "141",
  "CL-": "105",
  "ALP": "70",
  "CA": "9.6",
  "TP": "7.8",
  "TBIL": "0.6",
  "K+": "4.7",
  "tCO2": "25",
  "ALB": "4.0",
  "ALT": "28",
  "AST": "26"
}'

## /body_composition
curl -X "POST" "http://10.0.20.10:3030/body_composition/data" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "fat_free_mass": "31.36",
  "skeletal_muscle_mass": "37.1",
  "weight": "103.96",
  "body_fat_mass": "35.5",
  "segmental_lean_LA": "6.56",
  "segmental_lean_LL": "24.16",
  "segmentl_fat_TR": "0.0",
  "segmentl_fat_LL": "1.0",
  "muscle_control": "25.9",
  "segmentl_fat_RL": "1.1",
  "segmentl_fat_LA": "0.0",
  "extracellular_water": "22.1",
  "segmental_lean_RL": "25.29",
  "total_body_water": "60.2",
  "gender": "M",
  "segmental_lean_RA": "6.84",
  "segmentl_fat_RA": "0.0",
  "dry_lean_mass": "2115",
  "height": "238.8",
  "bmi": "14.6",
  "percent_body_fat": "3.0",
  "bmr": "2115",
  "age": "0.0",
  "visceral_fat_level": "13",
  "segmental_lean_TR": "45.45",
  "fat_control": "16.3",
  "intracellular_water": "38.1",
  "ecw_tbw": "0.366"
}'

## body_scan
curl -X "POST" "http://10.0.20.10:3030/body_scan/data" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "chest_at_blades_back_depth": "834",
  "armscye_right_girth": "574",
  "knee_right_height": "489",
  "arm_right_surface_area": "140470",
  "waist_hip_ratio": "0.9",
  "ankle_left_height_outside": "85",
  "bust_cup_left_angle": "1340",
  "outseam_leg_right_length": "859",
  "acromion_left_height": "1524",
  "torso_across_chest_width": "403",
  "waist_to_seat_left_back": "46",
  "outseam_right_angled": "860",
  "breast_volume_volume_right": "0",
  "ankle_right_girth_10": "317",
  "wrist_right_girth_30": "283",
  "thigh_right_max_girth": "624",
  "chest_at_armscye_width": "352",
  "belly_max_height": "924",
  "shoulder_to_waist_small_back_left_front": "738",
  "torso_across_back_length": "388",
  "hips_at_width_max_girth_front": "528",
  "neck_back_to_wrist_right_length": "799",
  "hips_at_width_max_girth": "1072",
  "bust_girth": "1062",
  "belly_max_width": "380",
  "hip_upper_girth": "1081",
  "shoulder_right_height": "1517",
  "shoulder_right_to_wrist_length": "599",
  "armscye_right_width_caliper": "139",
  "total_crotch_length": "400",
  "hip_top_width": "402",
  "bust_cup_left_depth_2_plane": "26",
  "abdomen_front_depth": "1129",
  "forearm_left_girth": "303",
  "neck_base_width": "183",
  "chest_at_blades_girth": "1075",
  "forearm_right_girth": "296",
  "head_top_height": "1800",
  "calf_right_girth": "419",
  "neck_back_to_knuckle_right": "888",
  "wrist_left_girth_20": "304",
  "wrist_right_girth_20": "297",
  "hip_top_girth": "1076",
  "neck_back_to_waist_small_back_contour": "747",
  "neck_front_to_waist_small_back_contour": "647",
  "waist_front_left_to_calf_length": "515",
  "seat_back_depth": "854",
  "abdomen_back_depth": "856",
  "bust_prominence_right": "239",
  "wrist_left_girth_50": "363",
  "bust_front_depth": "1108",
  "inseam_left_angled": "752",
  "thigh_mid_right_height": "614",
  "ankle_right_height_inside": "73",
  "chest_at_armscye_girth": "1075",
  "body_shape_rating": "71",
  "hips_at_girth_max_girth_back": "553",
  "ankle_left_height_inside": "75",
  "leg_right_volume": "9800",
  "chest_at_armscye_back_depth": "834",
  "waist_small_back_front_depth": "1121",
  "waist_natural_girth_back": "532",
  "bust_cup_left_bottom": "80",
  "wrist_right_girth_10": "235",
  "neck_back_to_elbow_right_length": "493",
  "shoulder_to_shoulder_length_thur_neck": "412",
  "thigh_upper_right_girth": "606",
  "waist_small_back_girth_front": "530",
  "hips_at_girth_max_girth_front": "528",
  "knee_upper_left_girth": "530",
  "neck_to_blade_length_vert": "193",
  "armscye_left_girth": "533",
  "acromion_right_height": "1509",
  "hip_upper_width": "401",
  "bust_volume_upper_inside_right": "12418900",
  "overarm_width": "511",
  "height": "74.0",
  "waist_max_girth_back": "562",
  "belly_max_girth_front": "537",
  "chest_at_armscye_girth_back": "563",
  "shoulder_left_length": "119",
  "bust_cup_right_bottom": "80",
  "bfp": "27.45",
  "acromion_right_to_wrist_length": "599",
  "overarm_girth": "1246",
  "center_back_to_elbow_right": "493",
  "hip_top_girth_front": "528",
  "acromion_left_slope": "48",
  "inseam_right_angled": "744",
  "torso_surface_area": "833480",
  "ankle_left_girth_30": "418",
  "shoulder_crown_right_height": "145",
  "torso_sagittal_girth_front_contour": "856",
  "chest_tilt_girth": "1081",
  "neck_to_blade_contour_length_horiz": "85",
  "ankle_left_girth_60": "612",
  "bust_prominence_short_left": "0",
  "bust_volume_lower_outside_left": "0",
  "bust_cup_right_horizontal_arc": "82",
  "center_back_to_wrist_left": "811",
  "biceps_left_girth": "368",
  "shoulder_left_to_wrist_length": "599",
  "hips_at_width_max_girth_back": "544",
  "seat_girth_front": "528",
  "chest_at_blades_front_depth": "1107",
  "abdomen_width": "402",
  "hips_at_width_max_width": "403",
  "shoulder_right_to_elbow_length": "293",
  "underbust_girth": "1049",
  "ankle_left_girth_0": "371",
  "abdomen_girth": "1077",
  "waist_to_hips_back": "10",
  "waist_natural_width": "346",
  "outseam_left_angled": "860",
  "trunk_leg_vol_ratio": "1.5",
  "belly_max_front_depth": "1142",
  "thigh_max_girth_height": "709",
  "knee_right_girth": "437",
  "neck_to_blade_contour_length": "212",
  "weight": "81",
  "acromion_to_acromion_thru_neck": "427",
  "ankle_left_girth": "371",
  "hips_at_depth_max_girth": "1075",
  "bust_width": "365",
  "hips_at_girth_max_back_depth": "857",
  "breast_volume_volume_left": "0",
  "hips_at_width_max_front_depth": "1128",
  "thigh_upper_right_height": "688",
  "shoulder_to_shoulder_length": "411",
  "acromion_to_wirst_left": "578",
  "hips_at_depth_max_girth_front": "528",
  "waist_natural_girth_front": "507",
  "ankle_right_girth": "393",
  "bust_cup_left_horizontal_arc": "54",
  "elbow_right_girth": "310",
  "waist_small_back_width": "400",
  "neck_base_side_left_height": "1542",
  "chest_at_armscye_front_depth": "1107",
  "chest_at_blades_girth_front": "512",
  "acromion_to_acromion_width": "404",
  "underbust_back_depth": "826",
  "underbust_width": "360",
  "shoulder_left_height": "1519",
  "overarm_arms_down_girth": "1230",
  "waist_front_right_to_floor_length": "854",
  "leg_left_surface_area": "294800",
  "chest_at_armscye_girth_front": "512",
  "hips_at_depth_max_girth_back": "547",
  "calf_left_girth": "430",
  "calf_left_height": "339",
  "bust_prominence_short_right": "0",
  "bust_cup_right_depth_2_plane": "58",
  "hips_at_girth_max_height": "849",
  "shoulder_left_slope": "48",
  "external_user_id": "user-94567631c0",
  "acromion_right_to_elbow_length": "293",
  "bust_height": "1304",
  "underbust_girth_front": "490",
  "hip_upper_height": "848",
  "seat_front_depth": "1127",
  "seat_girth": "1067",
  "bust_cup_left_vertical_length": "202",
  "arm_right_volume": "4100",
  "thigh_mid_left_height": "614",
  "foot_right_length": "256",
  "waist_natural_back_depth": "835",
  "leg_left_volume": "10200",
  "wrist_left_girth_10": "231",
  "shoulder_right_slope": "48",
  "neck_to_blade_length": "219",
  "neck_base_girth_back": "266",
  "armscye_to_wrist_left": "459",
  "wrist_left_girth_40": "353",
  "belly_max_back_depth": "832",
  "seat_girth_back": "539",
  "acromion_left_to_wrist_length": "599",
  "hips_at_girth_max_front_depth": "1129",
  "wrist_right_girth_0": "206",
  "fat_mass": "49.8",
  "center_back_to_elbow_left": "592",
  "abdomen_height": "839",
  "bust_volume_lower_inside_right": "5381400",
  "waist_small_back_girth": "1085",
  "wrist_left_girth_70": "0",
  "neck_to_blade_length_horiz": "93",
  "knee_low_right_girth": "389",
  "bust_volume_upper_inside_left": "5234000",
  "shoulder_to_waist_small_back_right_front": "742",
  "shoulder_right_length": "104",
  "thigh_left_length": "255",
  "waist_to_seat_right_back": "49",
  "bust_cup_left_depth_horizontal": "0",
  "waist_circumference": "74",
  "foot_left_length": "264",
  "waist_to_seat_right": "45",
  "shoulder_left_to_elbow_length": "381",
  "underbust_front_depth": "1116",
  "ankle_left_girth_20": "401",
  "email": "billyjoel@joel.com",
  "chin_height": "1544",
  "abdomen_girth_back": "549",
  "hips_at_depth_max_width": "402",
  "hips_at_girth_max_girth": "1081",
  "abdomen_girth_front": "528",
  "overarm_height": "1367",
  "waist_max_girth": "1100",
  "crotch_height": "739",
  "neck_back_to_elbow_left_length": "592",
  "armscye_left_height": "1373",
  "shoulder_crown_left_height": "122",
  "seat_back_angle": "34",
  "knee_low_left_girth": "394",
  "breast_volume_base_surface_left": "0",
  "ankle_left_girth_50": "545",
  "neck_back_to_knuckle_left": "888",
  "hips_at_width_max_back_depth": "855",
  "external_scan_id": "scan-2430ee4181",
  "ankle_left_girth_80": "1088",
  "underbust_girth_back": "559",
  "hip_upper_girth_front": "528",
  "neck_front_to_bust_left": "219",
  "outseam_leg_left_length": "859",
  "waist_to_seat_left": "45",
  "waist_front_left_to_thigh_length": "145",
  "waist_to_hips_right": "10",
  "acromion_right_length": "123",
  "arm_left_surface_area": "150420",
  "acromion_left_to_elbow_length": "381",
  "bust_back_depth": "832",
  "knee_left_height": "489",
  "arm_left_volume": "4400",
  "foot_left_girth": "289",
  "waist_front_left_to_floor_length": "854",
  "ankle_right_girth_80": "1086",
  "chest_at_armscye_height": "1329",
  "bust_to_waist_small_back_left": "445",
  "belly_max_girth_back": "560",
  "armscye_right_width": "245",
  "waist_to_seat_front": "55",
  "seat_low_height": "808",
  "bust_cup_right_vertical_length": "202",
  "knee_upper_right_girth": "514",
  "waist_natural_girth": "1040",
  "hips_at_depth_max_front_depth": "1129",
  "bust_cup_right_depth_horizontal": "4",
  "waist_max_width": "386",
  "knee_left_girth": "444",
  "shoulder_to_waist_small_back_left_back": "732",
  "small_back_to_crotch_height_diff": "120",
  "thigh_upper_left_girth": "606",
  "bust_prominence_left": "254",
  "neck_back_to_wrist_left_length": "810",
  "hips_at_width_max_height": "824",
  "armscye_to_wrist_right": "440",
  "bust_girth_contoured": "1067",
  "ankle_right_girth_70": "1059",
  "elbow_left_girth": "300",
  "seat_width": "400",
  "waist_max_height": "904",
  "thigh_mid_right_girth": "549",
  "waist_front_right_to_calf_length": "515",
  "birth_year": "1990",
  "hips_at_depth_max_back_depth": "855",
  "bust_volume_lower_inside_left": "2361600",
  "waist_max_girth_front": "538",
  "waist_to_hips_front": "13",
  "neck_base_front_height": "1492",
  "waist_natural_front_depth": "1131",
  "neck_collar_girth": "488",
  "hips_at_depth_max_height": "834",
  "torso_sagittal_girth_front": "841",
  "foot_left_width": "114",
  "bust_cup_right_horizontal_length": "0",
  "ankle_right_girth_60": "584",
  "armscye_avg_height_back": "1346",
  "total_volume": "94700",
  "bust_volume_lower_outside_right": "40300",
  "bust_cup_left_vertical_arc": "205",
  "wrist_left_girth": "211",
  "bmi": "23.3",
  "shoulder_to_waist_small_back_right_back": "742",
  "hips_at_girth_max_width": "401",
  "wrist_left_girth_30": "297",
  "waist_front_right_to_thigh_length": "145",
  "hip_top_height": "837",
  "armscye_left_width": "240",
  "neck_back_to_waist_small_back": "748",
  "wrist_left_girth_60": "165",
  "ankle_spacing": "211",
  "ankle_right_girth_50": "524",
  "wrist_right_girth_70": "0",
  "foot_right_girth": "259",
  "leg_right_surface_area": "301150",
  "scan_date": "2017-09-27 18:21:09",
  "absi": "0.82",
  "acromion_left_length": "115",
  "biceps_right_girth": "341",
  "thigh_right_length": "257",
  "torso_volume": "66300",
  "neck_base_side_right_height": "1539",
  "armscye_right_height": "1361",
  "ankle_right_height_outside": "53",
  "neck_side_to_bust_right": "256",
  "waist_max_front_depth": "1140",
  "chest_at_blades_width": "352",
  "acromion_to_wrist_right": "569",
  "foot_right_width": "93",
  "seat_height": "814",
  "breast_volume_base_surface_right": "0",
  "torso_sagittal_girth": "1795",
  "wrist_right_girth": "200",
  "breast_volume_surface_left": "0",
  "ankle_left_girth_10": "330",
  "wrist_right_girth_60": "136",
  "ankle_right_girth_40": "393",
  "thigh_upper_left_height": "688",
  "wrist_left_girth_0": "214",
  "shoulder_to_shoulder_width": "389",
  "lean_mass": "131.5",
  "waist_small_back_back_depth": "858",
  "torso_sagittal_girth_contour": "1835",
  "chest_at_blades_height": "1329",
  "sbsi": "0.105",
  "neck_base_back_height": "1572",
  "waist_small_back_height": "859",
  "ankle_left_girth_40": "422",
  "waist_to_hips_left": "10",
  "bmr": "1872.0",
  "neck_front_to_bust_right": "211",
  "neck_to_blade_contour_length_vert": "193",
  "bust_volume_upper_outside_right": "63000",
  "ankle_right_girth_0": "394",
  "neck_front_to_waist_small_back": "646",
  "acromion_right_slope": "48",
  "acromion_to_acromion": "425",
  "neck_side_to_bust_left": "262",
  "center_back_to_wrist_right": "799",
  "waist_tilted_down_girth": "1085",
  "bust_cup_right_vertical_arc": "204",
  "ankle_left_girth_70": "1063",
  "underbust_height": "1224",
  "ankle_right_girth_30": "416",
  "waist_natural_height": "1106",
  "thigh_mid_left_girth": "558",
  "wrist_right_girth_50": "372",
  "waist_small_back_girth_back": "556",
  "breast_volume_surface_right": "0",
  "armscye_left_width_caliper": "141",
  "thigh_left_max_girth": "632",
  "bust_girth_back": "561",
  "overarm_arms_down_height": "1367",
  "bust_volume_upper_outside_left": "0",
  "bust_girth_front": "501",
  "bust_to_bust_length": "188",
  "chest_at_blades_girth_back": "563",
  "belly_max_girth": "1097",
  "ankle_right_girth_20": "377",
  "bust_cup_right_angle": "1336",
  "wrist_right_girth_40": "349",
  "armscye_avg_height_front": "1367",
  "waist_max_back_depth": "831",
  "neck_base_girth": "541",
  "bust_cup_left_horizontal_length": "0",
  "bust_to_waist_small_back_right": "445",
  "calf_right_height": "339",
  "waist_to_seat_back": "45",
  "neck_front_to_bust_front": "193"
}'

## cognition
curl -X "POST" "http://10.0.20.10:3030/cognition/data" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "assessment": {
    "status": 3,
    "statusString": "Completed",
    "archived": null,
    "instruments": [
      {
        "skippedOther": null,
        "parserName": "PracticeVocabParser",
        "status": 3,
        "title": "NIH Toolbox Picture Vocabulary Test Age 3+ Practice v2.0",
        "index": 0,
        "medianReactionTime": null,
        "scores": [],
        "dateFinished": "09/21/2017",
        "uuid": "63B5CFAC-A3AC-47B3-8B47-01FF798ED27B",
        "skipped": null,
        "viewName": "NCSPictureVocabularyInstrumentView",
        "dateCreated": "09/21/2017",
        "type": "4D30584C-B948-4F8D-8EC4-7E4B7D4A9EF1",
        "statusString": "Completed",
        "participantTitle": "NIH Toolbox PVT 3+",
        "dateModified": "09/21/2017",
        "dateStartedString": "Sep 21, 2017 03:59:36",
        "dateFinishedString": "Sep 21, 2017 04:00:09",
        "age": null,
        "mode": -1,
        "dateStarted": "09/21/2017"
      },
      {
        "skippedOther": null,
        "parserName": "VocabParser",
        "status": 3,
        "title": "NIH Toolbox Picture Vocabulary Test Age 3+ v2.0",
        "index": 1,
        "medianReactionTime": null,
        "scores": [
          {
            "value": 50.31002,
            "key": "FullyAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 0.4653485,
            "key": "SE",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": 69.09301,
            "key": "NatlPercentileAgeAdj",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 5.56564,
            "key": "Theta",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": 107.4773,
            "key": "AgeAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 108.769,
            "key": "UnadjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          }
        ],
        "dateFinished": "09/21/2017",
        "uuid": "87521ECD-86B3-4C77-8FC7-983E58F64453",
        "skipped": null,
        "viewName": "NCSPictureVocabularyInstrumentView",
        "dateCreated": "09/21/2017",
        "type": "65EB2645-33C9-405F-836E-6A0DFCEC45FE",
        "statusString": "Completed",
        "participantTitle": "NIH Toolbox PVT 3+",
        "dateModified": "09/21/2017",
        "dateStartedString": "Sep 21, 2017 04:00:10",
        "dateFinishedString": "Sep 21, 2017 04:00:51",
        "age": null,
        "mode": 0,
        "dateStarted": "09/21/2017"
      },
      {
        "skippedOther": null,
        "parserName": "FlankerDataParser",
        "status": 3,
        "title": "NIH Toolbox Flanker Inhibitory Control and Attention Test Age 12+ v2.1",
        "index": 2,
        "medianReactionTime": null,
        "scores": [
          {
            "value": 107.2973,
            "key": "UnadjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 102.6748,
            "key": "AgeAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 48.64813,
            "key": "FullyAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 57.07651,
            "key": "NatlPercentileAgeAdj",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 20,
            "key": "RawScore",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": 9.01,
            "key": "ComputedScore",
            "name": null,
            "type": 0,
            "valueString": null
          }
        ],
        "dateFinished": "09/21/2017",
        "uuid": "769EEDDB-1C61-4D5F-9C6C-A3906BAB10FC",
        "skipped": null,
        "viewName": "NCSFlankerInstrumentView",
        "dateCreated": "09/21/2017",
        "type": "BC8ACB1C-D7A6-4451-B9A5-E8B9DC7DCED5",
        "statusString": "Completed",
        "participantTitle": "NIH Toolbox FL 12+",
        "dateModified": "09/21/2017",
        "dateStartedString": "Never",
        "dateFinishedString": "Sep 21, 2017 04:04:48",
        "age": 12,
        "mode": 0,
        "dateStarted": null
      },
      {
        "skippedOther": null,
        "parserName": "DCCSDataParser",
        "status": 3,
        "title": "NIH Toolbox Dimensional Change Card Sort Test Age 12+ v2.1",
        "index": 3,
        "medianReactionTime": null,
        "scores": [
          {
            "value": 2.38,
            "key": "ComputedScore",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": 15.40689,
            "key": "FullyAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 48.84098,
            "key": "AgeAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 0.03240991,
            "key": "NatlPercentileAgeAdj",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 53.24562,
            "key": "UnadjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 9,
            "key": "RawScore",
            "name": null,
            "type": 0,
            "valueString": null
          }
        ],
        "dateFinished": "09/21/2017",
        "uuid": "A1A014C5-D09B-4080-A294-FBBBAE00BDDA",
        "skipped": null,
        "viewName": "NCSDCCSInstrumentView",
        "dateCreated": "09/21/2017",
        "type": "E97B1C3E-8406-4318-8EF4-17C5460EA158",
        "statusString": "Completed",
        "participantTitle": "NIH Toolbox DCCS 12+",
        "dateModified": "09/21/2017",
        "dateStartedString": "Never",
        "dateFinishedString": "Sep 21, 2017 04:09:00",
        "age": 12,
        "mode": 0,
        "dateStarted": null
      },
      {
        "skippedOther": null,
        "parserName": "PracticePatternComparisonParser",
        "status": 3,
        "title": "NIH Toolbox Pattern Comparison Processing Speed Test Age 7+ Practice v2.1",
        "index": 4,
        "medianReactionTime": null,
        "scores": [],
        "dateFinished": "09/21/2017",
        "uuid": "36846550-1BAB-477F-9C45-BD16893A5716",
        "skipped": null,
        "viewName": "NCSPracticePatternComparisonInstrumentView",
        "dateCreated": "09/21/2017",
        "type": "63A5CE60-974F-4F53-9528-9D7376EF8F6C",
        "statusString": "Completed",
        "participantTitle": null,
        "dateModified": "09/21/2017",
        "dateStartedString": "Sep 21, 2017 04:09:02",
        "dateFinishedString": "Sep 21, 2017 04:09:41",
        "age": 7,
        "mode": -1,
        "dateStarted": "09/21/2017"
      },
      {
        "skippedOther": null,
        "parserName": "PatternComparisonParser",
        "status": 3,
        "title": "NIH Toolbox Pattern Comparison Processing Speed Test Age 7+ v2.1",
        "index": 5,
        "medianReactionTime": null,
        "scores": [
          {
            "value": 150.8669,
            "key": "UnadjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 96,
            "key": "ComputedScore",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": 75.87053,
            "key": "FullyAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 99.78168,
            "key": "NatlPercentileAgeAdj",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 68,
            "key": "RawScore",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": 142.756,
            "key": "AgeAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          }
        ],
        "dateFinished": "09/21/2017",
        "uuid": "3E1E1C89-B5FB-4470-9F75-ED17CD379BBC",
        "skipped": null,
        "viewName": "NCSPatternComparisonInstrumentView",
        "dateCreated": "09/21/2017",
        "type": "601D4579-89A9-4D7E-B997-58F125679DDE",
        "statusString": "Completed",
        "participantTitle": "NIH Toolbox PC 7+",
        "dateModified": "09/21/2017",
        "dateStartedString": "Sep 21, 2017 04:09:41",
        "dateFinishedString": "Sep 21, 2017 04:11:29",
        "age": 7,
        "mode": 0,
        "dateStarted": "09/21/2017"
      },
      {
        "skippedOther": null,
        "parserName": "IBAMParser",
        "status": 3,
        "title": "NIH Toolbox Picture Sequence Memory Test Age 8+ Form A v2.1",
        "index": 6,
        "medianReactionTime": null,
        "scores": [
          {
            "value": 5.696232,
            "key": "NatlPercentileAgeAdj",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 81.99607,
            "key": "UnadjIntermediateScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 1,
            "key": "RawScore",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": -1.990286,
            "key": "Theta",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": 385.7679,
            "key": "ComputedScore",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": 0.4113992,
            "key": "SE",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": 76.28806,
            "key": "AgeAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 50.63423,
            "key": "FullyAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 79.28777,
            "key": "UnadjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          }
        ],
        "dateFinished": "09/21/2017",
        "uuid": "3412F88A-D4CA-4BEA-9420-38EDC8BA760A",
        "skipped": null,
        "viewName": "NCSPSMInstrumentView",
        "dateCreated": "09/21/2017",
        "type": "DFBABBE4-E39A-4FEF-9A1A-6082E7788588",
        "statusString": "Completed",
        "participantTitle": "NIH Toolbox PSM 8+ Form A",
        "dateModified": "09/21/2017",
        "dateStartedString": "Never",
        "dateFinishedString": "Sep 21, 2017 04:15:54",
        "age": 8,
        "mode": 0,
        "dateStarted": null
      }
    ],
    "lastArchivedDate": null,
    "itemDateModified": "09/21/2017",
    "uuid": "EBE268FA-5A90-450F-B8B2-7E93B8BCB17B",
    "dateCreated": "09/21/2017",
    "lastUnarchivedDate": null,
    "nameString": "Assessment 8",
    "dateModified": "09/21/2017"
  },
  "participant": {
    "education": {
      "MSSType": 22,
      "MSSTitle": "Masters degree (e.g., MA, MS, MEng, MEd, MSW, MBA)"
    },
    "startingLevelOverrideString": "Masters degree (e.g., MA, MS, MEng, MEd, MSW, MBA)",
    "language": {
      "MSSType": "en-US",
      "MSSTitle": "English"
    },
    "fathersEducationString": null,
    "dob": "02/27/1985",
    "raceString": "White",
    "lastArchivedDate": null,
    "mothersEducation": {
      "MSSType": 22,
      "MSSTitle": "Masters degree (e.g., MA, MS, MEng, MEd, MSW, MBA)"
    },
    "snapshotDateModified": "09/21/2017",
    "fathersEducation": null,
    "guardiansEducationString": "Bachelor\'s degree (e.g., BA, AB, BS)",
    "archived": 0,
    "uuid": "737D76EA-E4C9-42A7-AA04-5403C7C3404B",
    "lastUnarchivedDate": null,
    "guardiansEducation": {
      "MSSType": 21,
      "MSSTitle": "Bachelor\'s degree (e.g., BA, AB, BS)"
    },
    "nameString": "John Doe",
    "mothersEducationString": "Masters degree (e.g., MA, MS, MEng, MEd, MSW, MBA)",
    "dateCreated": "09/21/2017",
    "languageString": "English",
    "ageDuringAssessment": 32,
    "identifier": "69818832",
    "startingLevelOverride": {
      "MSSType": 22,
      "MSSTitle": "Masters degree (e.g., MA, MS, MEng, MEd, MSW, MBA)"
    },
    "handedness": {
      "MSSType": 2,
      "MSSTitle": "Left"
    },
    "genderString": "Male",
    "valid": 1,
    "educationString": "Masters degree (e.g., MA, MS, MEng, MEd, MSW, MBA)",
    "dateModified": "09/21/2017",
    "dobString": "February 27, 1985",
    "ethnicityString": "Not Hispanic or Latino"
  }
}'

## balance
curl -X "POST" "http://10.0.20.10:3030/balance/data" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "assessment": {
    "status": 3,
    "statusString": "Completed",
    "archived": null,
    "instruments": [
      {
        "skippedOther": null,
        "parserName": "BalanceParser",
        "status": 3,
        "title": "NIH Toolbox Standing Balance Test Age 7+ v2.0",
        "index": 0,
        "medianReactionTime": null,
        "scores": [
          {
            "value": 0.4235416,
            "key": "SE",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": 1.0736397,
            "key": "BalanceRatio1",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 109.2463,
            "key": "AgeAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 1.53741,
            "key": "BalanceRatio2",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 58.09485,
            "key": "FullyAdjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 1.190323,
            "key": "ToolboxTheta",
            "name": null,
            "type": 0,
            "valueString": null
          },
          {
            "value": 73.11905,
            "key": "NatlPercentileAgeAdj",
            "name": null,
            "type": 1,
            "valueString": null
          },
          {
            "value": 114.4759,
            "key": "UnadjScaleScore",
            "name": null,
            "type": 1,
            "valueString": null
          }
        ],
        "dateFinished": "09/28/2017",
        "uuid": "242EFE66-DE85-42A8-A20C-37815FAE03AA",
        "skipped": null,
        "viewName": "NTBBalanceInstrumentViewController",
        "dateCreated": "09/28/2017",
        "type": "C4807462-4620-4947-AA23-8A7DB6CCA117",
        "statusString": "Completed",
        "participantTitle": "NIH Toolbox Standing Balance Test 7+",
        "dateModified": "09/28/2017",
        "dateStartedString": "Sep 28, 2017 02:44:28",
        "dateFinishedString": "Sep 28, 2017 02:50:31",
        "age": null,
        "mode": 0,
        "dateStarted": "09/28/2017"
      }
    ],
    "lastArchivedDate": null,
    "itemDateModified": "09/28/2017",
    "uuid": "23E01048-BB54-454D-A1B3-80B1C3AE0723",
    "dateCreated": "09/28/2017",
    "lastUnarchivedDate": null,
    "nameString": "Assessment 11",
    "dateModified": "09/28/2017"
  },
  "participant": {
    "education": {
      "MSSType": 22,
      "MSSTitle": "Masters degree (e.g., MA, MS, MEng, MEd, MSW, MBA)"
    },
    "startingLevelOverrideString": null,
    "language": {
      "MSSType": "en-US",
      "MSSTitle": "English"
    },
    "fathersEducationString": null,
    "dob": "02/12/1987",
    "raceString": "White",
    "lastArchivedDate": null,
    "mothersEducation": {
      "MSSType": 21,
      "MSSTitle": "Bachelor\\'s degree (e.g., BA, AB, BS)"
    },
    "snapshotDateModified": "09/28/2017",
    "fathersEducation": null,
    "guardiansEducationString": "Unknown",
    "archived": 0,
    "uuid": "26423214-5517-456A-B08D-E9A90DECBD43",
    "lastUnarchivedDate": null,
    "guardiansEducation": {
      "MSSType": 999,
      "MSSTitle": "Unknown"
    },
    "nameString": "Craig Pickard",
    "mothersEducationString": "Bachelor\\'s degree (e.g., BA, AB, BS)",
    "dateCreated": "09/28/2017",
    "languageString": "English",
    "ageDuringAssessment": 30,
    "identifier": "75088575",
    "startingLevelOverride": null,
    "handedness": {
      "MSSType": 1,
      "MSSTitle": "Right"
    },
    "genderString": "Male",
    "valid": 1,
    "educationString": "Masters degree (e.g., MA, MS, MEng, MEd, MSW, MBA)",
    "dateModified": "09/28/2017",
    "dobString": "February 12, 1987",
    "ethnicityString": "Not Hispanic or Latino"
  }
}'

## strength
curl -X "POST" "http://10.0.20.10:3030/strength/data" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "right": 131.334,
  "left": 101.643
}'

## dexterity
curl -X "POST" "http://10.0.20.10:3030/dexterity/data" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d $'{
  "right": 16.565537,
  "left": 17.989352
}'