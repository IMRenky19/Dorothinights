from litestar import Router, get, Response

@get("/config")
async def config() -> Response:
    return Response(
        content = {
            "data":{
                "antiAddiction":{
                    "minorPeriodEnd":21,"minorPeriodStart":20
                },
                "payment":[
                    {
                        "key":"alipay",
                        "recommend":True
                    },
                    {
                        "key":"wechat",
                        "recommend":False
                    },
                    {
                        "key":"pcredit",
                        "recommend":False
                    }
                ],
                "customerServiceUrl":"https://chat.hypergryph.com/chat/h5/v2/index.html?sysnum=889ee281e3564ddf883942fe85764d44\u0026channelid=2",
                "cancelDeactivateUrl":"https://user.hypergryph.com/cancellation",
                "agreementUrl":{
                    "game":"https://user.hypergryph.com/protocol/plain/ak/index",
                    "unbind":"https://user.hypergryph.com/protocol/plain/ak/cancellation",
                    "gameService":"https://user.hypergryph.com/protocol/plain/ak/service",
                    "account":"https://user.hypergryph.com/protocol/plain/index",
                    "privacy":"https://user.hypergryph.com/protocol/plain/privacy",
                    "register":"https://user.hypergryph.com/protocol/plain/registration",
                    "updateOverview":"https://user.hypergryph.com/protocol/plain/overview_of_changes",
                    "childrenPrivacy":"https://user.hypergryph.com/protocol/plain/children_privacy"
                },
                "app":{
                    "enablePayment":True,
                    "enableAutoLogin":False,
                    "enableAuthenticate":True,
                    "enableAntiAddiction":True,
                    "wechatAppId":"wx0ae7fb63d830f7c1",
                    "alipayAppId":"2018091261385264",
                    "oneLoginAppId":"7af226e84f13f17bd256eca8e1e61b5a",
                    "enablePaidApp":False,
                    "appName":"明日方舟",
                    "appAmount":600,
                    "needShowName":False,
                    "customerServiceUrl":"https://customer-service.hypergryph.com/ak?hg_token={hg_token}\u0026source_from=sdk",
                    "needAntiAddictionAlert":True
                },
                "scanUrl":{
                    "login":"yj://scan_login"
                },
                "userCenterUrl":"https://user.hypergryph.com/pcSdk/userInfo"
            },
            "msg":"OK",
            "status":0,
            "type":"A"
        }
    )
    
