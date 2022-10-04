import scipy.stats, os, json, time
import numpy as np
from scipy.stats import gaussian_kde as sp_kde
import random
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV

#for a density plot, generates the number of local maxima
def generate_num_maxima(y_values):
    num_maxima = 0
    for index, val in enumerate(y_values[1:-1]):
        if val > y_values[index+2] and val > y_values[index]:
            num_maxima += 1
    return num_maxima

#general generate_density_plot_function
def generate_density_plot(distribution = None, stats = None, min = 2.5, max = 97.5, number_of_points = 100, bandwidth = 'auto', method = 'sklearn', filedir = '', override_cache = False):
    print("filedir: " +  filedir)
    if (distribution is not None and stats is not None) or (distribution is None and stats is None):
        raise Exception('Please input either a distribution *or* a set of summary statistics')

    if distribution is not None: #expects a list of floats
        return _generate_density_plot_from_distribution(distribution, lower_bound = min, upper_bound = max, number_of_points = number_of_points, bandwidth = bandwidth, method = method, filedir = filedir, override_cache = override_cache)
    else: #stats
        return _generate_density_plot_from_summary_statistics(stats, lower_bound = min, upper_bound = max, number_of_points = number_of_points)

#generate density plot from population data. Not the best possible implementation! But generates reasonable looking results for the data. It uses sklearn's GridSearchCV function to generate an appropriate bandwidth (which I modify if it has too many local maxima, ie, is too "bumpy") and then fits a KDE to the data using that bandwidth, and outputs a series of x,y coordinates matching the distribution
def _generate_density_plot_from_distribution(distribution, lower_bound = 2.275, upper_bound = 97.725, number_of_points = 100, bandwidth = 'auto', method = 'sklearn', filedir = '', override_cache = False):

    start_time = time.time()

    if len(filedir) > 0:
        hash_code = hash(tuple(sorted(distribution)))
        filepath = filedir+str(hash_code)+'.json'
        if os.path.isfile(filepath) and not override_cache:
            f = open(filepath, 'r')
            output = json.load(f)
            print("Loaded density plot form cache in " + str(time.time()-start_time) + " seconds.")
            return output


    min_value = np.percentile(distribution, lower_bound)
    max_value = np.percentile(distribution, upper_bound)
    mean = np.percentile(distribution, 50.0)
    interval = (max_value-min_value*1.0)/(number_of_points-1)
    x_values = np.arange(min_value, max_value+interval, interval)
    input = np.array(distribution).reshape(-1,1)
    print('Bandwidth selection type for density plot is', bandwidth)
    if method == 'sklearn':
        if bandwidth == 'auto':
            if len(distribution) > 2000:
                bandwidth_input = np.array(random.sample(distribution, 2000)).reshape(-1,1)
            else:
                bandwidth_input = input
            print('Finding best bandwidth for density plot')
            min_adjust = (-.1 if mean < .5 else 0) + (-.1 if mean < 1 else 0) + (-.1 if mean < 10 else 0)

            grid = GridSearchCV(KernelDensity(),
                        {'bandwidth': np.linspace(0.2, 2.0, 10)},
                        cv=20) # 20-fold cross-validation
            grid.fit(bandwidth_input)
            bandwidth = grid.best_params_['bandwidth']
            if bandwidth <= .2:
                print('Optimal bandwidth below .2, rerunning', bandwidth)
                grid = GridSearchCV(KernelDensity(),
                            {'bandwidth': np.linspace(bandwidth-.18, bandwidth, 19)},
                            cv=20) # 20-fold cross-validation
                grid.fit(bandwidth_input)
                bandwidth = grid.best_params_['bandwidth']
            print('Optimal bandwidth for the distribution is:', bandwidth)
        kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(input)
        y_values = map(np.exp, kde.score_samples(x_values.reshape(-1,1)))
        while generate_num_maxima(y_values) > 5 and bandwidth < 1000:
            bandwidth = bandwidth * 1.1
            print('There are too many local maxima in the density plot - the new optimal bandwidth is:', bandwidth)
            kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(input)
            y_values = map(np.exp, kde.score_samples(x_values.reshape(-1,1)))
    elif method =='scipy':
        if bandwidth == 'auto':
            bandwidth = .2
        bandwidth = bandwidth / input.std(ddof=1)
        print('Calculating KDE, new bandwidth is ', bandwidth)
        kde = sp_kde(input, bw_method = bandwidth)
        print('Succcessfully trained KDE')
        y_values = list(kde(x_values.reshape(-1,1)))

    output = list(map(lambda x: (x_values[x], y_values[x]), range(len(x_values))))
    if len(filedir) > 0:
        f = open(filepath, 'w')
        json.dump(output, f)
    print("Generated density plot from distribution in " + str(time.time()-start_time) + " seconds.")
    return output

def _generate_density_plot_from_summary_statistics(stats, lower_bound = 2.275, upper_bound = 97.725, number_of_points = 100):
    norm = scipy.stats.norm(float(stats['mean']), float(stats['sd']))
    min_value = norm.ppf(lower_bound/100.0)
    max_value = norm.ppf(upper_bound/100.0)
    interval = (max_value-min_value*1.0)/(number_of_points-1)
    x_values = np.arange(min_value, max_value+interval, interval)
    return list(map(lambda x: (x_values[x], norm.pdf(x_values[x])), range(len(x_values))))


def _test_distribution(n = 500):
    m1 = np.random.normal(size=n)
    return generate_density_plot(stats = {'mean':0, 'sd':1})


