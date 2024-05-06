import sqlite3
import pandas as pd
import numpy as np
import ast
import re
import scipy.io as sio

conn = sqlite3.connect('db.sqlite3')
strategy_name = "CONSENSUS"
def convert_to_array(string_value):
    string_value = string_value[1:-1]
    try:
        return np.array(np.float32(ast.literal_eval(string_value)))
    except (ValueError, SyntaxError):
        return None  # Handle invalid string formats gracefully
def convert_to_mse_array(string_val):
    string_val = string_val[1:-1]
    try:
        unescaped_strings = re.sub(r'\\"', r'"', string_val)
        x =  ast.literal_eval(unescaped_strings)[1:]
        x = [ele['mse'] for ele in x]
        return x
    except (ValueError, SyntaxError):
        return None  # Handle invalid string formats gracefully

def find_last_strategy_pid(strategy):
    global conn
    p_id_query = "SELECT p_id FROM stream_process WHERE strategy='{}'".format(strategy)
    df = pd.read_sql_query(p_id_query, conn)
    # print(df, df.iloc[-1])
    return df.iloc[-1, 0]



req_p_id = find_last_strategy_pid(strategy_name)
process_id_query = "SELECT id FROM stream_process WHERE p_id='{}'".format("mJpTC9xwN2")
# print(process_id_query,pd.read_sql_query(process_id_query, conn))
df_p_id = pd.read_sql_query(process_id_query, conn)['id'].iloc[0]
export_data = {}
max_iter = 50

device_id_array = []


for it in range(6):
    device_id_q = "SELECT id FROM stream_device WHERE process_id = {} AND device_id = 'picow_{}'".format(df_p_id, it)
    df = pd.read_sql_query(device_id_q, conn)
    device_id_array.append(df.iloc[0, 0])

weights_final = None
export_data['iter_1'] = {} 
for _it in range(1, max_iter+1):
    #since we cant oreder by device id, we need to get the node index
    df = None
    for d_id in device_id_array:
        sql_query = "SELECT * FROM stream_measurement WHERE process_id={} AND iteration={} AND device_id = {}".format(df_p_id, _it, d_id)
        df_new = pd.read_sql_query(sql_query, conn)
        if df is None:
            df = df_new
        else:
            df = pd.concat([df, df_new])
    index = "iter_{}".format(_it)
    index_next = "iter_{}".format(_it+1)
    
    export_data[index]['high_cost_data'] = np.array(df['high_cost_data'], ndmin=2).T
    export_data[index]['low_cost_data'] = np.stack(df['low_cost_data'].apply(convert_to_array))
    export_data[index_next] = {} 
    export_data[index_next]['weights'] = np.stack(df['w_iter'].apply(convert_to_array))
    weights_final = np.stack(df['w_iter'].apply(convert_to_array))
export_data["iter_1"]["weights"] = np.zeros((6, 3))
print(export_data)
sql_query_con_mse = "SELECT * FROM stream_consolidatedMSE WHERE process_id={}".format(df_p_id)
df2 = pd.read_sql_query(sql_query_con_mse, conn)
# print(np.stack(df['low_cost_data'].apply(convert_to_array)))
# print(np.stack(df['high_cost_data']))
# mse_array_data = df2["mse_array"].apply(convert_to_mse_array)
# mse_average = [0]*max_iter
# for it in range(6):
#     for _it in range(max_iter):
#         mse_average[_it] = mse_average[_it] + mse_array_data[it][_it]
#         if it == 5:
#             mse_average[_it] = mse_average[_it] / 6
# # print(export_data)
# export_data['mse'] = np.array(mse_average, ndmin=2).T
sio.savemat('./testing/noise/con_test_0.mat', export_data)
# np.savetxt("matrix_cta.csv", weights_final.T, delimiter=',')