from lib.normalizer import Normalizer, UnsupportedTargetException
import time
    
def blood_draw(blood_draw):
    query_params = blood_draw.get('params', {})
    try:
        normer = Normalizer('NHANES_Downloader/data/',
                                cache_dir = 'data/cached_jsons/',
                                target_variables = blood_draw["targets"],\
                                normalization_variables = {'gender': str(blood_draw['variables']['gender']),\
                                    'age': blood_draw['variables']['age'],\
                                        'ethnicity': blood_draw['variables']['ethinicity']},
                                **query_params
                                )
    except UnsupportedTargetException:
        return {'error':'unsupported target value'}
    start_time = time.time()
    output = normer.get_target_distributions()
    print("Took " + str(time.time()-start_time) + " seconds to get target distributions.")
    return output
   