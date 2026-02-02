import pytest
import httpx
from app.checker.health_check import check_single_service
from app.models import Service

@pytest.mark.asyncio
async def test_check_single_service_success(respx_mock):
    url = "https://example.com"
    mock_service = Service(name="Test", url=url)
    
    respx_mock.get(url).mock(return_value=httpx.Response(200))
    
    result = await check_single_service(mock_service)
    
    assert result["status"] == "UP"  
    assert result["status_code"] == 200
