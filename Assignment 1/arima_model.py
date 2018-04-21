import math
import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA

'''
Runs the VAR model with given parameters
    - k: the lag to use
    - n: number of features to select (includes mood)
    - test: True if final testing of model, False if just validatin
    - fs: feature selection scheme, either 'Corrs' or 'MSE'
'''

def run_arima(k=1, test=True):
    mses = []
    for i in range(1, 34):
    
        # load patient data
        try:
            data = pd.read_csv(open('./patient_data/p{:02d}.csv'.format(i),'rb'), index_col=0, parse_dates=True)
        except:
            continue

        #print('\n --- Patient {:02d} ---'.format(i))
        
        p_data = data[['next_mood', 'mood']]
        
        # split into training, validation and testing set
        seg = [0.7, 0.1, 0.2]
        t = len(p_data)
        splits = [math.floor(seg[0]*t), math.floor((seg[0]+seg[1])*t)]
        

        # --- Run Model Here on p_data ---

        squared_error = []

        # Train on trainset + parts of validation set
        if test:
            start, stop = splits[1], len(p_data)
        else:
            start, stop = splits[0], splits[1]

        for t in range(start, stop):
            model = ARIMA(p_data['mood'].iloc[:t], order=(k, 1, 0))
            model_fit = model.fit(disp=0)
            yhat = model_fit.forecast()[0][0]
            obs = p_data.iloc[t, 0]
            squared_error.append((obs - yhat)**2)
        
        mse = np.mean(squared_error)
        #print('\nMSE: {}'.format(mse))
        mses.append(mse)

    s = np.std(mses, ddof=1)
    mean = np.mean(mses)
    lb = mean - 2.06*s / math.sqrt(27)
    ub = mean + 2.06*s / math.sqrt(27)
    print('\n\nARIMA model (k={}) results:'.format(k))
    print('Mean: {:.4f}, std: {:.4f}, CI: ({:.4f}, {:.4f}))'.format(mean, s,
                                                                    lb, ub))
    
    return mean 

if __name__ == '__main__':
    results = []

    for k in range(3, 4):
        results.append(run_arima(k, test=True))

    print(results)






    






