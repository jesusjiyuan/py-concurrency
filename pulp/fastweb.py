from fastapi import FastAPI,Request,Header,Depends
from fastapi.exceptions import HTTPException
from typing import Optional
import lp
from param import BaseReq
from common import resp,error_code
import time

def verify_token(request: Request):
    token = request.headers.get("token")
    if token == None or token != "fUgfzz3nK3pQrTPeSv":
        raise HTTPException(status_code=401, detail="Token 无效")

app = FastAPI(dependencies=[Depends(verify_token)])


# 在异常中间件 拦截，相当于 重写
@app.exception_handler(HTTPException)
async def http_exception_v1(request: Request, exc: HTTPException):
    """
    # 改变成字符串响应
    :param request: 不可省略
    :param exc: HTTPException
    :return:
    """
    return resp.respErrorJson(error = error_code.AUTH_ERROR ,msg=str(exc.detail))

@app.exception_handler(Exception)
async def http_exception_v1(request: Request, exc: Exception):
    """
    # 改变成字符串响应
    :param request: 不可省略
    :param exc: Exception
    :return:
    """
    return resp.respErrorJson(error = error_code.SYSTEM_ERROR ,msg=error_code.SYSTEM_ERROR.msg)


# 为app增加接口处理耗时的响应头信息
#@app.middleware("http")
#async def handler_token(request: Request, call_next):
#    token = request.headers.get('token')
#    if token == None:
#        return 401
#    start_time = time.time()
#    response = await call_next(request)
#    process_time = time.time() - start_time
#
#    # X- 作为前缀代表专有自定义请求头
#    response.headers["X-Process-Time"] = str(process_time)
#    response
#    return response

@app.get("/")
async def index():
    return {"message":"Hello world!"}

@app.get("/ombrun")
async def index():
    start_time = time.time()
    result = lp.make_solve()
    print(f"ombrun cost time: ",(time.time()-start_time))
    if result == 0:
        return resp.respSuccessJson('',msg='success')
    else:
        return resp.respErrorJson(error=error_code.SYSTEM_ERROR,msg="没有可行解")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return resp.respSuccessJson({"item_id": item_id, "q": q})

@app.post("/items/{item_id}")
def update_item(item_id: int, item: BaseReq.Item):
    return {"item_name": item.name, "item_id": item_id}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='fastweb:app',port=8011,reload=True)
    #uvicorn.run(app, host="127.0.0.1", port=8001, reload=True, debug=True)

#uvicorn.exe fastweb:app --reload