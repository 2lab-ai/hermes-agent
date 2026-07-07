# Skill Support Taxonomy

작성일: 2026-05-25

이 문서는 자동전투 스킬 시스템의 support category를 20개 이하로 제한해 정의한다.
참조 축은 POE2의 skill 자체 support socket, Undecember의 skill/link rune, Noita의 spell order, Grim Dawn의 item-granted trigger다.

## 목표

- 플레이어가 전투 중 직접 조작하지 않아도 빌드로 행동을 설계하게 한다.
- Support는 단순 damage multiplier보다 행동 변형을 우선한다.
- 자동전투 로그에서 "왜 이 스킬이 이렇게 발동했는지"를 읽을 수 있어야 한다.
- Prototype은 방향/색상 rune board를 쓰지 않고 tag compatibility만 쓴다.

## Active Skill Schema

```json
{
  "id": "fire_orb",
  "tags": ["spell", "projectile", "fire", "aoe"],
  "base_cooldown": 2.4,
  "base_targeting": "nearest_elite",
  "base_range": 8,
  "base_projectiles": 1,
  "base_area_radius": 1.4,
  "allowed_support_tags": [
    "projectile",
    "targeting",
    "trigger",
    "area",
    "ailment",
    "resource"
  ],
  "socket_cap": 5
}
```

## Support Category List

Prototype category는 18개로 제한한다.

| category | 역할 | 예시 support | 주요 UI 표시 |
|---|---|---|---|
| `targeting` | 어떤 적을 먼저 노릴지 변경 | nearest elite, lowest hp, highest threat | target priority |
| `projectile_count` | 발사체 수 증가 또는 분할 | multi projectile, spread shot | projectile count, damage penalty |
| `projectile_path` | 관통, 연쇄, 귀환, 분열 | pierce, chain, return | max chain/pierce |
| `area_shape` | 범위 형태 변경 | nova, cone, line, ground zone | shape preview |
| `area_scale` | 범위 크기와 밀도 변경 | larger area, concentrated area | radius, overlap rule |
| `cooldown` | 쿨다운을 줄이거나 늘려 위력 보정 | rapid cast, overcharge | cooldown delta |
| `duration` | 지속시간, tick rate 변경 | longer burn, faster pulse | duration, tick interval |
| `trigger` | 조건부 자동 발동 | on kill, on hit, when shield breaks | trigger condition |
| `sequence` | 다른 스킬 전후에 실행 | cast after primary, repeat previous | sequence line |
| `minion` | 소환수 수/행동 변경 | extra minion, aggressive minion | minion cap, AI mode |
| `ailment` | 상태이상 부여/소모 | ignite, freeze, poison spread | chance, stack cap |
| `conversion` | 피해 타입 변경 | physical to fire, cold to poison | damage type flow |
| `resource` | 비용/회복/예약 변경 | spirit reserve, mana refund | cost, reservation |
| `defense` | 생존 행동 부여 | barrier on cast, armor while channeling | defensive uptime |
| `leech_recovery` | 흡혈/회복/보호막 회복 | life leech, ward gain | recovery per hit |
| `movement` | 위치 행동 변경 | dash cast, orbiting cast | movement trigger |
| `self_risk` | 자해/과열/반동으로 보상 증가 | unstable payload, blood cast | risk warning |
| `loot_utility` | 전투력 대신 드랍/재료 영향 | mark for rune drops | reward tag |

## Compatibility Rules

```json
{
  "support_id": "support_chain",
  "category": "projectile_path",
  "requires_any_skill_tag": ["projectile", "beam"],
  "blocked_skill_tags": ["melee_aura", "minion_only"],
  "exclusive_group": "projectile_path_major",
  "stacking": "single",
  "cost_multiplier": 1.25
}
```

규칙:

- Active skill tag와 support requirement가 맞아야 장착 가능하다.
- 같은 `exclusive_group`은 1개만 장착 가능하다.
- `self_risk` support는 confirm 없이 장착할 수 있지만, 전투 시작 전 위험 아이콘을 보여준다.
- `loot_utility` support는 damage support와 같은 socket을 경쟁하게 해 기회비용을 만든다.

## Active Skill Archetypes

Prototype active skill은 12개 archetype만 필요하다.

| archetype | 설명 | 좋은 support category |
|---|---|---|
| `projectile_spell` | 탄을 쏘는 주문 | projectile_count, projectile_path, trigger |
| `melee_sweep` | 가까운 적 범위 타격 | area_shape, cooldown, leech_recovery |
| `aura_pulse` | 주변 주기 피해 또는 버프 | area_scale, duration, resource |
| `minion_summon` | 자동 소환수 유지 | minion, trigger, defense |
| `trap_zone` | 바닥에 지속 위험 생성 | duration, area_shape, trigger |
| `beam_channel` | 한 방향 지속 공격 | targeting, cooldown, self_risk |
| `curse_mark` | 적에게 약화/보상 표식 | targeting, duration, loot_utility |
| `shield_skill` | 방어막/반격 생성 | defense, trigger, leech_recovery |
| `dash_strike` | 이동과 공격 결합 | movement, cooldown, ailment |
| `totem_device` | 고정 장치 소환 | minion, area_scale, duration |
| `meteor_delay` | 지연 후 큰 피해 | targeting, area_scale, sequence |
| `chain_reaction` | 처치/상태이상 확산 | trigger, ailment, projectile_path |

## Behavior Priority

자동전투는 매 tick 아래 순서로 skill을 평가한다.

1. 생존 emergency trigger.
2. player-defined priority가 높은 skill.
3. target condition을 만족한 trigger skill.
4. cooldown이 끝난 일반 skill.
5. resource가 부족한 skill은 skip.

```json
{
  "skill_id": "shield_burst",
  "behavior_priority": 95,
  "trigger_condition": {
    "type": "life_below_percent",
    "value": 35
  },
  "cooldown_ready": true,
  "resource_available": true
}
```

## Support Upgrade Model

Support는 레벨과 품질을 가지되, Prototype에서는 두 축만 쓴다.

- `level`: 수치 효과 증가.
- `socket_tier`: 고급 support 장착 가능 여부.

피할 축:

- 색상/방향/링크 shape.
- support 자체 potential/crafting.
- active skill마다 별도 거대 skill tree.

## UI Requirements

SkillBoard는 아래 정보를 한 화면에 보여야 한다.

- Active skill 4개.
- 각 skill의 support socket 2~5개.
- 적용 중인 support category icon.
- cooldown, targeting, projectile, trigger 변화 요약.
- 중복 제한 또는 tag mismatch 이유.
- 자동전투 행동 우선순위.
- 위험 support가 만든 self-risk.

## Combat Log Requirements

Support는 전투 로그에 원인으로 표시되어야 한다.

```text
00:12.4 Fire Orb cast at Elite Skeleton
00:12.4 Support: Multi Projectile changed projectile count 1 -> 3
00:12.6 Support: Chain bounced to 2 additional targets
00:12.8 Support: On Kill Explosion triggered from burning target
```

로그가 없으면 자동전투 게임에서 support build가 납득되지 않는다.

## Source Mapping

- POE2에서 가져올 것: skill 자체 support socket, spirit-like reservation.
- Undecember에서 가져올 것: skill rune와 link rune의 분리, rune growth.
- Noita에서 가져올 것: sequence와 trigger가 행동을 바꾸는 감각.
- Grim Dawn에서 가져올 것: item-granted trigger와 devotion-like proc.
- Vampire Survivors류에서 가져올 것: 단순한 자동 발동 readability.

## Prototype Cut Line

넣는다:

- Active skill 4개.
- Support socket 2개 시작, 최대 5개.
- 18개 support category.
- Tag compatibility.
- Behavior priority.
- Trigger support.

미룬다:

- Undecember식 방향/색상 board.
- Noita식 완전 주문 프로그래밍.
- POE1식 장비 socket link.
- 스킬별 대형 tree.

