# Map Key Modifiers

작성일: 2026-05-25

이 문서는 자동전투 콘텐츠 입장권인 `MapKey`의 modifier 초안이다.
참조 축은 POE map/POE2 waystone, Diablo II 특수 지역 recipe, Last Epoch Monolith/Echo, Undecember Chaos Card다.

## 목표

- 전투 선택 자체를 아이템 파밍과 제작 루프에 포함한다.
- 자동전투 실패가 완전한 시간 손실로만 끝나지 않게 한다.
- 위험을 올리면 보상과 target farming이 명확히 올라가야 한다.
- `origin_family`별 아이템/재료 파밍을 MapKey에서 조절하게 한다.

## MapKey Core

```json
{
  "area_level": 28,
  "tier": 3,
  "biome": "ash_forest",
  "monster_tags": ["beast", "fire", "swarm"],
  "danger_mods": [],
  "reward_mods": [],
  "origin_bias": {},
  "boss_key_progress": {},
  "corrupted": false,
  "unidentified": false
}
```

## Modifier Slots

Prototype의 MapKey는 아래 slot만 가진다.

- `danger_mods`: 최대 3개.
- `reward_mods`: 최대 3개.
- `origin_bias`: 1개 primary family, 1개 secondary family.
- `special_state`: corrupted, unidentified, boss_touched 중 1개.

Tier 1~3에서는 danger 2개, reward 2개까지만 허용한다.
Tier 4부터 danger 3개, reward 3개를 연다.

## Danger Modifier Categories

| category | 전투 영향 | 보상 보정 |
|---|---|---|
| `monster_count` | 적 수 증가 | quantity 증가 |
| `monster_speed` | 이동/공격 tick 증가 | rarity 소폭 증가 |
| `monster_damage` | 피해 증가 | rarity 증가 |
| `monster_life` | 체력 증가 | material drop 증가 |
| `elite_density` | elite 출현 증가 | high-tier affix chance 증가 |
| `projectile_pressure` | 원거리 탄막 증가 | ranged/support 재료 증가 |
| `ground_hazard` | 바닥 피해/감속 | elemental 재료 증가 |
| `recovery_penalty` | 회복/흡혈 감소 | defense 재료 증가 |
| `resistance_wall` | 특정 피해 저항 증가 | 해당 속성 craft 재료 증가 |
| `timer_pressure` | 제한 시간 또는 enrage | boss fragment 증가 |
| `death_tax` | 패배 시 추가 key damage | reward multiplier 증가 |
| `crafting_curse` | 특정 family 드랍은 증가하지만 crafting risk도 증가 | family material 증가 |

## Reward Modifier Categories

| category | 보상 영향 | 연결 family |
|---|---|---|
| `item_quantity` | 장비 드랍 수 증가 | all |
| `item_rarity` | magic/rare/unique 비율 증가 | all |
| `affix_tier` | 높은 tier affix 등장 확률 증가 | poe, last_epoch |
| `currency_drop` | orb/essence/scroll 증가 | poe, layered_enhancement |
| `rune_drop` | rune/gem/jewel 증가 | d2 |
| `shard_drop` | affix shard/glyph/rune 증가 | last_epoch |
| `enhance_material` | scroll/flame/potential 재료 증가 | layered_enhancement |
| `support_gem` | active/support skill 보상 증가 | skill_rune |
| `map_key_drop` | 다음 map key 드랍 증가 | map_key |
| `boss_fragment` | 보스 조각 진행 증가 | map_key |
| `blessing_choice` | clear 후 blessing 선택지 증가 | account_progress |
| `sealed_research` | V1 family 잠금 해제 연구 아이템 증가 | sealed_research |

## Origin Bias

`origin_bias`는 드랍되는 아이템 문법을 조절한다.

```json
{
  "primary_family": "d2",
  "primary_bonus": 0.35,
  "secondary_family": "poe",
  "secondary_bonus": 0.15,
  "penalty": {
    "family": "layered_enhancement",
    "drop_multiplier": 0.8
  }
}
```

규칙:

- Bias는 총 드랍량을 늘리지 않고 분포를 바꾼다.
- Reward mod와 같이 붙으면 해당 family material도 증가한다.
- 특정 family가 70% 이상으로 쏠리지 않게 cap을 둔다.
- Corruption은 cap을 넘길 수 있지만 danger를 같이 추가한다.

## Prototype Danger Mods

| id | tier | 효과 | reward delta |
|---|---:|---|---|
| `danger_horde_t1` | 1 | monster_count +20% | quantity +10% |
| `danger_horde_t2` | 2 | monster_count +35% | quantity +18% |
| `danger_swift_t1` | 1 | monster_speed +12% | rarity +5% |
| `danger_brutal_t1` | 1 | monster_damage +15% | rarity +8% |
| `danger_bulwark_t1` | 1 | monster_life +20% | material +8% |
| `danger_elite_pack_t2` | 2 | elite_density +1 pack | affix_tier +8% |
| `danger_arrow_rain_t2` | 2 | projectile_pressure +25% | support_gem +8% |
| `danger_burning_ground_t2` | 2 | periodic fire hazard | fire material +12% |
| `danger_no_leech_t3` | 3 | leech_recovery -40% | defense material +18% |
| `danger_fire_wall_t2` | 2 | monsters gain fire resistance | fire craft material +20% |
| `danger_enrage_timer_t3` | 3 | boss enrages after timer | boss_fragment +20% |
| `danger_death_tax_t3` | 3 | defeat damages key reward state | all reward +25% |

## Prototype Reward Mods

| id | tier | 효과 | family |
|---|---:|---|---|
| `reward_quantity_t1` | 1 | item_quantity +15% | all |
| `reward_rarity_t1` | 1 | item_rarity +10% | all |
| `reward_affix_tier_t2` | 2 | high tier affix chance +10% | poe, last_epoch |
| `reward_essence_t1` | 1 | essence drop +20% | poe |
| `reward_orb_t1` | 1 | orb currency +15% | poe |
| `reward_rune_t1` | 1 | rune drop +18% | d2 |
| `reward_socket_base_t2` | 2 | socketed/superior base chance +14% | d2 |
| `reward_scroll_t1` | 1 | enhance scroll +20% | layered_enhancement |
| `reward_flame_t2` | 2 | flame material +18% | layered_enhancement |
| `reward_shard_t1` | 1 | affix shard +20% | last_epoch |
| `reward_glyph_t2` | 2 | glyph/rune forge material +15% | last_epoch |
| `reward_support_t1` | 1 | support gem +15% | skill_rune |
| `reward_boss_fragment_t2` | 2 | boss fragment +1 chance | map_key |
| `reward_blessing_t3` | 3 | clear reward offers blessing choice | account_progress |
| `reward_research_t3` | 3 | sealed research item chance | sealed_research |

## Corruption Outcomes

MapKey corruption은 되돌릴 수 없다.

```json
[
  {
    "outcome": "extra_danger_extra_reward",
    "weight": 40,
    "failure_result": "bad_roll"
  },
  {
    "outcome": "upgrade_reward_tier",
    "weight": 25,
    "failure_result": "none"
  },
  {
    "outcome": "unidentified_key",
    "weight": 20,
    "failure_result": "bad_roll"
  },
  {
    "outcome": "boss_touched",
    "weight": 10,
    "failure_result": "none"
  },
  {
    "outcome": "bricked_to_fragments",
    "weight": 5,
    "failure_result": "item_break"
  }
]
```

`bricked_to_fragments`는 key를 없애지만 boss fragment 또는 map dust를 남긴다.

## Failure Rewards

자동전투 실패 시 아래 중 하나는 반드시 남긴다.

- `map_dust`: MapKey 재제작 재료.
- `atlas_progress`: 같은 biome 진행도.
- `boss_fragment_progress`: 보스 조각 일부.
- `family_material_cache`: 선택 family 재료 소량.
- `death_report`: 어떤 danger mod가 패배 원인이었는지 표시.

실패 보상은 승리 보상을 대체하지 않는다.
목표는 실패를 이득으로 만드는 것이 아니라, 완전 무의미한 손실을 막는 것이다.

## Biome List

Prototype biome은 8개만 둔다.

| biome | monster tags | 대표 위험 | 대표 보상 |
|---|---|---|---|
| `crypt` | undead, swarm | curse, horde | rune, boss fragment |
| `ash_forest` | beast, fire | burning ground | fire essence, flame |
| `iron_keep` | construct, armor | resistance wall | socket base, defense shard |
| `plague_marsh` | poison, slow | recovery penalty | poison affix, leech support |
| `storm_ruins` | lightning, ranged | projectile pressure | projectile support |
| `blood_cavern` | demon, melee | brutal damage | life/leech craft |
| `frozen_archive` | cold, caster | chill/freeze | cooldown and spell material |
| `void_gate` | mixed, elite | timer pressure | corrupted item, blessing |

## Example Map Keys

### D2 Rune Farm

```json
{
  "area_level": 22,
  "biome": "crypt",
  "danger_mods": ["danger_horde_t1", "danger_elite_pack_t2"],
  "reward_mods": ["reward_rune_t1", "reward_socket_base_t2"],
  "origin_bias": {
    "primary_family": "d2",
    "primary_bonus": 0.35
  }
}
```

### POE Affix Farm

```json
{
  "area_level": 34,
  "biome": "storm_ruins",
  "danger_mods": ["danger_arrow_rain_t2", "danger_enrage_timer_t3"],
  "reward_mods": ["reward_affix_tier_t2", "reward_essence_t1"],
  "origin_bias": {
    "primary_family": "poe",
    "primary_bonus": 0.35
  }
}
```

### Last Epoch Shard Farm

```json
{
  "area_level": 28,
  "biome": "iron_keep",
  "danger_mods": ["danger_bulwark_t1", "danger_fire_wall_t2"],
  "reward_mods": ["reward_shard_t1", "reward_glyph_t2"],
  "origin_bias": {
    "primary_family": "last_epoch",
    "primary_bonus": 0.35
  }
}
```

## UI Requirements

MapKey tooltip은 아래를 보여준다.

- Area level, biome, tier.
- Monster tag.
- Danger mod와 reward mod를 짝지어 보여주는 tradeoff line.
- Origin family drop bias.
- Boss fragment progress.
- 자동전투 실패 시 남는 것.
- Corrupted/unidentified 상태.

Map craft 화면은 아래를 보여준다.

- 현재 clear chance estimate.
- 예상 kill time 또는 simulation tick pressure.
- 위험을 추가하면 어떤 reward가 오르는지.
- Family material target.
- 실패 보상.

## Prototype Cut Line

넣는다:

- 8 biome.
- danger mod 12개.
- reward mod 15개.
- origin family bias.
- corruption outcome.
- boss fragment combine.

미룬다:

- Atlas passive tree 전체.
- Undecember Chaos Statue의 깊은 account progression.
- Last Epoch echo web 전체.
- League mechanic별 map device.

