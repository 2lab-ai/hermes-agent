# Prototype Data Schema

작성일: 2026-05-25

이 문서는 리서치 결과를 프로토타입 데이터 모델로 내린 것이다.
목표는 원작 시스템을 그대로 복제하는 것이 아니라, 서로 다른 제작 문법을 한 게임 안에서 안전하게 공존시키는 최소 공통 스키마를 정의하는 것이다.

## 설계 원칙

- 모든 장비는 공통 `ItemInstance`를 가진다.
- 원작별 차이는 `origin_family`와 `craft_state`에 격리한다.
- 전투 시뮬레이션은 원작 세부 제작 규칙을 직접 알 필요가 없다.
- 제작 UI는 family별 상태를 읽지만, 결과는 공통 `CraftResult`로 기록한다.
- 되돌릴 수 없는 행동은 `history`에 반드시 남긴다.

## 공통 Enum

```json
{
  "OriginFamily": [
    "poe",
    "d2",
    "layered_enhancement",
    "last_epoch",
    "skill_rune",
    "map_key",
    "passive_jewel",
    "sealed_research",
    "spatial_grid",
    "spell_program",
    "module_budget",
    "recipe_trait_lab"
  ],
  "Rarity": [
    "normal",
    "magic",
    "rare",
    "unique",
    "set",
    "crafted",
    "runeword",
    "legendary",
    "corrupted"
  ],
  "EquipSlot": [
    "weapon",
    "offhand",
    "helmet",
    "body",
    "gloves",
    "boots",
    "amulet",
    "ring",
    "belt",
    "relic"
  ],
  "AffixSlot": [
    "implicit",
    "prefix",
    "suffix",
    "sealed",
    "crafted",
    "flame",
    "potential",
    "runeword",
    "socketed"
  ],
  "FailureResult": [
    "none",
    "resource_loss",
    "bad_roll",
    "craft_life_loss",
    "tier_loss",
    "item_break"
  ],
  "BindState": [
    "tradable",
    "account_bound",
    "character_bound",
    "locked_for_crafting"
  ]
}
```

## Entity Map

프로토타입 핵심은 아래 9개 타입이면 충분하다.

- `ItemInstance`: 실제 드랍/장착/제작 대상.
- `BaseItemDefinition`: 베이스 아이템 정의.
- `ModDefinition`: affix, implicit, potential, flame, runeword line의 원본.
- `MaterialStack`: currency, rune, shard, scroll, fragment.
- `CraftActionDefinition`: 제작 동사 정의.
- `CraftResult`: 제작 실행 결과.
- `SkillGem`: 자동전투 active skill.
- `SupportGem`: skill behavior modifier.
- `MapKey`: 자동전투 콘텐츠 입장 아이템.

4차 딥다이브에서 추가된 보조 타입은 Prototype/V1 경계에 둔다.

- `GridItem`: 공간 보드에 배치되는 아이템.
- `RecipeUnlock`: 드랍/소비로 영구 제작법을 여는 레시피 아이템.
- `SalvageResource`: 분해로 얻는 bits/shards/runes 계열 자원.
- `AttachableTrait`: 장비/소환수/스킬에 붙는 자동 발동 trait.
- `ProgrammableItem`: 좌->우로 컴파일되는 주문 프로그램 아이템.
- `ModuleBudgetBoard`: capacity/polarity/drain 기반 장비 보드.

## ItemInstance

모든 장비는 이 공통 형태를 가진다.

```json
{
  "id": "item_000001",
  "origin_family": "poe",
  "base_id": "iron_sword",
  "slot": "weapon",
  "item_level": 18,
  "rarity": "rare",
  "requirements": {
    "level": 12,
    "str": 24,
    "dex": 0,
    "int": 0
  },
  "implicit_mods": ["mod_sword_phys_implicit_t2"],
  "explicit_mods": [
    {
      "mod_id": "mod_added_fire_prefix_t2",
      "slot": "prefix",
      "tier": 2,
      "roll": 0.64,
      "source": "drop"
    }
  ],
  "crafted_mods": [],
  "craft_state": {
    "family": "poe",
    "state": {}
  },
  "bind_state": "tradable",
  "source_map": {
    "map_key_id": "map_000014",
    "area_level": 18,
    "biome": "crypt"
  },
  "history": [
    {
      "turn": 124,
      "action": "drop",
      "summary": "Dropped as rare in crypt map"
    }
  ]
}
```

## BaseItemDefinition

베이스는 드랍 가치와 제작 가능성을 동시에 정한다.

```json
{
  "id": "iron_sword",
  "name_key": "base.iron_sword",
  "slot": "weapon",
  "tags": ["weapon", "sword", "one_hand", "melee"],
  "drop_level": 1,
  "max_item_level": 30,
  "base_stats": {
    "attack_min": 5,
    "attack_max": 9,
    "attacks_per_second": 1.35
  },
  "implicit_pool": ["implicit_sword_physical", "implicit_sword_accuracy"],
  "affix_pool_id": "pool_weapon_sword_t1",
  "socket_rules": {
    "max_sockets": 3,
    "allowed_materials": ["rune", "gem", "jewel"]
  },
  "family_allowed": ["poe", "d2", "last_epoch", "layered_enhancement"]
}
```

## ModDefinition

모든 옵션 줄은 같은 definition으로 표현한다.

```json
{
  "id": "mod_added_fire_prefix_t2",
  "name_key": "mod.added_fire_damage",
  "slot": "prefix",
  "tags": ["damage", "fire", "attack"],
  "tier": 2,
  "weight": 350,
  "item_level_min": 12,
  "applies_to": ["weapon"],
  "exclusive_group": "added_elemental_damage",
  "values": [
    {
      "stat": "flat_fire_damage_min",
      "min": 3,
      "max": 5
    },
    {
      "stat": "flat_fire_damage_max",
      "min": 7,
      "max": 11
    }
  ],
  "combat_hooks": [
    {
      "hook": "on_hit",
      "effect": "add_damage",
      "damage_type": "fire"
    }
  ],
  "ui_group": "offense"
}
```

## POE Craft State

POE형은 prefix/suffix와 irreversible state가 핵심이다.

```json
{
  "family": "poe",
  "max_prefixes": 3,
  "max_suffixes": 3,
  "crafted_mod_limit": 1,
  "prefix_lock": false,
  "suffix_lock": false,
  "fractured_mod_ids": [],
  "corrupted": false,
  "influence_tags": [],
  "quality": 0,
  "rarity_unlock": {
    "rare_affix_cap": 4,
    "six_affix_unlocked": false
  }
}
```

프로토타입 제한:

- 초반 rare는 4 affix까지.
- 엔드게임에서 6 affix를 해금한다.
- influence는 Prototype에서는 데이터 필드만 두고 실제 행동은 미룬다.

## D2 Craft State

D2형은 베이스, 소켓, 순서, recipe eligibility가 핵심이다.

```json
{
  "family": "d2",
  "base_quality": "normal",
  "base_tier": "normal",
  "superior_roll": 0,
  "ethereal": false,
  "socket_count": 3,
  "sockets": [
    {
      "index": 0,
      "material_id": "rune_tal",
      "material_type": "rune"
    },
    {
      "index": 1,
      "material_id": "rune_eth",
      "material_type": "rune"
    },
    {
      "index": 2,
      "material_id": "rune_ral",
      "material_type": "rune"
    }
  ],
  "runeword_id": "ember_pulse",
  "runeword_active": true,
  "cube_recipe_locks": []
}
```

프로토타입 제한:

- 룬은 12종 이하.
- 룬워드는 슬롯별 2~4개.
- runeword는 순서가 틀리면 활성화되지 않고 socketed stat만 적용된다.

## Layered Enhancement Craft State

MapleStory와 Lineage 1은 하나로 묶어 장기 강화 레이어를 만든다.

```json
{
  "family": "layered_enhancement",
  "safe_limit": 5,
  "enchant_level": 7,
  "star_tier": 7,
  "flame_lines": [
    {
      "mod_id": "flame_bonus_str_t2",
      "tier": 2,
      "roll": 0.42
    }
  ],
  "potential_grade": "epic",
  "potential_lines": [
    {
      "mod_id": "potential_attack_percent_t1",
      "tier": 1,
      "roll": 0.75
    },
    {
      "mod_id": "potential_life_percent_t1",
      "tier": 1,
      "roll": 0.21
    }
  ],
  "trace_progress": 37,
  "destruction_trace_id": null,
  "protection_active": false,
  "pity": {
    "potential_grade_up_attempts": 4,
    "next_grade_guarantee_at": 12
  }
}
```

프로토타입 제한:

- `flame_lines`는 1~3줄.
- `potential_lines`는 2줄에서 시작하고 후반 3줄.
- 완전 파괴는 high-risk action에서만 허용하고 항상 trace를 남긴다.

## Last Epoch Craft State

Last Epoch형은 제작 수명과 sealed fifth line이 핵심이다.

```json
{
  "family": "last_epoch",
  "forging_potential": 18,
  "max_normal_affixes": 4,
  "sealed_affix": {
    "mod_id": "mod_chill_on_hit_suffix_t1",
    "tier": 1,
    "roll": 0.55,
    "sealed_at_turn": 88
  },
  "exalted_mod_ids": ["mod_minion_damage_prefix_t6"],
  "legendary_potential": 0,
  "weaver_progress": null,
  "last_forge_result": {
    "action": "upgrade_affix_tier",
    "potential_spent": 3,
    "turn": 121
  }
}
```

프로토타입 제한:

- 제작 가능 tier는 T5까지.
- T6/T7은 드랍 전용.
- `legendary_potential`은 UI 표시만 하고 실제 unique imprint는 V1로 미룬다.

## Spatial / Program / Module Extension Schemas

4차 딥다이브에서 나온 비-POE 문법은 Prototype 전체 핵심이 아니라 보조 표면으로 둔다.
다만 `RecipeUnlock`과 `SalvageResource`는 낮은 티어 드랍을 계속 의미 있게 만들기 때문에 Prototype에 포함한다.

### GridItem

```json
{
  "id": "grid_item_iron_charm",
  "origin_family": "spatial_grid",
  "shape_cells": [[0, 0], [1, 0]],
  "rotation": 0,
  "tags": ["charm", "metal", "attack"],
  "position": {
    "board_id": "charm_grid",
    "x": 2,
    "y": 3
  },
  "adjacency_rules": [
    {
      "mode": "orthogonal",
      "required_tags": ["rune"],
      "effect_id": "effect_attack_speed_near_rune"
    }
  ],
  "recipe_refs": ["recipe_charged_iron_charm"]
}
```

### RecipeUnlock / SalvageResource

```json
{
  "recipe_id": "recipe_mod_chain_projectile",
  "origin_family": "recipe_trait_lab",
  "target_type": "mod",
  "source": "data_disk_drop",
  "consumed_on_use": true,
  "learned_permanent": true,
  "required_tier": 2
}
```

```json
{
  "resource_id": "bit_red_t2",
  "source_item_id": "item_000421",
  "disassemble_rule": "highest_bit_guaranteed",
  "guaranteed_yield": ["bit_red_t2"],
  "random_yield": ["bit_gray_t1", "bit_blue_t1"]
}
```

### ProgrammableItem

```json
{
  "id": "wand_0007",
  "origin_family": "spell_program",
  "slots": ["spell_firebolt", "mod_split", "trigger_on_hit_explode"],
  "fixed_prefix_slots": [],
  "shuffle": false,
  "spells_per_cast": 1,
  "cast_delay_frames": 18,
  "recharge_frames": 72,
  "mana_max": 120,
  "mana_regen_per_frame": 1,
  "rng_seed": 91922,
  "compile_mode": "fixed_tick_bytecode"
}
```

### ModuleBudgetBoard

```json
{
  "carrier_item_id": "item_relic_0009",
  "origin_family": "module_budget",
  "carrier_level": 12,
  "base_capacity": 30,
  "capacity_multiplier": 1,
  "slots": [
    {
      "index": 0,
      "polarity": "flame",
      "accepts_tags": ["damage", "fire"],
      "installed_module_id": "mod_burning_engine"
    }
  ],
  "remaining_capacity": 8
}
```

Prototype 제한:

- `GridItem`은 `CharmGridBoard` 전용으로만 사용한다.
- `ProgrammableItem`과 `ModuleBudgetBoard`는 V1 데이터 호환성을 위해 스키마만 둔다.
- `RecipeUnlock`과 `SalvageResource`는 Prototype 제작 경제에 포함한다.

## Skill Board Schema

스킬은 장비가 아니라 자동전투 행동 카드다.

```json
{
  "id": "skill_fire_orb",
  "slot_index": 0,
  "skill_id": "fire_orb",
  "level": 7,
  "quality": 0,
  "tags": ["spell", "projectile", "fire", "aoe"],
  "base_behavior": {
    "cooldown_seconds": 2.4,
    "targeting": "nearest_elite",
    "range": 8,
    "projectiles": 1
  },
  "support_sockets": [
    {
      "index": 0,
      "support_id": "support_multi_projectile",
      "level": 3
    },
    {
      "index": 1,
      "support_id": "support_on_kill_explode",
      "level": 1
    }
  ],
  "behavior_priority": 40,
  "reservation_cost": 0
}
```

## Passive Tree Lite Schema

Prototype은 거대 트리가 아니라 3갈래 트리로 시작한다.

```json
{
  "class_id": "pyromancer",
  "start_node_id": "pyro_start",
  "allocated_nodes": [
    "pyro_start",
    "fire_damage_01",
    "ignite_notable_01",
    "volatile_keystone"
  ],
  "jewel_sockets": [
    {
      "socket_id": "pyro_jewel_01",
      "item_id": "item_jewel_0004"
    }
  ],
  "mastery_choices": [
    {
      "cluster_id": "fire_cluster_01",
      "choice_id": "fire_mastery_projectile_speed"
    }
  ]
}
```

## MapKey Schema

MapKey는 전투 콘텐츠이면서 제작 아이템이다.

```json
{
  "id": "map_000014",
  "area_level": 18,
  "biome": "crypt",
  "tier": 2,
  "monster_tags": ["undead", "swarm"],
  "danger_mods": [
    {
      "mod_id": "danger_monster_speed_t1",
      "tier": 1,
      "roll": 0.6
    }
  ],
  "reward_mods": [
    {
      "mod_id": "reward_rune_drop_t1",
      "tier": 1,
      "roll": 0.3
    }
  ],
  "origin_bias": {
    "poe": 0.35,
    "d2": 0.3,
    "layered_enhancement": 0.2,
    "last_epoch": 0.15
  },
  "boss_key_progress": {
    "boss_id": "crypt_lord",
    "fragments": 2,
    "required": 5
  },
  "corrupted": false,
  "entry_cost": {
    "stamina": 1,
    "key_consumed": true
  }
}
```

## CraftResult

모든 제작 동사는 같은 결과 envelope을 반환한다.

```json
{
  "action_id": "poe_essence_reroll",
  "input_item_id": "item_000001",
  "output_item_id": "item_000001",
  "materials_spent": [
    {
      "material_id": "essence_fire_t2",
      "count": 1
    }
  ],
  "failure_result": "bad_roll",
  "success": true,
  "state_changes": [
    {
      "path": "explicit_mods",
      "change": "rerolled_all_with_guaranteed_fire_prefix"
    }
  ],
  "player_visible_summary": "Fire prefix guaranteed, other affixes rerolled",
  "irreversible": false,
  "history_event": {
    "turn": 132,
    "action": "poe_essence_reroll",
    "summary": "Used fire essence on rare sword"
  }
}
```

## Derived Combat Channels

전투 시뮬레이터는 원작별 제작 상태 대신 아래 파생 채널만 읽는다.

- `damage_channels`: physical, fire, cold, lightning, poison, chaos.
- `defense_channels`: armor, evasion, barrier, block, ward.
- `auto_behavior`: cooldown, target priority, projectile count, chain, trigger.
- `resource_channels`: life, shield, mana, spirit, rage.
- `drop_channels`: family bias, material bias, rarity bias.
- `risk_channels`: self_damage, reduced_recovery, map_timer, durability_loss.

## Validation Rules

프로토타입 데이터 검증은 아래 규칙만 강제한다.

- `origin_family`와 `craft_state.family`는 같아야 한다.
- `slot`은 `base_id`의 allowed slot과 맞아야 한다.
- prefix/suffix 개수는 family별 limit을 넘을 수 없다.
- corrupted item은 corrupted item 전용 action 외에는 제작할 수 없다.
- runeword는 socket count, base type, material order가 모두 맞아야 active가 된다.
- safe limit 이하 enhance는 `item_break`를 낼 수 없다.
- forging potential이 0이면 Last Epoch형 craft action은 `shatter` 외 실행할 수 없다.
- MapKey의 danger/reward mod tier는 `area_level` gate를 넘을 수 없다.

## Prototype Cut Line

이 스키마에서 Prototype에 실제 구현할 범위:

- 장비 family 4개: `poe`, `d2`, `layered_enhancement`, `last_epoch`.
- 스킬 board 1개: `SkillBoard`와 support socket.
- 맵 아이템 1개: `MapKey`.
- 패시브 1개: `PassiveTreeLite`.

V1 이후로 미루는 범위:

- Undecember식 방향/색상 rune board 전체.
- Warframe식 polarity/capacity 전체.
- Noita식 ordered spell program.
- Siralim식 companion party circuit.
- Monster Hunter식 긴 material tree.
