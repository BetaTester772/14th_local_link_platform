from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from functions import *
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd


class Search(BaseModel):
    data: str


class SearchInfo(BaseModel):
    data1: str
    data2: str


app = FastAPI()


@app.get('/paperList')
async def paper_list(search: Search):
    retL = list()
    if search.data == 'AC': retL = outputTitle()[0]
    elif search.data == 'ME': retL = outputTitle()[1]
    elif search.data == 'DE': retL = outputTitle()[2]
    return retL


@app.get('/paperInfo')
async def paper_info(search: SearchInfo):
    retL = list()
    index = 3
    data1 = search.data1
    data2 = search.data2
    if data1 == 'AC': index = 0
    elif data1 == 'ME': index = 1
    elif data1 == 'DE': index = 2
    if index < 3:
        # tempS = search.data2.split(' ')
        info = outputInfo()[index]
        for paper in info:
            if (data2 in paper['titleK'] or data2 in paper['titleE'] or
                data2 in paper['author'] or data2 in paper['abstract'] or data2 in paper['id']):
                retL.append(paper)
    return retL


@app.post('/stream')
async def stream(search: Search):
    info = outputInfo()[1]
    data = search.data
    videoID = False
    for paper in info:
        if (data in paper['titleK'] or data in paper['titleE'] or
            data in paper['author'] or data in paper['abstract'] or data in paper['id']):
            videoID = str(paper['id'])
    if videoID: return StreamingResponse(video(videoID + '.mp4'), media_type="video/mp4")
    else: return {'e': '영상이 읎으용'}