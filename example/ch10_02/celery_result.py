from celery.result import AsyncResult
from common.messaging import celery

if __name__=="__main__":
    async_result = AsyncResult("c2368172-6f68-4e07-99b4-5fe8ee54dd1a", app=celery)
    result = async_result.result
    
    print(result)