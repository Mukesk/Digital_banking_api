import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="API Gateway")

SERVICE_MAP = {
    '/auth':         'http://auth:8001',
    '/accounts':     'http://account:8002',
    '/transactions': 'http://transaction:8003',
    '/loans':        'http://loan:8004',
    '/admin':        'http://reporting:8005',
}

@app.api_route('/{path:path}', methods=['GET','POST','PUT','DELETE', 'PATCH'])
async def proxy(path: str, request: Request):
    if not path.startswith('/'):
        path = '/' + path
    
    # Extract the prefix to route to the correct service
    parts = path.split('/')
    prefix = '/' + parts[1] if len(parts) > 1 else '/'
    
    # Handle /admin/reports exactly as requested in routing table
    if prefix == '/admin':
        base = SERVICE_MAP.get('/admin')
    else:
        base = SERVICE_MAP.get(prefix)

    if not base:
        return JSONResponse(status_code=404, content={"message": "Not Found"})

    # Forward the request
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(
                method=request.method,
                url=f'{base}{path}',
                headers=dict(request.headers),
                content=await request.body()
            )
            return JSONResponse(status_code=resp.status_code, content=resp.json() if resp.content else None)
        except httpx.RequestError as exc:
            return JSONResponse(status_code=502, content={"message": "Bad Gateway", "details": str(exc)})
