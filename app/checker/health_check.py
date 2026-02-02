import httpx
import time
from typing import Dict, Any
from app.models import Service


async def check_single_service(service: Service) -> Dict[str, Any]:
    result = {
        "status": "DOWN",
        "response_time": 0.0,
        "status_code": None,
        "error_message": None
    }
    start_time = time.perf_counter()

    
    try:

        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(service.url)
            result["status_code"] = response.status_code


            if response.status_code in [200, 301, 302]:
                result["status"] = "UP"
                result["error_message"] = None  
            else:
                result["status"] = "DOWN"
                result["error_message"] = f"Неожиданный код состояния: {response.status_code}"
                
    except Exception as e:
            result["status"] = "DOWN"
            result["error_message"] = str(e)
    
    finally:
        end_time = time.perf_counter()
        duration_ms = (end_time - start_time) * 1000
        result["response_time"] = round(duration_ms, 2)
    
    return result