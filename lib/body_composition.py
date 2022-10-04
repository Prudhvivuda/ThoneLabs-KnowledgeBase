from lib.normalizer import Normalizer, UnsupportedTargetException
import time
    
def body_composition(body_composition):
    query_params = {}
    try:
        normer = Normalizer('NHANES_Downloader/data/',
                                cache_dir = 'data/cached_jsons/',
                                target_variables = {"percent_body_fat": body_composition['percent_body_fat'],\
                                    "percent_skeletal_muscle":body_composition['percent_skeletal_muscle']},
                                normalization_variables = {'gender': str(body_composition['gender']),\
                                    'age': body_composition['age']},
                                **query_params
                                )
    except UnsupportedTargetException:
        return {'error':'unsupported target value'}
    start_time = time.time()
    output = normer.get_target_distributions()
    print("Took " + str(time.time()-start_time) + " seconds to get target distributions.")
    return output

