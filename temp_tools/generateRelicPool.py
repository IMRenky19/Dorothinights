

ROGUELIKE_TOPIC_EXCEL_PATH = "D:\\Dorothinights\\excel\\roguelike_topic_table.json"
ROGUELIKE_RELIC_POOL_PATH = "D:\\Dorothinights\\config\\rlv2RelicPools.json"
import json

def read_json(filepath: str, **args) -> dict:
    with open(filepath, **args, encoding="utf-8") as f:
        return json.load(f)


def write_json(data: dict, filepath: str) -> None:
    with open(filepath, 'w', encoding="utf-8") as f:
        json.dump(data, f, sort_keys=False, indent=4, ensure_ascii=False)
        
        

rogueTable = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)["details"]["rogue_3"]["items"]
beforeProcessingRelicPool = read_json(ROGUELIKE_RELIC_POOL_PATH)

legacyRelic = []
resRelic = []
fightRelic = []
book = []
hand = []
bossRelic = []
curseRelic = []
others = []

relic_4 = []
relic_8 = []
relic_12 = []
relic_16 = []
relic_special = []

for name, details in rogueTable.items():
    match name:
        case name if name.find("legacy") != -1:
            legacyRelic.append(name)
        case name if name.find("res") != -1:
            resRelic.append(name)
        case name if name.find("fight") != -1:
            fightRelic.append(name)
        case name if name.find("book") != -1:
            book.append(name)
        case name if name.find("hand") != -1:
            hand.append(name)
        case name if name.find("curse") != -1:
            curseRelic.append(name)
        case name if name.find("boss") != -1:
            bossRelic.append(name)
        case _:
            others.append(name)
    match details["value"]:
        case 4:
            relic_4.append(name)
        case 8:
            relic_8.append(name)
        case 12:
            relic_12.append(name)
        case 16:
            relic_16.append(name)
        case 1:
            relic_special.append(name)
write_json(
    {
        "legacyRelic": legacyRelic,
        "resRelic": resRelic,
        "fightRelic": fightRelic,
        "book": book,
        "hand": hand,
        "bossRelic": bossRelic,
        "curseRelic": curseRelic,
        "others": others,
        "1": relic_special,
        "4": relic_4,
        "8": relic_8,
        "12": relic_12,
        "16": relic_16,
        
    },
    "D:\\tmp.json"
)

relicAll = [name for name in rogueTable.keys() if name.find("relic") != -1 or name.find("active_tool") != -1]
finals = {}
for name,i in beforeProcessingRelicPool["rogue_3"].items():
    finals[f"{name}"] = []
    if i["mode"] == "blackList":
        for item2 in relicAll:
            if not(item2 in i["pool"]):
                finals[f"{name}"].append(item2)
    else:
        finals[f"{name}"] = i["pool"]
write_json({
        "rogue_3": finals
}, "D:\\finals.json")