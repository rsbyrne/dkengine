from . import tools

import time
import math
# from sklearn.linear_model import LinearRegression
# import numpy as np

present_time = lambda: round(time.time())

def observe_lambda(startTime, endTime, endPerf):
    endPerf = max(1e-9, endPerf)
    t_interval = endTime - startTime
    lambdaVal = -math.log(endPerf) / t_interval
    return lambdaVal

def observe_lambda_card(history, cardID, index):
    cardHistory = history.card_histories[cardID]
    endTime, endPerf = cardHistory[index]
    startTime, startPerf = cardHistory[index - 1]
    return observe_lambda(startTime, endTime, endPerf)

def observe_lambdas_card(history, cardID):
    cardHistory = history.card_histories[cardID]
    lambdas = [
        observe_lambda_card(history, cardID, i) \
            for i in range(1, len(cardHistory))
        ]
    return lambdas

def observe_all_lambdas(history):
    cardLambdas = {}
    for cardID in history.card_histories:
        lambdaVals = observe_lambdas_card(history, cardID)
        cardLambdas[cardID] = lambdaVals
    return cardLambdas

def lambdaFn(history):
    # cardDict = tools.make_cardDict(history)
    return 1.

def predict_performance_maths(TSLE, POLE, lambdaVal):
    return POLE * math.e ** (-TSLE * lambdaVal)

def predict_performance(cardID, history):
    cardHistory = history.card_histories[cardID]
    if cardHistory is None:
        return 0
    TOLE, POLE = cardHistory[-1]
    TSLE = present_time() - TOLE
    pred_performance = predict_performance_maths(
        TSLE,
        POLE,
        lambdaFn(history)
        )
    return pred_performance

# def regress_tau_card(cardHistory, index):
#     xs = cardHi
#     regressor = LinearRegression()
#     # xs = np.array(cardHistory)[:depth, 0].reshape(depth, 1)
#     # ys = np.log(np.array(cardHistory)[:depth, 1].reshape(depth, 1))
#     regressor.fit(xs, ys)
#     coef_val = regressor.coef_[0][0]
#     if coef_val == 0.:
#         coef_val = -1e-9
#     tau_val = -1. / coef_val
#     return tau_val
#
# def regress_tau_card_recursive(cardHistory):
#     tau_vals = []
#     for i in range(1, len(cardHistory)):
#         sub_cardHistory = cardHistory[:i]
#         tau_vals.append(regress_tau_card(sub_cardHistory))
#     return tau_vals
#
# def get_observed_taus_card(cardHistory):
#     return regress_tau_card_recursive(cardHistory)
#
# def predict_past_performance(cardHistory, index, tau):
#     TOLE, POLE = cardHistory[index - 1]
#     TSLE = cardHistory[index][0] - TOLEb
#     pred_performance = predict_performance_single(TSLE, POLE, tau)
#
# def predict_past_performances(cardHistory, tauVals):
#     performances_vals = []
#     for i in range(1, len(cardHistory)):
#         performance_val = predict_past_performance(
#             cardHistory,
#             i,
#             tauVals[i]
#             )
#         performances_vals.append(performance_val)
#     return performances_vals
