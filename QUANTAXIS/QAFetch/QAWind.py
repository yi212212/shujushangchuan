# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2021 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
QAWind

QAWind is a data fetch module just for WIND Institution Version

QAWind is under the [QAStandard#0.0.2 @101-1],[QAStandard#0.0.2 @501-0] protocol

@author: yutiansut

@last modified:2017/4/5
"""
import datetime
import re
import time

import numpy as np
import pandas as pd
import pymongo

from QUANTAXIS.QAUtil import QA_util_date_valid, QA_util_log_info

from QUANTAXIS.QAFetch import data_list as data_list


def QA_fetch_get_stock_info(name, startDate, endDate):
    try:
        from WindPy import w
    except:
        QA_util_log_info('No WindPY Module!')
    w.start()
    # get the all stock list on the endDate
    # judge the vaild date
    if(QA_util_date_valid(endDate) is False):
        QA_util_log_info("wrong date")
    else:
        # tempStr='date='+endDate+";sectorid=a001010100000000"
        # data=w.wset("sectorconstituent",tempStr)
        data = w.wsd(name, "sec_name,sec_englishname,ipo_date,exch_city,mkt,\
                    sec_status,delist_date,issuecurrencycode,curr,RO,parvalue,\
                    lotsize,tunit,exch_eng,country,concept,marginornot,SHSC,\
                    parallelcode,sec_type,backdoor,backdoordate,windtype",
                     startDate, endDate)
        # QA_util_log_info(data)
        if (data.ErrorCode != 0):
            QA_util_log_info("Connect to Wind successfully")
            return data.Data


def QA_fetch_get_stock_day(name, startDate, endDate, if_fq='01'):
    try:
        from WindPy import w
    except:
        QA_util_log_info('No WindPY Module!')
    w.start()
    if(QA_util_date_valid(endDate) == False):
        QA_util_log_info("wrong date")
    else:
        if if_fq in ['00', 'bfq']:
            data = w.wsd(name, "sec_name,pre_close,open,high,low,close,volume",
                         startDate, endDate)
        elif if_fq in ['01', 'qfq']:
            data = w.wsd(name, "sec_name,pre_close,open,high,low,close,volume",
                         startDate, endDate, "PriceAdj=F")
        elif if_fq in ['02', 'hfq']:
            data = w.wsd(name, "sec_name,pre_close,open,high,low,close,volume",
                         startDate, endDate, "PriceAdj=B")
        else:
            QA_util_log_info('wrong fq factor! using qfq')
            data = w.wsd(name, "sec_name,pre_close,open,high,low,close,volume",
                         startDate, endDate, "PriceAdj=B")
        if (data.ErrorCode == 0):
            QA_util_log_info("Connect to Wind successfully")

            return pd.DataFrame(np.asarray(data.Data).T, columns=data.Fields, index=data.Times)


def QA_fetch_get_stock_day_simple(name, startDate, endDate):
    try:
        from WindPy import w
    except:
        QA_util_log_info('No WindPY Module!')
    w.start()
    if(QA_util_date_valid(endDate) == False):
        QA_util_log_info("wrong date")
    else:
        data = w.wsd(name, "sec_name,preclose,open,high,low,close,volume",
                     startDate, endDate, "Fill=Previous;PriceAdj=F")
        #data=w.wsd("000002.SZ", "open,high,low,close,volume", "2017-03-03", "2017-04-01", "PriceAdj=B")
        QA_util_log_info(data.ErrorCode)
        if (data.ErrorCode == 0):
            QA_util_log_info("Connect to Wind successfully")
            return data.Data


def QA_fetch_get_stock_indicator(name, startDate, endDate):
    try:
        from WindPy import w
    except:
        QA_util_log_info('No WindPY Module!')
    w.start()
    if(QA_util_date_valid(endDate) == False):
        QA_util_log_info("wrong date")
    else:
        # ADTM?????????????????????,ATR????????????,BBI????????????,BBIBOLL???????????????,BIAS?????????,BOLL?????????,CCI????????????,CDP????????????,DMA????????????,
        # DMI????????????,DPO???????????????,ENV,EXPMA????????????????????????,KDJ????????????,slowKD??????kd,MA??????????????????,MACD????????????????????????,MIKE????????????,
        # MTM????????????,PRICEOSC??????????????????,PVT??????????????????,RC???????????????,ROC????????????,RSI??????????????????,SAR????????????,SI????????????,SOBV?????????,
        # SRMI MI????????????,STD ?????????,TAPI ?????????????????????,TRIX ????????????????????????,VHF????????????,VMA?????????????????????,VMACD???????????????????????????,
        # VOSC???????????????,WVAD?????????????????????,vol_ratio??????
        data = w.wsd(name, "ADTM,ATR,BBI,BBIBOLL,BIAS,BOLL,CCI,CDP,\
                        DMA,DMI,DPO,ENV,EXPMA,KDJ,slowKD,MA,MACD,\
                        MIKE,MTM,PRICEOSC,PVT,RC,ROC,RSI,SAR,SI,\
                        SOBV,SRMI,STD,TAPI,TRIX,VHF,VMA,VMACD,VOSC,\
                        WVAD,vol_ratio", startDate, endDate,
                     "ADTM_N1=23;ADTM_N2=8;ADTM_IO=1;ATR_N=14;ATR_IO=1;\
                     BBI_N1=3;BBI_N2=6;BBI_N3=12;BBI_N4=24;BBIBOLL_N=10;\
                     BBIBOLL_Width=3;BBIBOLL_IO=1;BIAS_N=12;BOLL_N=26;\
                     BOLL_Width=2;BOLL_IO=1;CCI_N=14;CDP_IO=1;DMA_S=10;\
                     DMA_L=50;DMA_N=10;DMA_IO=1;DMI_N=14;DMI_N1=6;\
                     DMI_IO=1;DPO_N=20;DPO_M=6;DPO_IO=1;ENV_N=14;ENV_IO=1;\
                     EXPMA_N=12;KDJ_N=9;KDJ_M1=3;KDJ_M2=3;KDJ_IO=1;SlowKD_N1=9;\
                     SlowKD_N2=3;SlowKD_N3=3;SlowKD_N4=5;SlowKD_IO=1;MA_N=5;\
                     MACD_L=26;MACD_S=12;MACD_N=9;MACD_IO=1;MIKE_N=12;MIKE_IO=1;\
                     MTM_interDay=6;MTM_N=6;MTM_IO=1;PRICEOSC_L=26;PRICEOSC_S=12;\
                     RC_N=50;ROC_interDay=12;ROC_N=6;ROC_IO=1;RSI_N=6;SAR_N=4;\
                     SAR_SP=2;SAR_MP=20;SRMI_N=9;STD_N=26;TAPI_N=6;TAPI_IO=1;\
                     TRIX_N1=12;TRIX_N2=20;TRIX_IO=1;VHF_N=28;VMA_N=5;VMACD_S=12;\
                     VMACD_L=26;VMACD_N=9;VMACD_IO=1;VOSC_S=12;VOSC_L=26;WVAD_N1=24;\
                     WVAD_N2=6;WVAD_IO=1;VolumeRatio_N=5")
        if (data.ErrorCode == 0):
            QA_util_log_info("Connect to Wind successfully")
    return pd.DataFrame(np.asarray(data.Data).T, columns=data.Fields, index=data.Times)


def QA_fetch_get_stock_shape(name, startDate, endDate):
    try:
        from WindPy import w
    except:
        QA_util_log_info('No WindPY Module!')
    w.start()
    if(QA_util_date_valid(endDate) == False):
        QA_util_log_info("wrong date")
    else:
        # history_low?????????????????????,stage_high?????????????????????,history_high?????????????????????,stage_low?????????????????????,up_days????????????,down_days????????????,breakout_ma????????????????????????,breakdown_ma????????????????????????,bull_bear_ma??????????????????????????????
        data = w.wsd(name, "history_low,stage_high,history_high,stage_low,up_days,down_days,breakout_ma,breakdown_ma,bull_bear_ma",
                     startDate, endDate, "n=3;m=60;meanLine=60;N1=5;N2=10;N3=20;N4=30;upOrLow=1")
        if (data.ErrorCode == 0):
            QA_util_log_info("Connect to Wind successfully")
    return pd.DataFrame(np.asarray(data.Data).T, columns=data.Fields, index=data.Times)


def QA_fetch_get_stock_risk(name, startDate, endDate):
    try:
        from WindPy import w
    except:
        QA_util_log_info('No WindPY Module!')
    w.start()
    if(QA_util_date_valid(endDate) == False):
        QA_util_log_info("wrong date")
    else:
        data = w.wsd(name, "annualyeild_100w,annualyeild_24m,annualyeild_60m,\
                    annualstdevr_100w,annualstdevr_24m,annualstdevr_60m,beta_100w,\
                    beta_24m,beta_60m,avgreturn,avgreturny,stdevry,stdcof,\
                    risk_nonsysrisk1,r2,alpha2,beta,sharpe,treynor,jensen,jenseny,betadf",
                     startDate, endDate, "period=2;returnType=1;index=000001.SH;yield=1")
        if (data.ErrorCode == 0):
            QA_util_log_info("Connect to Wind successfully")
    return pd.DataFrame(np.asarray(data.Data).T, columns=data.Fields, index=data.Times)


def QA_fetch_get_stock_xueqiu(name, startDate, endDate):
    try:
        from WindPy import w
    except:
        QA_util_log_info('No WindPY Module!')
    w.start()
    if(QA_util_date_valid(endDate) == False):
        QA_util_log_info("wrong date")
    else:
        data = w.wsd(name, "xq_accmfocus,xq_accmcomments,xq_accmshares,\
                    xq_focusadded,xq_commentsadded,xq_sharesadded,\
                    xq_WOW_focus,xq_WOW_comments,xq_WOW_shares", startDate, endDate, "")
        if (data.ErrorCode == 0):
            QA_util_log_info("Connect to Wind successfully")
    return pd.DataFrame(np.asarray(data.Data).T, columns=data.Fields, index=data.Times)


def QA_fetch_get_stock_financial(name, startDate, endDate):
    try:
        from WindPy import w
    except:
        QA_util_log_info('No WindPY Module!')
    w.start()
    pass


def QA_fetch_get_trade_date(endDate, exchange):
    try:
        from WindPy import w
    except:
        QA_util_log_info('No WindPY Module!')
    w.start()
    supportExchanges = ["SSE", "SZSE", "CFFEX", "SHFE", "DCE", "CZCE"]
    if (exchange in supportExchanges):
        #"SSE","SZSE","CFFEX","SHFE","DCE","CZCE"
        # ?????????????????????,?????????????????????,???????????????????????????,?????????????????????,?????????????????????,?????????????????????
        exchanges = "TradingCalendar=" + exchange
        data = w.tdays("1990-01-01", endDate, exchanges)
        # QA_util_log_info(data.Data)
        dates = pd.DataFrame(np.asarray(data.Data).T,
                             columns=data.Fields, index=data.Times)
    else:
        QA_util_log_info("exchange name problem")
    return dates


def QA_fetch_get_stock_list(date):
    try:
        from WindPy import w
    except:
        QA_util_log_info('No WindPY Module!')
    w.start()
    if(QA_util_date_valid(date) == False):
        QA_util_log_info("wrong date")
    else:
        awgs = 'date=' + date + ';sectorid=a001010100000000'
        data = w.wset("sectorconstituent", awgs)
        return pd.DataFrame(np.asarray(data.Data).T, columns=data.Fields, index=data.Times)


def QA_fetch_get_stock_list_special(date, id):
    try:
        from WindPy import w
    except:
        QA_util_log_info('No WindPY Module!')
    w.start()
    if(QA_util_date_valid(date) == False):
        QA_util_log_info("wrong date")
    else:
        if id in ['big', 'small', 'cixin', 'yujing', 'rzrq', 'rq', 'yj', 'st', 'sst']:
            awgs = 'date=' + date + ';sectorid=' + \
                data_list.wind_stock_list_special_id[id]
            data = w.wset("sectorconstituent", awgs)
            return pd.DataFrame(np.asarray(data.Data).T, columns=data.Fields, index=data.Times)
