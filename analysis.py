from . import tools

import time
import math
# from sklearn.linear_model import LinearRegression
# import numpy as np

present_time = lambda: round(time.time())

def observe_tau_card(history, cardID, index):
    cardHistory = history.cardHistories[cardID]
    endTime, endPerf = cardHistory[index]
    startTime, startPerf = cardHistory[index - 1]
    t = endTime - startTime
    if endPerf >= startPerf:
        return None
    decayRatio = startPerf / endPerf
    tau = t / math.log(decayRatio)
    return tau

def observe_taus_card(history, cardID):
    cardHistory = history.cardHistories[cardID]
    taus = [
        observe_tau_card(history, cardID, i) \
            for i in range(1, len(cardHistory))
        ]
    return taus

def tauFn(history):
    # cardDict = tools.make_cardDict(history)
    return 1e9

def predict_performance_maths(TSLE, POLE, tau):
    return POLE * math.e ** (-TSLE / tau)

def predict_performance(cardID, history):
    cardHistory = history.cardHistories[cardID]
    if cardHistory is None:
        return 0
    TOLE, POLE = cardHistory[-1]
    TSLE = present_time() - TOLE
    pred_performance = predict_performance_maths(
        TSLE,
        POLE,
        tauFn(history)
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
