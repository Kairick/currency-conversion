import uvicorn

from settings import server_settings

if __name__ == '__main__':
    uvicorn.run(
        "src.application:app",
        host=server_settings.server_host,
        port=server_settings.server_port,
        reload=True
    )
