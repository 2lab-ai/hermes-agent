# Craft Actions Spec

작성일: 2026-05-25

이 문서는 Prototype 제작 동사를 family별 action으로 정의한다.
목표는 제작대마다 UI와 감정은 다르게 만들되, 실행 결과와 실패 모델은 공통으로 처리하는 것이다.

## 공통 Action Shape

```json
{
  "id": "poe_essence_reroll",
  "family": "poe",
  "bench": "PoeAffixWorkbench",
  "label_key": "craft.poe.essence_reroll",
  "input_filter": {
    "origin_family": "poe",
    "rarity": ["magic", "rare"],
    "corrupted": false
  },
  "materials": [
    {
      "material_id": "essence_any",
      "count": 1
    }
  ],
  "preview": {
    "shows_probabilities": true,
    "shows_blocked_outcomes": true,
    "requires_warning": false
  },
  "failure_results": ["resource_loss", "bad_roll"],
  "irreversible": false
}
```

## 공통 Result Rules

- 모든 action은 `CraftResult`를 만든다.
- `success: false`여도 material은 소모될 수 있다.
- `item_break`는 항상 fragment, trace, shard, boss progress 중 하나를 남긴다.
- `irreversible: true` action은 실행 전 UI confirm을 요구한다.
- 반복 제작은 Prototype에서 UI 자동화만 허용하고, 서버/시뮬레이터 action은 항상 1회 단위로 기록한다.

## POE형 Action

### `poe_transmute`

Normal item을 Magic으로 만든다.

```json
{
  "input": "normal poe item",
  "materials": ["orb_transmutation"],
  "output": "magic item with 1 random affix",
  "failure_result": "resource_loss",
  "notes": "초반 tutorial craft. item_level에 맞는 prefix/suffix pool만 사용한다."
}
```

### `poe_alchemy`

Normal item을 Rare로 만든다.

```json
{
  "input": "normal poe item",
  "materials": ["orb_alchemy"],
  "output": "rare item with 4 random affixes in Prototype",
  "failure_result": "bad_roll",
  "notes": "six_affix_unlocked가 true면 4~6 affix로 확장한다."
}
```

### `poe_regal`

Magic item을 Rare로 승격한다.

```json
{
  "input": "magic poe item",
  "materials": ["orb_regal"],
  "output": "rare item preserving existing affixes and adding 1 affix",
  "failure_result": "bad_roll",
  "notes": "magic 상태에서 좋은 2줄을 만든 뒤 rare로 올리는 route를 만든다."
}
```

### `poe_chaos_reroll`

Rare item의 explicit affix를 전부 다시 굴린다.

```json
{
  "input": "rare poe item",
  "materials": ["orb_chaos"],
  "output": "same base, new random rare affixes",
  "failure_result": "bad_roll",
  "blocked_if": ["corrupted", "prefix_lock", "suffix_lock"],
  "notes": "Prototype에서는 lock meta-craft와 동시에 쓰지 않는다."
}
```

### `poe_add_affix`

빈 prefix/suffix에 임의 affix를 추가한다.

```json
{
  "input": "magic or rare poe item with open affix slot",
  "materials": ["orb_augmentation", "orb_exalted"],
  "output": "same item with 1 added affix",
  "failure_result": "bad_roll",
  "notes": "Magic은 augmentation, Rare는 exalted 계열 재료를 쓴다."
}
```

### `poe_annul`

무작위 explicit affix 1개를 제거한다.

```json
{
  "input": "magic or rare poe item with at least 1 explicit affix",
  "materials": ["orb_annulment"],
  "output": "same item with 1 random explicit affix removed",
  "failure_result": "bad_roll",
  "notes": "좋은 줄이 사라질 수 있으므로 preview에 removable lines를 보여준다."
}
```

### `poe_divine`

Affix tier는 유지하고 numeric roll만 다시 굴린다.

```json
{
  "input": "poe item with variable explicit or implicit values",
  "materials": ["orb_divine"],
  "output": "same mods with rerolled numeric values",
  "failure_result": "bad_roll",
  "notes": "고급 확률표 대신 현재 roll percentile과 possible range를 보여준다."
}
```

### `poe_essence_reroll`

보장 tag affix를 포함해 item을 reroll한다.

```json
{
  "input": "normal, magic, or rare poe item",
  "materials": ["essence_by_tag"],
  "output": "rare item with guaranteed tag affix",
  "failure_result": "bad_roll",
  "notes": "태그 제어 crafting의 첫 형태. Fire, Minion, Projectile, Defense 등 8~12개 tag만 시작한다."
}
```

### `poe_bench_craft`

Crafted mod 1개를 붙인다.

```json
{
  "input": "magic or rare poe item with crafted_mod_limit available",
  "materials": ["bench_dust"],
  "output": "same item with crafted mod",
  "failure_result": "resource_loss",
  "blocked_if": ["corrupted", "crafted_mod_limit_reached"],
  "notes": "좋은 item을 완성하는 deterministic capstone 역할."
}
```

### `poe_corrupt`

아이템을 되돌릴 수 없는 corrupted 상태로 바꾼다.

```json
{
  "input": "non-corrupted poe item",
  "materials": ["corruption_orb"],
  "output": "one of: no_change_corrupted, add_corrupted_implicit, reroll_to_corrupted_rare, brick_to_fragment",
  "failure_result": "item_break",
  "irreversible": true,
  "notes": "완전 소실 대신 corrupted fragment를 남긴다."
}
```

## D2형 Action

### `d2_add_socket`

베이스에 socket을 부여한다.

```json
{
  "input": "d2 item without sockets or below max sockets",
  "materials": ["socket_kit"],
  "output": "same item with socket_count set or increased",
  "failure_result": "resource_loss",
  "notes": "Prototype에서는 무작위 socket 수 대신 preview 가능한 범위를 쓴다."
}
```

### `d2_insert_material`

Rune, gem, jewel을 socket에 넣는다.

```json
{
  "input": "d2 item with open socket",
  "materials": ["rune_or_gem_or_jewel"],
  "output": "socket filled; socketed material stat active",
  "failure_result": "none",
  "notes": "삽입 자체는 실패하지 않는다. 잘못된 순서는 runeword만 비활성화한다."
}
```

### `d2_clear_sockets`

Socket 재료를 제거하되 재료는 파괴한다.

```json
{
  "input": "d2 socketed item",
  "materials": ["cleansing_cube_token"],
  "output": "same item with empty sockets",
  "failure_result": "resource_loss",
  "irreversible": true,
  "notes": "베이스는 보존하고 socketed material만 잃는다."
}
```

### `d2_validate_runeword`

현재 socket sequence가 runeword를 만족하는지 검사하고 활성화한다.

```json
{
  "input": "d2 item with filled rune sockets",
  "materials": [],
  "output": "runeword_active true if base, count, order all match",
  "failure_result": "bad_roll",
  "notes": "명시 action이라기보다 insert 후 자동 검사. UI에는 가능한 runeword와 순서 오류를 보여준다."
}
```

### `d2_upgrade_base`

Normal base를 상위 tier로 올린다.

```json
{
  "input": "d2 item with base_tier below max",
  "materials": ["upgrade_rune", "upgrade_gem"],
  "output": "same item with higher base stats and requirements",
  "failure_result": "resource_loss",
  "notes": "저레벨 좋은 아이템을 버리지 않게 만드는 action."
}
```

### `d2_craft_family_recipe`

정해진 제작군 아이템을 만든다.

```json
{
  "input": "valid d2 base item",
  "materials": ["family_rune", "family_gem", "family_jewel"],
  "output": "crafted item with fixed family mods and random affixes",
  "failure_result": "bad_roll",
  "notes": "Blood/Caster/Safety를 자동전투형 흡혈/시전/방어/소환 family로 번역한다."
}
```

## Layered Enhancement Action

### `layered_reroll_flame`

드랍 보너스 줄을 다시 굴린다.

```json
{
  "input": "layered_enhancement item",
  "materials": ["flame"],
  "output": "1~3 flame lines rerolled",
  "failure_result": "bad_roll",
  "notes": "Maple flame의 역할. slot별 pool을 강하게 제한한다."
}
```

### `layered_safe_enhance`

안전 강화선 이하에서 +1을 보장한다.

```json
{
  "input": "item with enchant_level below safe_limit",
  "materials": ["enhance_scroll"],
  "output": "enchant_level +1",
  "failure_result": "resource_loss",
  "notes": "실패가 있더라도 item_break는 절대 발생하지 않는다."
}
```

### `layered_over_enhance`

안전선 이후 고위험 강화를 시도한다.

```json
{
  "input": "item with enchant_level >= safe_limit",
  "materials": ["enhance_scroll", "meso_like_gold"],
  "output": "one of: +1, unchanged, -1, broken_to_trace",
  "failure_result": "tier_loss or item_break",
  "notes": "파괴 시 destruction_trace_id와 trace_progress를 남긴다."
}
```

### `layered_blessed_jump`

성공 시 +1~2 단계 점프를 시도한다.

```json
{
  "input": "layered_enhancement item",
  "materials": ["blessed_scroll"],
  "output": "one of: +1, +2, unchanged, tier_loss",
  "failure_result": "tier_loss",
  "notes": "Lineage blessed scroll 감정. 확률은 UI에 직접 표시한다."
}
```

### `layered_cursed_adjust`

강화 단계를 의도적으로 낮춘다.

```json
{
  "input": "item with enchant_level > 0",
  "materials": ["cursed_scroll"],
  "output": "enchant_level -1",
  "failure_result": "resource_loss",
  "notes": "고위험 구간 재시도나 recipe 조건 맞추기용."
}
```

### `layered_reroll_potential`

Potential line을 다시 굴린다.

```json
{
  "input": "layered_enhancement item",
  "materials": ["potential_cube"],
  "output": "potential lines rerolled; chance to grade up",
  "failure_result": "bad_roll",
  "notes": "현금성 cube는 금지. pity counter를 항상 보여준다."
}
```

### `layered_restore_trace`

파괴 흔적으로 새 베이스에 일부 상태를 복구한다.

```json
{
  "input": "matching base item and destruction trace",
  "materials": ["destruction_trace", "restore_core"],
  "output": "new item with restored subset of flame, potential, enchant",
  "failure_result": "resource_loss",
  "notes": "파괴를 완전 소실이 아니라 장기 진행 손실로 바꾼다."
}
```

## Last Epoch형 Action

### `le_add_affix_shard`

빈 normal affix slot에 shard affix를 추가한다.

```json
{
  "input": "last_epoch item with open affix slot and forging_potential > 0",
  "materials": ["affix_shard"],
  "output": "same item with T1 affix added",
  "failure_result": "craft_life_loss",
  "notes": "Potential cost range를 preview한다."
}
```

### `le_upgrade_affix_tier`

Affix tier를 1 올린다.

```json
{
  "input": "last_epoch item with craftable affix below T5",
  "materials": ["matching_affix_shard"],
  "output": "affix tier +1 and forging_potential reduced",
  "failure_result": "craft_life_loss",
  "notes": "T6/T7은 drop-only라 craft target이 될 수 없다."
}
```

### `le_reroll_affix_value`

Affix tier는 유지하고 roll만 다시 굴린다.

```json
{
  "input": "last_epoch item with variable affix",
  "materials": ["glyph_refinement"],
  "output": "same affix tiers with rerolled values",
  "failure_result": "craft_life_loss",
  "notes": "좋은 tier를 보존하면서 perfect roll을 노리는 sink."
}
```

### `le_remove_random_affix`

무작위 affix를 제거하고 shard를 일부 회수한다.

```json
{
  "input": "last_epoch item with removable normal affix",
  "materials": ["rune_removal"],
  "output": "one random normal affix removed; shard returned",
  "failure_result": "bad_roll",
  "notes": "sealed affix와 exalted affix는 Prototype에서 제거 대상이 아니다."
}
```

### `le_seal_affix`

Affix 하나를 sealed slot으로 옮긴다.

```json
{
  "input": "last_epoch item with normal affix and empty sealed slot",
  "materials": ["glyph_despair"],
  "output": "affix moved to sealed slot; normal slot opens",
  "failure_result": "craft_life_loss",
  "irreversible": true,
  "notes": "성공 후 sealed affix는 수정/제거 불가."
}
```

### `le_shatter`

아이템을 파괴해 affix shard를 얻는다.

```json
{
  "input": "last_epoch item",
  "materials": ["rune_shattering"],
  "output": "item destroyed; shards returned based on affixes",
  "failure_result": "item_break",
  "irreversible": true,
  "notes": "의도적 파괴 action. 일반 실패와 혼동하지 않도록 별도 버튼으로 둔다."
}
```

## SkillSupportBoard Action

### `skill_socket_support`

Active skill에 support를 장착한다.

```json
{
  "input": "active skill with open support socket",
  "materials": ["support_gem"],
  "output": "support installed if tag rules match",
  "failure_result": "none",
  "notes": "tag가 맞지 않으면 장착 불가로 처리한다. 비활성 장착은 Prototype에서 금지한다."
}
```

### `skill_upgrade_socket_count`

Skill의 support socket 수를 늘린다.

```json
{
  "input": "active skill below socket cap",
  "materials": ["skill_link_core"],
  "output": "support socket count +1",
  "failure_result": "resource_loss",
  "notes": "초기 2개, 후반 4~5개. 6-link급은 endgame chase로 남긴다."
}
```

### `skill_set_behavior_priority`

자동전투 사용 우선순위를 정한다.

```json
{
  "input": "active skill",
  "materials": [],
  "output": "behavior_priority changed",
  "failure_result": "none",
  "notes": "전투 조작 대신 build phase에서 AI 행동을 설계하게 한다."
}
```

## MapKeyCrafting Action

### `map_add_danger`

위험 modifier를 추가하고 보상 계수를 올린다.

```json
{
  "input": "map key with open danger slot",
  "materials": ["danger_ink"],
  "output": "new danger mod and reward multiplier increase",
  "failure_result": "resource_loss",
  "notes": "자동전투 실패 가능성을 올리는 대신 드랍 기대값도 올린다."
}
```

### `map_reroll_reward`

Reward modifier를 다시 굴린다.

```json
{
  "input": "map key with reward mods",
  "materials": ["reward_orb"],
  "output": "reward mods rerolled, danger preserved",
  "failure_result": "bad_roll",
  "notes": "위험은 유지되어 sunk cost 선택이 생긴다."
}
```

### `map_bias_family`

특정 origin_family 드랍 가중치를 올린다.

```json
{
  "input": "map key",
  "materials": ["family_scarab"],
  "output": "origin_bias shifted toward selected family",
  "failure_result": "resource_loss",
  "notes": "POE형 재료맵, D2 룬맵, 강화 scroll맵처럼 목표 파밍을 만든다."
}
```

### `map_corrupt`

MapKey를 되돌릴 수 없는 고위험 상태로 만든다.

```json
{
  "input": "non-corrupted map key",
  "materials": ["corruption_orb"],
  "output": "one of: extra danger, extra reward, unidentified mods, boss fragment surge, bricked fragment",
  "failure_result": "item_break",
  "irreversible": true,
  "notes": "bricked key도 boss_key_progress나 fragment를 남긴다."
}
```

### `map_combine_boss_fragments`

보스 키 조각을 합친다.

```json
{
  "input": "boss fragments",
  "materials": ["fragment_set"],
  "output": "boss map key",
  "failure_result": "none",
  "notes": "D2 special map recipe와 POE fragment key를 자동전투 boss run으로 번역한다."
}
```

## UI Preview Contract

제작 버튼을 누르기 전 UI는 최소 아래 정보를 보여야 한다.

- 투입 아이템 상태.
- 소모 재료와 보유 수량.
- 가능한 성공 결과.
- 가능한 실패 결과.
- 되돌릴 수 없는 상태 변화.
- 확률이 있는 경우 성공/실패/하락/파괴 확률.
- tag 기반 결과라면 가능한 tag pool.
- 반복 제작 가능 action이라면 예상 소모량과 중단 조건.

## Logging Contract

전투 로그와 제작 로그는 같은 형식으로 남긴다.

```json
{
  "turn": 143,
  "kind": "craft",
  "action_id": "le_upgrade_affix_tier",
  "item_id": "item_000031",
  "before_hash": "b7a1",
  "after_hash": "c94d",
  "summary_key": "log.craft.le_upgrade_affix_tier",
  "failure_result": "craft_life_loss",
  "irreversible": false
}
```

이 로그가 있어야 플레이어가 자동전투 패배 후 어떤 제작 선택이 원인이었는지 추적할 수 있다.

