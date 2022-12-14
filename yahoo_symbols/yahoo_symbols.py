#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   yahoo_symbols.py
@Time    :   2022/08/18 20:28:24
@Author  :   Volker Lorrmann
@Version :   0.1
@Contact :   volker.lorrmann@gmail.com
@License :   (C)Copyright 2020-2022, Volker Lorrmann
@Desc    :   None
"""


import pandas as pd
from string import ascii_lowercase, digits
from itertools import product

from async_requests import async_requests, requests


class YahooSymbols:
    URL = "https://query1.finance.yahoo.com/v1/finance/lookup"

    async def search(
        self, query: str | list, type_: str | list, *args, **kwargs
    ) -> pd.DataFrame:
        async def parse_func(key, response):
            res = pd.DataFrame(response["finance"]["result"][0]["documents"])
            res["query"] = key
            return res

        if isinstance(query, str):
            query = [query]
        if isinstance(type_, list):
            type_ = ",".join(type_)

        params = [
            dict(
                formatted="false",
                query=query_,
                type=type_,
                count=10000,
                start=0,
            )
            for query_ in query
        ]

        res = await async_requests(
            url=self.URL,
            params=params,
            key=query,
            parse_func=parse_func,
            *args,
            **kwargs
        )
        if isinstance(res, list):
            res = pd.concat(res, ignore_index=True)
        return res

    async def lookup(
        self, query_length: int = 2, type_: str | list = "equity", *args, **kwargs
    ):

        letters = list(ascii_lowercase)
        numbers = list(digits)
        samples = letters + numbers + [".", "-"]

        queries = [
            "".join(q) for q in list(product(*[samples for n in range(query_length)]))
        ]
        res = await self.search(query=queries, type_=type_, *args, **kwargs)

        if isinstance(res, list):
            res = pd.concat(res)
        return res


def validate(symbol: str | list, max_symbols=1000, **kwargs):
    """Validation of the given symbols. True means the given symbol is a valid
    symbol in the yahoo finance database.

    Args:
        symbol (str | list): symbol
        max_symbols (int, optional): number if symbols included into one request. Defaults to 1000.
    """

    async def parse_json(json):
        return pd.Series(json["symbolsValidation"]["result"][0])

    if isinstance(symbol, str):
        symbol = [symbol]

    url = "https://query2.finance.yahoo.com/v6/finance/quote/validate"
    symbol_ = [
        symbol[i * max_symbols : (i + 1) * max_symbols]
        for i in range(len(symbol) // max_symbols + 1)
    ]
    params = [{"symbols": ",".join(s)} for s in symbol_]

    res = pd.concat(
        requests(url=url, params=params, parse_func=parse_json, **kwargs)
    ).rename("valid")
    res.index.names = ["symbol"]
    
    return res
