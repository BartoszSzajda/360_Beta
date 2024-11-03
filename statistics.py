import pandas as pd
import numpy as np
import krippendorff as kripp
import pingouin as pg


def split_data(data):
     #create seperate data sets and replaces their polsih indicators in to the numbers
   

    management_positive = data.iloc[:,4:12]
    management_negative = data.iloc[:,12:20].replace('Zdecydowanie tak', 'Zupełnie nie').replace('Raczej tak', 'Raczej nie').replace('Raczej nie', 'Raczej tak').replace('Zupełnie nie', 'Zdecydowanie tak')
    
    result_positive = data.iloc[:,20:27]
    result_negative = data.iloc[:,27:34].replace('Zdecydowanie tak', 'Zupełnie nie').replace('Raczej tak', 'Raczej nie').replace('Raczej nie', 'Raczej tak').replace('Zupełnie nie', 'Zdecydowanie tak')

    change_positive = data.iloc[:,34:38]
    change_negative = data.iloc[:,38:42].replace('Zdecydowanie tak', 'Zupełnie nie').replace('Raczej tak', 'Raczej nie').replace('Raczej nie', 'Raczej tak').replace('Zupełnie nie', 'Zdecydowanie tak')

    decision_positive = data.iloc[:,42:46]
    decision_negative = data.iloc[:,46:50].replace('Zdecydowanie tak', 'Zupełnie nie').replace('Raczej tak', 'Raczej nie').replace('Raczej nie', 'Raczej tak').replace('Zupełnie nie', 'Zdecydowanie tak')

    communication_positive = data.iloc[:,50:59]
    communication_negative = data.iloc[:,59:68].replace('Zdecydowanie tak', 'Zupełnie nie').replace('Raczej tak', 'Raczej nie').replace('Raczej nie', 'Raczej tak').replace('Zupełnie nie', 'Zdecydowanie tak')

    management = pd.concat([management_positive, management_negative], axis=1, join='inner')
    result = pd.concat([result_positive, result_negative], axis=1, join='inner')
    change = pd.concat([change_positive, change_negative], axis=1, join='inner')
    decision = pd.concat([decision_positive, decision_negative], axis=1, join='inner')
    communication = pd.concat([communication_positive, communication_negative], axis=1, join='inner')

    grade_mapping = {'Zdecydowanie tak': 4, 'Raczej tak': 3, 'Czasami': 2, 'Raczej nie': 1, 'Zupełnie nie': 0, 'Brak danych' : np.nan}
    management.replace(grade_mapping, inplace=True)
    result.replace(grade_mapping, inplace=True)
    change.replace(grade_mapping, inplace=True)
    decision.replace(grade_mapping, inplace=True)
    communication.replace(grade_mapping, inplace=True)
    #print(management)
    data = pd.concat([management, result, change, decision, communication], axis=1, join='inner')
    
    return data

def basic_statistics(data):    
    
    management = data.iloc[:,4:20]
    print(management)
    result = data.iloc[:,20:34]
    change = data.iloc[:,34:42]
    decision = data.iloc[:,42:50]
    communication = data.iloc[:,50:68]
    
    
    basic_statistics = pd.DataFrame({'Kierowanie': [np.mean(management), np.median(management), np.std(management.to_numpy())], 'Rezultat': [np.mean(result), np.median(result), np.std(result.to_numpy())],
                                     'Zmiana': [np.mean(change), np.median(change), np.std(change.to_numpy())], 'Decyzje': [np.mean(decision), np.median(decision), np.std(decision.to_numpy())],
                                     'Komunikacja': [np.mean(communication), np.median(communication), np.std(communication.to_numpy())]}, index=['Średnia', 'Mediana', 'Odchylenie standardowe'])
    return basic_statistics

def calculating_cumulative_krippendorf(data):
    #calculating cumulative krippendorf for every competence
    
    management = data.iloc[:,4:20]
    result = data.iloc[:,20:34]
    change = data.iloc[:,34:42]
    decision = data.iloc[:,42:50]
    communication = data.iloc[:,50:68]
    
    kripp_cumulative = pd.DataFrame(
        [
            (kripp.alpha(reliability_data=management, level_of_measurement='ordinal'), kripp.alpha(reliability_data=result, level_of_measurement='ordinal'), kripp.alpha(reliability_data=change, level_of_measurement='ordinal'),
            kripp.alpha(reliability_data=decision, level_of_measurement='ordinal'), kripp.alpha(reliability_data=communication, level_of_measurement='ordinal'))
        ],
        columns=['management', 'result', 'change', 'decision', 'communication']
    )
    
    return kripp_cumulative

def icc_mean_stats(data):
    #transpozing data info ICC format for every competence separately
    icc_data = data.iloc[:,4:].transpose()

    icc_data = icc_data.reset_index()

    data_judge_management = icc_data.loc[0:15].copy()
    data_judge_result = icc_data.loc[16:29].copy()
    data_judge_change = icc_data.loc[30:37].copy()
    data_judge_decision = icc_data.loc[38:45].copy()
    data_judge_communication = icc_data.loc[46:68].copy()

    #management
    data_judge1_management = data_judge_management[['index',0]]
    data_judge1_management = data_judge1_management.rename(columns = {0 : 'scores'})
    data_judge1_management['Judge'] = 'judge_1'

    data_judge2_management = data_judge_management[['index',1]]
    data_judge2_management = data_judge2_management.rename(columns = {1 : 'scores'})
    data_judge2_management['Judge'] = 'judge_2'

    data_judge3_management = data_judge_management[['index',2]]
    data_judge3_management = data_judge3_management.rename(columns = {2 : 'scores'})
    data_judge3_management['Judge'] = 'judge_3'

    data_judge4_management = data_judge_management[['index',3]]
    data_judge4_management = data_judge4_management.rename(columns = {3 : 'scores'})
    data_judge4_management['Judge'] = 'judge_4'

    icc_data_management = pd.concat([data_judge1_management, data_judge2_management, data_judge3_management, data_judge4_management])
    icc_data_management = icc_data_management.reset_index()
    icc_data_management = icc_data_management.drop('level_0', axis=1) 

    #result
    data_judge1_result = data_judge_result[['index',0]]
    data_judge1_result = data_judge1_result.rename(columns = {0 : 'scores'})
    data_judge1_result['Judge'] = 'judge_1'

    data_judge2_result = data_judge_result[['index',1]]
    data_judge2_result = data_judge2_result.rename(columns = {1 : 'scores'})
    data_judge2_result['Judge'] = 'judge_2'

    data_judge3_result = data_judge_result[['index',2]]
    data_judge3_result = data_judge3_result.rename(columns = {2 : 'scores'})
    data_judge3_result['Judge'] = 'judge_3'

    data_judge4_result = data_judge_result[['index',3]]
    data_judge4_result = data_judge4_result.rename(columns = {3 : 'scores'})
    data_judge4_result['Judge'] = 'judge_4'

    icc_data_result = pd.concat([data_judge1_result, data_judge2_result, data_judge3_result, data_judge4_result])
    icc_data_result = icc_data_result.reset_index()
    icc_data_result = icc_data_result.drop('level_0', axis=1) 

    #change
    data_judge1_change = data_judge_change[['index',0]]
    data_judge1_change = data_judge1_change.rename(columns = {0 : 'scores'})
    data_judge1_change['Judge'] = 'judge_1'

    data_judge2_change = data_judge_change[['index',1]]
    data_judge2_change = data_judge2_change.rename(columns = {1 : 'scores'})
    data_judge2_change['Judge'] = 'judge_2'

    data_judge3_change = data_judge_change[['index',2]]
    data_judge3_change = data_judge3_change.rename(columns = {2 : 'scores'})
    data_judge3_change['Judge'] = 'judge_3'

    data_judge4_change = data_judge_change[['index',3]]
    data_judge4_change = data_judge4_change.rename(columns = {3 : 'scores'})
    data_judge4_change['Judge'] = 'judge_4'

    icc_data_change = pd.concat([data_judge1_change, data_judge2_change, data_judge3_change, data_judge4_change])
    icc_data_change = icc_data_change.reset_index()
    icc_data_change = icc_data_change.drop('level_0', axis=1) 

    #decision
    data_judge1_decision = data_judge_decision[['index',0]]
    data_judge1_decision = data_judge1_decision.rename(columns = {0 : 'scores'})
    data_judge1_decision['Judge'] = 'judge_1'

    data_judge2_decision = data_judge_decision[['index',1]]
    data_judge2_decision = data_judge2_decision.rename(columns = {1 : 'scores'})
    data_judge2_decision['Judge'] = 'judge_2'

    data_judge3_decision = data_judge_decision[['index',2]]
    data_judge3_decision = data_judge3_decision.rename(columns = {2 : 'scores'})
    data_judge3_decision['Judge'] = 'judge_3'

    data_judge4_decision = data_judge_decision[['index',3]]
    data_judge4_decision = data_judge4_decision.rename(columns = {3 : 'scores'})
    data_judge4_decision['Judge'] = 'judge_4'

    icc_data_decision = pd.concat([data_judge1_decision, data_judge2_decision, data_judge3_decision, data_judge4_decision])
    icc_data_decision = icc_data_decision.reset_index()
    icc_data_decision = icc_data_decision.drop('level_0', axis=1)

    #communication
    data_judge1_communication = data_judge_communication[['index',0]]
    data_judge1_communication = data_judge1_communication.rename(columns = {0 : 'scores'})
    data_judge1_communication['Judge'] = 'judge_1'

    data_judge2_communication = data_judge_communication[['index',1]]
    data_judge2_communication = data_judge2_communication.rename(columns = {1 : 'scores'})
    data_judge2_communication['Judge'] = 'judge_2'

    data_judge3_communication = data_judge_communication[['index',2]]
    data_judge3_communication = data_judge3_communication.rename(columns = {2 : 'scores'})
    data_judge3_communication['Judge'] = 'judge_3'

    data_judge4_communication = data_judge_communication[['index',3]]
    data_judge4_communication = data_judge4_communication.rename(columns = {3 : 'scores'})
    data_judge4_communication['Judge'] = 'judge_4'

    icc_data_communication = pd.concat([data_judge1_communication, data_judge2_communication, data_judge3_communication, data_judge4_communication])
    icc_data_communication = icc_data_communication.reset_index()
    icc_data_communication = icc_data_communication.drop('level_0', axis=1)
    
    #calculating ICC for every competence
    icc_result_management = pg.intraclass_corr(data=icc_data_management, targets='index', raters='Judge', ratings='scores', nan_policy = 'omit')

    icc_result_result = pg.intraclass_corr(data=icc_data_result, targets='index', raters='Judge', ratings='scores', nan_policy = 'omit')

    icc_result_change = pg.intraclass_corr(data=icc_data_change, targets='index', raters='Judge', ratings='scores', nan_policy = 'omit')

    icc_result_decision = pg.intraclass_corr(data=icc_data_decision, targets='index', raters='Judge', ratings='scores', nan_policy = 'omit')

    icc_result_communication = pg.intraclass_corr(data=icc_data_communication, targets='index', raters='Judge', ratings='scores', nan_policy = 'omit')
    
    icc_results = [icc_result_management, icc_result_result, icc_result_change, icc_result_decision, icc_result_communication]
    
    
    
    #self ve other perception
    data_other_management = pd.concat([data_judge2_management, data_judge3_management, data_judge4_management])
    mean_self_management = np.mean(data_judge1_management[['scores']])
    mean_others_management = np.mean(data_other_management[['scores']])

    data_other_result = pd.concat([data_judge2_result, data_judge3_result, data_judge4_result])
    mean_self_result = np.mean(data_judge1_result[['scores']])
    mean_others_result = np.mean(data_other_result[['scores']])

    data_other_change = pd.concat([data_judge2_change, data_judge3_change, data_judge4_change])
    mean_self_change = np.mean(data_judge1_change[['scores']])
    mean_others_change = np.mean(data_other_change[['scores']])

    data_other_decision = pd.concat([data_judge2_decision, data_judge3_decision, data_judge4_decision])
    mean_self_decision = np.mean(data_judge1_decision[['scores']])
    mean_others_decision = np.mean(data_other_decision[['scores']])

    data_other_communication = pd.concat([data_judge2_communication, data_judge3_communication, data_judge4_communication])
    mean_self_communication = np.mean(data_judge1_communication[['scores']])
    mean_others_communication = np.mean(data_other_communication[['scores']])

    mean_statistics = pd.DataFrame({'Kierowanie - Samoocena': [mean_self_management], 'Kierowanie - Ocena innych': [mean_others_management],
                                    'Nastawienie na rezultat - Samoocena': [mean_self_result], 'Nastawienie na rezultat - Ocena innych': [mean_others_result],
                                    'Zarządzanie zmianą - Samoocena': [mean_self_change], 'Zarządzanie zmianą - Ocena innych': [mean_others_change],
                                    'Podejmowanie decyzji - Samoocena': [mean_self_decision], 'Podejmowanie decyzji - Ocena innych': [mean_others_decision],
                                    'Komunikacja - Samoocena': [mean_self_communication], 'Komunikacja - Ocena innych': [mean_others_communication],
                                    }, index=['Średnia'])
    
    #self vs other separate percaption
    mean_judge2_management = np.mean(data_judge2_management[['scores']])
    mean_judge2_result = np.mean(data_judge2_result[['scores']])
    mean_judge2_change = np.mean(data_judge2_change[['scores']])
    mean_judge2_decision = np.mean(data_judge2_decision[['scores']])
    mean_judge2_communication = np.mean(data_judge2_communication[['scores']])

    mean_judge3_management = np.mean(data_judge3_management[['scores']])
    mean_judge3_result = np.mean(data_judge3_result[['scores']])
    mean_judge3_change = np.mean(data_judge3_change[['scores']])
    mean_judge3_decision = np.mean(data_judge3_decision[['scores']])
    mean_judge3_communication = np.mean(data_judge3_communication[['scores']])

    mean_judge4_management = np.mean(data_judge4_management[['scores']])
    mean_judge4_result = np.mean(data_judge4_result[['scores']])
    mean_judge4_change = np.mean(data_judge4_change[['scores']])
    mean_judge4_decision = np.mean(data_judge4_decision[['scores']])
    mean_judge4_communication = np.mean(data_judge4_communication[['scores']])

    mean_separate_statistics = pd.DataFrame({'Kierowanie': [mean_self_management, mean_judge2_management, mean_judge3_management, mean_judge4_management],
                                    'Nastawienie na rezultat': [mean_self_result, mean_judge2_result, mean_judge3_result, mean_judge4_result],
                                    'Zarządzanie zmianą': [mean_self_change, mean_judge2_change, mean_judge3_change, mean_judge4_change],
                                    'Podejmowanie decyzji': [mean_self_decision, mean_judge2_decision, mean_judge3_decision, mean_judge4_decision],
                                    'Komunikacja': [mean_self_communication, mean_judge2_communication, mean_judge3_communication, mean_judge4_communication],
                                    }, index=['Samoocena', 'Judge1', 'Judge2', 'Judge3'])
    
    return icc_results, mean_statistics, mean_separate_statistics 

def top_bottom_five(data):
    #your top 5 and bottom 5
    sorted_mean_data = data.iloc[:,:].transpose()
    sorted_mean_data = sorted_mean_data.drop(0, axis=1)
    sorted_mean_data['mean'] = sorted_mean_data.mean(axis=1)
    sorted_mean_data = sorted_mean_data.sort_values(by=['mean'])

    top_five = sorted_mean_data.iloc[0:5].copy()
    bottom_five = sorted_mean_data.iloc[59:64].copy()
    
    return top_five, bottom_five


def biggest_gaps(data):
    biggest_gaps_data = data.iloc[:,:].transpose()
    biggest_gaps_self = biggest_gaps_data[[0]].copy()
    iggest_gaps_data = biggest_gaps_data.drop(0, axis=1)
    biggest_gaps_data['mean'] = biggest_gaps_data.mean(axis=1)
    biggest_gaps_data['0'] = biggest_gaps_self
    biggest_gaps_data['Różnica'] = biggest_gaps_data['mean'].sub(biggest_gaps_data['0'])

    biggest_gaps_data = biggest_gaps_data.sort_values(by=['Różnica'])

    top_five_diff = biggest_gaps_data.iloc[0:5].copy()
    bottom_five_diff = biggest_gaps_data.iloc[59:64].copy()
    
    return top_five_diff, bottom_five_diff


def all_items_means(data):
    #mean and score of every item
    item_mean_data = data.iloc[:,:].transpose()
    item_mean_data['mean'] = item_mean_data.mean(axis=1)    
    return item_mean_data
    
