import pandas as pd
import time


def measure(submission, label_path=None):
    if not label_path:
        label_path = "../datasets/Y_Moniter_labelled_data"
    data = pd.read_csv(label_path)
    result = pd.read_csv(submission)
    if len(result) > 0:
        data_1 = data[(data.label == 1)]
#         print(type(data_1))
        TP, FP, FN = 0, 0, 0
        for index, i in result.iterrows():
            temp = (data_1["left_spec_id"].isin([i.left_spec_id]) & data_1['right_spec_id'].isin([i.right_spec_id])) | (
                data_1["right_spec_id"].isin([i.left_spec_id]) & data_1['left_spec_id'].isin([i.right_spec_id]))
#             print(type(temp.values) )
#             print(temp.values.sum()>0)
#             print(temp.values.dtype)
            if temp.values.sum() > 0:
                TP += 1
            else:
                FP += 1
        P = TP / len(result)
        R = TP / len(data_1)
        if P + R == 0:
            f1_measure = 0
        else:
            f1_measure = 2 * P * R / (P + R)
        print("precision:%.5f   recall:%.5f  f1_measure: %.5f" %
              (P, R, f1_measure))
        return (P, R, f1_measure)
    else:
        return (0, 0, 0)


if __name__ == '__main__':
	#start = time.time()
    measure("submission.csv",label_path='../datasets/Y_Notebook_labelled_data.csv')
    #print(time.time()-start)
