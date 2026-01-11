#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API JSON Generator for Kenkoku Server
Generates NPC and Lottery JSON files from items.json and server info.
"""

import json
import os

# File paths
ITEMS_JSON_PATH = '/Users/fur-dev/my-system/sub-github/momo-git/workspace/projects/minecraft/kenkoku-2025winter/items.json'
OUTPUT_DIR = '/Users/fur-dev/my-system/sub-github/momo-git/workspace/projects/minecraft/kenkoku-2025winter/json_data'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load item mappings from items.json
print("Loading items.json...")
with open(ITEMS_JSON_PATH, 'r', encoding='utf-8') as f:
    items_data = json.load(f)

# Build lookup dictionaries
# key_to_id: minecraft:id -> db_id (for non-original items)
# name_to_id: original item name -> db_id (for original items)
key_to_id = {}
name_to_id = {}
all_items = {}

for item in items_data:
    db_id = item['id']
    key = item.get('key', '')
    name = item.get('name')
    is_original = item.get('is_original', 0)
    
    all_items[db_id] = item
    
    # For non-original items, map the key
    if is_original == 0:
        if key and key not in key_to_id:
            key_to_id[key] = db_id
    
    # For original items, map by name
    if name:
        name_to_id[name] = db_id

print(f"Loaded {len(items_data)} items total")
print(f"  - {len(key_to_id)} unique vanilla item keys")
print(f"  - {len(name_to_id)} named original items")

# Helper function to get ID by minecraft key
def get_id_by_key(mc_key):
    if not mc_key:
        return None
    if mc_key in key_to_id:
        return key_to_id[mc_key]
    # Try with minecraft: prefix
    if not mc_key.startswith('minecraft:'):
        full_key = 'minecraft:' + mc_key
        if full_key in key_to_id:
            return key_to_id[full_key]
    print(f"  WARNING: Key not found: {mc_key}")
    return None

# Helper function to get ID by original item name
def get_id_by_name(name):
    if name in name_to_id:
        return name_to_id[name]
    print(f"  WARNING: Original item name not found: {name}")
    return None

# Placeholder IDs
BIOME_ID = 1
PROFESSION_ID = 1

# Get specific item IDs we need
PAPER_ID = get_id_by_key("minecraft:paper")  # For tickets

# ============================================================
# 2. Define Data based on info.md / server_info.html
# ============================================================

# --- Buy Prices (買取価格) -> NPC Type 1 (Pawnshop) ---
buy_prices_categories = [
    {
        "category": "買取屋(鉱石)",
        "items": [
            {"name": "原銅ブロック", "key": "minecraft:raw_copper_block", "price": 10},
            {"name": "原金ブロック", "key": "minecraft:raw_gold_block", "price": 300},
            {"name": "ダイヤ", "key": "minecraft:diamond", "price": 1000},
            {"name": "レッドストーンブロック", "key": "minecraft:redstone_block", "price": 100},
            {"name": "ラピスラズリブロック", "key": "minecraft:lapis_block", "price": 100},
            {"name": "ネザーラック", "key": "minecraft:netherrack", "price": 1},
            {"name": "丸石", "key": "minecraft:cobblestone", "price": 1},
            {"name": "荒れた深層岩", "key": "minecraft:cobbled_deepslate", "price": 1},
        ]
    },
    {
        "category": "買取屋(農作物)",
        "items": [
            {"name": "人参", "key": "minecraft:carrot", "price": 2},
            {"name": "じゃがいも", "key": "minecraft:potato", "price": 2},
            {"name": "俵", "key": "minecraft:hay_block", "price": 100},
            {"name": "ビートルート", "key": "minecraft:beetroot", "price": 10},
            {"name": "青い目のジャガイモ", "key": "minecraft:poisonous_potato", "price": 100},
        ]
    },
    {
        "category": "買取屋(水産物)",
        "items": [
            {"name": "タラ", "key": "minecraft:cod", "price": 10},
            {"name": "鮭", "key": "minecraft:salmon", "price": 10},
            {"name": "フグ", "key": "minecraft:pufferfish", "price": 50},
            {"name": "熱帯魚", "key": "minecraft:tropical_fish", "price": 50},
        ]
    },
    {
        "category": "買取屋(レア)",
        "items": [
            {"name": "エンチャント金リンゴ", "key": "minecraft:enchanted_golden_apple", "price": 30000},
            {"name": "海の心", "key": "minecraft:heart_of_the_sea", "price": 10000},
        ]
    }
]

# --- Shops (ショップ) -> NPC Type 2 (Shop) ---
shops = [
    {
        "name": "雑貨屋",
        "items": [
            {"name": "シュルカーボックス", "key": "minecraft:shulker_box", "price": 100000, "quantity": 1},
            {"name": "バンドル", "key": "minecraft:bundle", "price": 500, "quantity": 1},
            {"name": "額縁", "key": "minecraft:item_frame", "price": 100, "quantity": 1},
            {"name": "蝋燭(白)", "key": "minecraft:white_candle", "price": 100, "quantity": 1},
            {"name": "ランタン", "key": "minecraft:lantern", "price": 100, "quantity": 1},
        ]
    },
    {
        "name": "武器・防具屋",
        "items": [
            # 弓 (耐久Ⅲ) -> original item "unbreakingBow"
            {"name": "弓 (耐久Ⅲ)", "original_name": "unbreakingBow", "price": 1000, "quantity": 1},
            {"name": "矢 ×64", "key": "minecraft:arrow", "price": 500, "quantity": 64},
            {"name": "トライデント", "key": "minecraft:trident", "price": 5000, "quantity": 1},
            {"name": "メイス", "key": "minecraft:mace", "price": 50000, "quantity": 1},
        ]
    },
    {
        "name": "本屋",
        "items": [
            # エンチャ本 (耐久Ⅲ)
            {"name": "エンチャ本 (耐久Ⅲ)", "original_name": "unbreaking", "price": 5000, "quantity": 1},
            # エンチャ本 (鋭さV)
            {"name": "エンチャ本 (鋭さV)", "original_name": "sharpness", "price": 5000, "quantity": 1},
            # エンチャ本 (幸運Ⅲ)
            {"name": "エンチャ本 (幸運Ⅲ)", "original_name": "fortune", "price": 10000, "quantity": 1},
            # エンチャ本 (効率強化V)
            {"name": "エンチャ本 (効率強化V)", "original_name": "efficiency", "price": 10000, "quantity": 1},
        ]
    },
    {
        "name": "海晶屋",
        "items": [
            {"name": "海晶ブロック ×64", "key": "minecraft:prismarine", "price": 3000, "quantity": 64},
            {"name": "暗海晶ブロック ×64", "key": "minecraft:dark_prismarine", "price": 3000, "quantity": 64},
            {"name": "シーランタン ×1", "key": "minecraft:sea_lantern", "price": 1000, "quantity": 1},
        ]
    },
    {
        "name": "ツールチケット交換所",
        "description": "ツールチケットで１つと交換",
        "items": [
            # 幸運ダイヤピッケル (幸運Ⅳ、耐久Ⅲ) -> luckPick
            {"name": "幸運ダイヤピッケル", "original_name": "luckPick", "ticket_cost": 1},
            # 効率強化ダイヤピッケル (耐久V、効率強化Ⅵ) -> efficiencyPick
            {"name": "効率強化ダイヤピッケル", "original_name": "efficiencyPick", "ticket_cost": 1},
            # 効率強化ダイヤ斧 (耐久V、効率強化Ⅵ) -> efficiencyAxe
            {"name": "効率強化ダイヤ斧", "original_name": "efficiencyAxe", "ticket_cost": 1},
            # 効率強化ダイヤシャベル (耐久V、効率強化Ⅵ) -> efficiencyShovel
            {"name": "効率強化ダイヤシャベル", "original_name": "efficiencyShovel", "ticket_cost": 1},
        ]
    },
    {
        "name": "武器チケット交換所",
        "description": "武器チケットで1つと交換",
        "items": [
            # ダイヤ剣 (耐久Ⅲ、虫特効Ⅵ) -> baneOfArthropodsSword
            {"name": "ダイヤ剣 (虫特効Ⅵ)", "original_name": "baneOfArthropodsSword", "ticket_cost": 1},
            # ダイヤ剣 (耐久Ⅲ、アンデット特効Ⅵ) -> smiteSword
            {"name": "ダイヤ剣 (アンデット特効Ⅵ)", "original_name": "smiteSword", "ticket_cost": 1},
            # ダイヤ剣 (耐久Ⅲ、ノックバックX) -> knockbackSword
            {"name": "ダイヤ剣 (ノックバックX)", "original_name": "knockbackSword", "ticket_cost": 1},
            # 弓 (耐久Ⅲ、無限、修繕、ノックバックX) -> knockbackBow
            {"name": "弓 (ノックバックX)", "original_name": "knockbackBow", "ticket_cost": 1},
        ]
    }
]

# --- Armor Exchange Shops (防具交換所) ---
# Separate definition for new JSON output
armor_shops = [
    {
        "name": "防具交換所 (無制限)",
        "description": "防具チケット枚で交換",
        "items": [
            # ショップ形式（何度でも可）：防具チケット1枚と交換
            {"name": "ダイヤのヘルメット(水中呼吸 III)", "original_name": "ダイヤのヘルメット(水中呼吸 III)", "cost_original": "防具チケット"},
            {"name": "ダイヤのヘルメット(水中呼吸 I)", "original_name": "ダイヤのヘルメット(水中呼吸 I)", "cost_original": "防具チケット"},
            {"name": "ダイヤのブーツ(水中歩行 III)", "original_name": "ダイヤのブーツ(水中歩行 III)", "cost_original": "防具チケット"},
        ]
    }
]

# --- Restaurant Shops (お食事処) ---
# Separate definition for food JSON output
restaurant_shops = [
    {
        "name": "お食事処",
        "description": "お食事券1枚と交換",
        "items": [
            # ショップ形式（何度でも可）：お食事券1枚と交換
            {"name": "鉱夫じゃがいも", "original_name": "鉱夫じゃがいも", "cost_original": "お食事券"},
            {"name": "爆速スープ", "original_name": "爆速スープ", "cost_original": "お食事券"},
            {"name": "マグマパイ", "original_name": "マグマパイ", "cost_original": "お食事券"},
        ]
    }
]


# --- Vanilla Quest Patches (バニラクエスト追加分) ---
# Separate definition for patch JSON output
vanilla_quest_patches = [
    {
        "id": 1,
        "difficulty": "★ (初級)",
        "list": [
            {"name": "ケーキ", "req_key": "minecraft:cake", "req_amount": 1, "reward_lottery_tickets": 1},
            {"name": "ビートルート", "req_key": "minecraft:beetroot", "req_amount": 16, "reward_lottery_tickets": 1},
            {"name": "パンプキンパイ", "req_key": "minecraft:pumpkin_pie", "req_amount": 1, "reward_lottery_tickets": 1},
            {"name": "クッキー", "req_key": "minecraft:cookie", "req_amount": 16, "reward_lottery_tickets": 1},
        ]
    },
    {
        "id": 2,
        "difficulty": "★★ (中級)",
        "list": [
            {"name": "熱帯魚", "req_key": "minecraft:tropical_fish", "req_amount": 16, "reward_lottery_tickets": 2},
            {"name": "鱈", "req_key": "minecraft:cod", "req_amount": 64, "reward_lottery_tickets": 2},
            {"name": "鮭", "req_key": "minecraft:salmon", "req_amount": 64, "reward_lottery_tickets": 2},
            {"name": "うさぎの皮", "req_key": "minecraft:rabbit_hide", "req_amount": 4, "reward_lottery_tickets": 2},
            {"name": "青緑の染料", "req_key": "minecraft:cyan_dye", "req_amount": 16, "reward_lottery_tickets": 2},
        ]
    },
    {
        "id": 3,
        "difficulty": "★★★ (上級)",
        "list": [
            {"name": "古代の残骸", "req_key": "minecraft:ancient_debris", "req_amount": 1, "reward_lottery_tickets": 3},
            {"name": "エンドクリスタル", "req_key": "minecraft:end_crystal", "req_amount": 1, "reward_lottery_tickets": 3},
        ]
    }
]

# --- Quests (クエスト) -> NPC Type 3 (Quest) ---
quests = [
    {
        "difficulty": "★ (初級)",
        "list": [
            {"name": "街のお掃除", "req_key": "minecraft:oak_leaves", "req_amount": 64, "reward_lottery_tickets": 1},
            {"name": "珍味？", "req_key": "minecraft:golden_apple", "req_amount": 1, "reward_lottery_tickets": 1},
            {"name": "ダイヤ発見記念", "req_key": "minecraft:diamond", "req_amount": 1, "reward_lottery_tickets": 1},
            {"name": "アメジスト発見記念", "req_key": "minecraft:amethyst_block", "req_amount": 10, "reward_lottery_tickets": 1},
            {"name": "スローライフ", "req_key": "minecraft:salmon", "req_amount": 16, "reward_lottery_tickets": 1},
            {"name": "モンスターハンター", "req_key": "minecraft:rotten_flesh", "req_amount": 16, "reward_lottery_tickets": 1},
            {"name": "雪だるま", "req_key": "minecraft:snow_block", "req_amount": 2, "reward_lottery_tickets": 1},
        ]
    },
    {
        "difficulty": "★★ (中級)",
        "list": [
            {"name": "リッチな昼食", "req_key": "minecraft:rabbit_stew", "req_amount": 1, "reward_lottery_tickets": 2},
            {"name": "硬くて溶けない氷", "req_key": "minecraft:packed_ice", "req_amount": 1, "reward_lottery_tickets": 2},
            {"name": "ブヨブヨしてる緑な奴", "req_key": "minecraft:slime_block", "req_amount": 4, "reward_lottery_tickets": 2},
            {"name": "ブヨブヨしてる甘い奴", "req_key": "minecraft:honey_block", "req_amount": 4, "reward_lottery_tickets": 2},
        ]
    },
    {
        "difficulty": "★★★ (上級)",
        "list": [
            {"name": "うさぎ討伐隊", "req_key": "minecraft:rabbit_foot", "req_amount": 4, "reward_lottery_tickets": 3},
            {"name": "お豆腐屋さん", "req_key": "minecraft:dried_ghast", "req_amount": 3, "reward_lottery_tickets": 3},
            {"name": "イカしたフィスを探せ", "req_key": "minecraft:wither_skeleton_skull", "req_amount": 1, "reward_lottery_tickets": 3},
            {"name": "ホットな羽付き大会", "req_key": "minecraft:ghast_tear", "req_amount": 3, "reward_lottery_tickets": 3},
        ]
    },
    {
        "difficulty": "特別クエスト",
        "list": [
            # 特別報酬 (アイテム)
            {"name": "ブラック鉱夫", "req_key": "minecraft:obsidian", "req_amount": 32, "reward_original": None},  # 鉄ピッケル修繕 - TBD
            {"name": "赤くてデカくなるアレ", "req_key": "minecraft:red_mushroom", "req_amount": 32, "reward_original": "health_boost_1"},
            {"name": "目指せ太公望", "req_key": "minecraft:pufferfish", "req_amount": 64, "reward_original": "fishingRod"},
            {"name": "追尾しない方の甲羅", "req_key": "minecraft:nautilus_shell", "req_amount": 3, "reward_original": None},  # 亀の甲羅 - TBD
        ]
    }
]

# --- Armor Exchange Quests (防具交換クエスト) ---
# Separate definition for new JSON output
armor_quests = [
    {
        "difficulty": "防具交換 (初回限定)",
        "list": [
            # クエスト形式（1回のみ取引可能）：防具チケット1枚と交換
            {"name": "ダイヤのヘルメット(防護V、耐久V)", "req_original": "防具チケット", "req_amount": 1, "reward_original": "ダイヤのヘルメット(防護V、耐久V)"},
            {"name": "ダイヤのチェストプレート(防護V、耐久V)", "req_original": "防具チケット", "req_amount": 1, "reward_original": "ダイヤのチェストプレート(防護V、耐久V)"},
            {"name": "ダイヤのレギンス(防護V、耐久V)", "req_original": "防具チケット", "req_amount": 1, "reward_original": "ダイヤのレギンス(防護V、耐久V)"},
            {"name": "ダイヤのブーツ(防護V、耐久V)", "req_original": "防具チケット", "req_amount": 1, "reward_original": "ダイヤのブーツ(防護V、耐久V)"},
        ]
    }
]

# --- Lottery (福引) ---
# Based on info.md lottery section
lottery_data = {
    "name": "通常福引",
    "rarities": [
        {
            "name": "ハズレ",
            "probability": 70,
            "items": []  # ハズレ券 - custom item, may not be in DB yet
        },
        {
            "name": "当たり",
            "probability": 24,
            "items": [
                {"key": "minecraft:sponge"},          # スポンジ ×1
                # お食事券 - custom item
                {"key": "minecraft:diamond_block"},    # ダイヤブロック ×1
                {"key": "minecraft:gold_block"},       # 金ブロック ×2
                {"key": "minecraft:iron_block"},       # 鉄ブロック ×3
                {"key": "minecraft:totem_of_undying"}, # 不死のトーテム ×1
                {"key": "minecraft:experience_bottle"}, # エンチャント瓶 ×64
            ]
        },
        {
            "name": "大当たり",
            "probability": 5,
            "items": [
                # 武器チケット, ツールチケット, 防具チケット - custom items
                {"key": "minecraft:shulker_box"},      # シュルカーボックス
                {"original_name": "mending"},          # 修繕
            ]
        },
        {
            "name": "アクセサリー",
            "probability": 1,
            "items": [
                {"original_name": "health_boost_1"},   # 体力増強 (10)
                {"original_name": "health_boost_2"},   # 体力増強 (20)
                {"original_name": "health_boost_3"},   # 体力増強 (30)
                {"original_name": "speed_boost_1"},    # スピード (Ⅰ)
                {"original_name": "haste_boost_2"},    # 採掘速度 (Ⅱ)
                {"original_name": "jump_boost_2"},     # ジャンプ (Ⅱ)
                {"original_name": "slow_falling"},     # 低速落下
                {"original_name": "fire_resistance"},  # 火炎耐性
                {"original_name": "night_vision"},     # 暗視
                {"original_name": "infinite_pearl"},   # 無限エンパ
                {"original_name": "petapeta"},         # ペタペタくん
                {"original_name": "jumpkun"},          # ジャンプくん
            ]
        }
    ]
}

# ============================================================
# 3. Generate Request JSONs
# ============================================================

print("\n--- Generating Pawnshop JSON ---")
pawnshop_request = {"store": [], "patch": [], "delete": []}

for cat in buy_prices_categories:
    npc = {
        "name": cat["category"],
        "biome_id": BIOME_ID,
        "profession_id": PROFESSION_ID,
        "npc_type_id": 1,  # pawnshop
        "trades": []
    }
    for item in cat["items"]:
        db_id = get_id_by_key(item["key"])
        if db_id:
            trade = {
                "content": f"Buy {item['name']}", 
                "view_item_id": db_id,
                "costs": [{"item_id": db_id, "quantity": 1}],
                "rewards": [{"price": item["price"]}]
            }
            npc["trades"].append(trade)
    if npc["trades"]:
        pawnshop_request["store"].append(npc)

with open(os.path.join(OUTPUT_DIR, 'request_pawnshop.json'), 'w', encoding='utf-8') as f:
    json.dump(pawnshop_request, f, indent=2, ensure_ascii=False)
print(f"  Created request_pawnshop.json with {len(pawnshop_request['store'])} NPCs")


print("\n--- Generating Shop JSON ---")
shop_request = {"store": [], "patch": [], "delete": []}

for shop in shops:
    npc = {
        "name": shop["name"],
        "biome_id": BIOME_ID,
        "profession_id": PROFESSION_ID,
        "npc_type_id": 2,  # shop
        "trades": []
    }
    for item in shop["items"]:
        # Get item ID
        db_id = None
        if "original_name" in item:
            db_id = get_id_by_name(item["original_name"])
        elif "key" in item:
            db_id = get_id_by_key(item["key"])
        
        if db_id:
            # Determine cost (money or ticket or original)
            if "price" in item:
                cost = {"price": item["price"]}
            elif "ticket_cost" in item:
                # Ticket-based exchange (use paper as ticket placeholder)
                cost = {"item_id": PAPER_ID, "quantity": item["ticket_cost"]}
            elif "cost_original" in item:
                 cost_id = get_id_by_name(item["cost_original"])
                 if cost_id:
                     cost = {"item_id": cost_id, "quantity": 1}
                 else:
                     continue
            else:
                continue
            
            trade = {
                "content": f"Sell {item['name']}",
                "view_item_id": db_id,
                "costs": [cost],
                "rewards": [{"item_id": db_id, "quantity": item.get("quantity", 1)}]
            }
            npc["trades"].append(trade)
    
    if npc["trades"]:
        shop_request["store"].append(npc)

with open(os.path.join(OUTPUT_DIR, 'request_shop.json'), 'w', encoding='utf-8') as f:
    json.dump(shop_request, f, indent=2, ensure_ascii=False)
print(f"  Created request_shop.json with {len(shop_request['store'])} NPCs")


print("\n--- Generating Quest JSON ---")
quest_request = {"store": [], "patch": [], "delete": []}

for cat in quests:
    npc = {
        "name": f"クエスト ({cat['difficulty']})",
        "biome_id": BIOME_ID,
        "profession_id": PROFESSION_ID,
        "npc_type_id": 3,  # quest
        "trades": []
    }
    for quest in cat["list"]:
        # Requirement can be vanilla key or original item
        req_id = None
        if "req_key" in quest:
            req_id = get_id_by_key(quest["req_key"])
        elif "req_original" in quest:
            req_id = get_id_by_name(quest["req_original"])

        if not req_id:
            continue
        
        # Determine reward
        if "reward_tickets" in quest:
            reward = {"item_id": PAPER_ID, "quantity": quest["reward_tickets"]}
        elif "reward_original" in quest and quest["reward_original"]:
            reward_id = get_id_by_name(quest["reward_original"])
            if reward_id:
                reward = {"item_id": reward_id, "quantity": 1}
            else:
                continue
        else:
            # Default to paper if not specified
            reward = {"item_id": PAPER_ID, "quantity": 1}
        
        trade = {
            "content": quest["name"],
            "view_item_id": req_id,
            "costs": [{"item_id": req_id, "quantity": quest["req_amount"]}],
            "rewards": [reward]
        }
        npc["trades"].append(trade)
    
    if npc["trades"]:
        quest_request["store"].append(npc)

with open(os.path.join(OUTPUT_DIR, 'request_quest.json'), 'w', encoding='utf-8') as f:
    json.dump(quest_request, f, indent=2, ensure_ascii=False)
print(f"  Created request_quest.json with {len(quest_request['store'])} NPCs")


print("\n--- Generating Quest Patch JSON ---")
quest_patch_request = {"store": [], "patch": [], "delete": []}

for cat in vanilla_quest_patches:
    npc = {
        "id": cat["id"],
        "name": f"クエスト ({cat['difficulty']})",
        "biome_id": BIOME_ID,
        "profession_id": PROFESSION_ID,
        "npc_type_id": 3,  # quest
        "add_trades": []
    }
    
    # Only process new quests from the patch list (no merging needed)
    for quest in cat["list"]:
        # Requirement can be vanilla key or original item
        req_id = None
        if "req_key" in quest:
            req_id = get_id_by_key(quest["req_key"])
        elif "req_original" in quest:
            req_id = get_id_by_name(quest["req_original"])

        if not req_id:
            continue
        
        # Determine reward
        if "reward_tickets" in quest:
            reward = {"item_id": PAPER_ID, "quantity": quest["reward_tickets"]}
        elif "reward_lottery_tickets" in quest:
             # Hardcoded Lottery Ticket ID from user request
            reward = {"item_id": 1532, "quantity": quest["reward_lottery_tickets"]}
        elif "reward_original" in quest and quest["reward_original"]:
            reward_id = get_id_by_name(quest["reward_original"])
            if reward_id:
                reward = {"item_id": reward_id, "quantity": 1}
            else:
                continue
        else:
            # Default to paper if not specified
            reward = {"item_id": PAPER_ID, "quantity": 1}
        
        trade = {
            "content": quest["name"],
            "view_item_id": req_id,
            "costs": [{"item_id": req_id, "quantity": quest["req_amount"]}],
            "rewards": [reward]
        }
        npc["add_trades"].append(trade)
    
    if npc["add_trades"]:
        quest_patch_request["patch"].append(npc)

with open(os.path.join(OUTPUT_DIR, 'request_quest_patch.json'), 'w', encoding='utf-8') as f:
    json.dump(quest_patch_request, f, indent=2, ensure_ascii=False)
print(f"  Created request_quest_patch.json with {len(quest_patch_request['patch'])} patches")


print("\n--- Generating Lottery JSON ---")
lottery_request = {"store": [], "patch": [], "delete": []}

lottery_obj = {
    "name": lottery_data["name"],
    "rarities": []
}

for rarity in lottery_data["rarities"]:
    rarity_obj = {
        "name": rarity["name"],
        "probability": rarity["probability"],
        "items": []
    }
    for item in rarity["items"]:
        item_id = None
        if "original_name" in item:
            item_id = get_id_by_name(item["original_name"])
        elif "key" in item:
            item_id = get_id_by_key(item["key"])
        
        if item_id:
            rarity_obj["items"].append(item_id)
    
    lottery_obj["rarities"].append(rarity_obj)

lottery_request["store"].append(lottery_obj)

with open(os.path.join(OUTPUT_DIR, 'request_lottery.json'), 'w', encoding='utf-8') as f:
    json.dump(lottery_request, f, indent=2, ensure_ascii=False)
print(f"  Created request_lottery.json with {len(lottery_obj['rarities'])} rarities")


print("\n--- Generating Armor Trades JSON ---")
armor_request = {"store": [], "patch": [], "delete": []}

# Process Armor Shops
for shop in armor_shops:
    npc = {
        "name": shop["name"],
        "biome_id": BIOME_ID,
        "profession_id": PROFESSION_ID,
        "npc_type_id": 2,  # shop
        "trades": []
    }
    for item in shop["items"]:
        # Get item ID
        db_id = None
        if "original_name" in item:
            db_id = get_id_by_name(item["original_name"])
        elif "key" in item:
            db_id = get_id_by_key(item["key"])
        
        if db_id:
            # Determine cost
            if "cost_original" in item:
                 cost_id = get_id_by_name(item["cost_original"])
                 if cost_id:
                     cost = {"item_id": cost_id, "quantity": 1}
                 else:
                     continue
            else:
                continue
            
            trade = {
                "content": f"Sell {item['name']}",
                "view_item_id": db_id,
                "costs": [cost],
                "rewards": [{"item_id": db_id, "quantity": item.get("quantity", 1)}]
            }
            npc["trades"].append(trade)
    
    if npc["trades"]:
        armor_request["store"].append(npc)

# Process Armor Quests
for cat in armor_quests:
    npc = {
        "name": f"クエスト ({cat['difficulty']})",
        "biome_id": BIOME_ID,
        "profession_id": PROFESSION_ID,
        "npc_type_id": 3,  # quest
        "trades": []
    }
    for quest in cat["list"]:
        # Requirement can be vanilla key or original item
        req_id = None
        if "req_key" in quest:
            req_id = get_id_by_key(quest["req_key"])
        elif "req_original" in quest:
            req_id = get_id_by_name(quest["req_original"])

        if not req_id:
            continue
        
        # Determine reward
        if "reward_original" in quest and quest["reward_original"]:
            reward_id = get_id_by_name(quest["reward_original"])
            if reward_id:
                reward = {"item_id": reward_id, "quantity": 1}
            else:
                continue
        else:
            continue
        
        trade = {
            "content": quest["name"],
            "view_item_id": req_id,
            "costs": [{"item_id": req_id, "quantity": quest["req_amount"]}],
            "rewards": [reward]
        }
        npc["trades"].append(trade)
    
    if npc["trades"]:
        armor_request["store"].append(npc)

with open(os.path.join(OUTPUT_DIR, 'request_armor_trades.json'), 'w', encoding='utf-8') as f:
    json.dump(armor_request, f, indent=2, ensure_ascii=False)
print(f"  Created request_armor_trades.json with {len(armor_request['store'])} NPCs")


print("\n--- Generating Food Trades JSON ---")
food_request = {"store": [], "patch": [], "delete": []}

# Process Restaurant Shops
for shop in restaurant_shops:
    npc = {
        "name": shop["name"],
        "biome_id": BIOME_ID,
        "profession_id": PROFESSION_ID,
        "npc_type_id": 2,  # shop
        "trades": []
    }
    for item in shop["items"]:
        # Get item ID
        db_id = None
        if "original_name" in item:
            db_id = get_id_by_name(item["original_name"])
        elif "key" in item:
            db_id = get_id_by_key(item["key"])
        
        if db_id:
            # Determine cost
            if "cost_original" in item:
                 cost_id = get_id_by_name(item["cost_original"])
                 if cost_id:
                     cost = {"item_id": cost_id, "quantity": 1}
                 else:
                     continue
            else:
                continue
            
            trade = {
                "content": f"Sell {item['name']}",
                "view_item_id": db_id,
                "costs": [cost],
                "rewards": [{"item_id": db_id, "quantity": item.get("quantity", 1)}]
            }
            npc["trades"].append(trade)
    
    if npc["trades"]:
        food_request["store"].append(npc)

with open(os.path.join(OUTPUT_DIR, 'request_food_trades.json'), 'w', encoding='utf-8') as f:
    json.dump(food_request, f, indent=2, ensure_ascii=False)
print(f"  Created request_food_trades.json with {len(food_request['store'])} NPCs")

print("\n=== Done! ===")
print(f"Output directory: {OUTPUT_DIR}")
