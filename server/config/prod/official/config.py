from litestar import Router, get, Response
from server.core.utils.json import read_json
from server.constants import CONFIG_PATH, NETWORK_CONFIG_PATH, REMOTE_CONFIG_PATH, VERSION_PATH
import json
import re

@get("/network_config")
async def networkConfig() -> Response:
    server_config: dict = read_json(CONFIG_PATH)
    netconfig: dict = read_json(NETWORK_CONFIG_PATH)["networkConfig"]

    server: str = "http://" + server_config["server"]["host"] + ":" + str(server_config["server"]["port"])
    funcVer: str = netconfig["content"]["funcVer"]

    for index in netconfig["content"]["configs"][funcVer]["network"]:
        url: str = netconfig["content"]["configs"][funcVer]["network"][index]
        if isinstance(url, str) and url.find("{server}") >= 0:
            netconfig["content"]["configs"][funcVer]["network"][index] = re.sub("{server}", server, url)

    netconfig["content"] = json.dumps(netconfig["content"])
    return Response(
        content = netconfig
    )
    
    
@get("/remote_config")
async def remoteConfig() -> Response:
    remote_config: dict = read_json(REMOTE_CONFIG_PATH)["remoteConfig"]
    return Response(
        content = remote_config
    )
@get("/{platform:str}/version")
async def version(platform: str) -> Response:
    version_dict: dict = read_json(VERSION_PATH)[platform]
    return Response(
        content = version_dict
    )
