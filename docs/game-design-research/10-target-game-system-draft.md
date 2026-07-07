# 목표 게임 통합 시스템 초안

작성일: 2026-05-25

이 문서는 리서치 결과를 목표 게임의 시스템 가설로 합친 것이다.
구현 설계가 아니라 다음 리서치와 프로토타입 범위를 정하기 위한 초안이다.

## 핵심 컨셉

8비트풍 자동 전투 게임이지만, 아이템은 단일 강화 규칙을 쓰지 않는다.
각 아이템은 `origin_family`를 가지고, 출신 문법에 따라 다른 제작 UI와 실패 모델을 사용한다.

예시:

- `poe_item`: prefix/suffix, orb, essence, bench, corruption으로 제작.
- `d2_item`: base, socket, rune, runeword, cube recipe로 제작.
- `maple_item`: flame, starforce, potential, trace로 강화.
- `lineage_item`: safe enchant, blessed/cursed scroll, over-enchant risk로 강화.
- `last_epoch_item`: affix shard, glyph, rune, forging potential로 제작.
- `undecember_skill_rune`: skill rune + link rune + direction/color board로 성장.
- `warframe_modded_item`: capacity, polarity, mod fusion으로 성장.
- `noita_wand_item`: spell list, modifier, trigger, cast order로 행동을 구성.
- `monster_material_item`: 보스 재료와 제작 트리로 성장.

## 플레이 루프

1. 플레이어가 `MapKey`를 선택한다.
2. 자동 전투가 시뮬레이션 틱으로 진행된다.
3. 전투 결과로 장비, 제작 재료, 룬, 젬, 맵 키, 보스 키가 드랍된다.
4. 드랍 아이템은 `origin_family`별로 다른 해석과 제작 UI를 가진다.
5. 플레이어는 장비, 스킬, 특성 트리, 맵 키를 조정한다.
6. 더 위험한 맵 키를 제작/강화해 다음 자동 전투에 투입한다.

## 기본 장착 표면

MVP 장착 슬롯은 10개로 시작한다.

- Weapon
- Offhand 또는 Relic
- Helmet
- Body
- Gloves
- Boots
- Amulet
- Ring 1
- Ring 2
- Belt

별도 보드는 3개만 둔다.

- `SkillBoard`: active skill 4~6개, 각 skill에 support socket.
- `PassiveTree`: 클래스 시작점 1개, 경로 3개, keystone, jewel socket.
- `CharmBoard`: Diablo II charm과 Backpack 계열 공간 시너지를 축약한 제한 보드.

## 아이템 공통 데이터

모든 장비는 최소한 아래 필드를 가진다.

- `id`
- `origin_family`
- `slot`
- `base_type`
- `item_level`
- `rarity`
- `requirements`
- `implicit_mods`
- `explicit_mods`
- `craft_state`
- `bind_state`
- `source_map`
- `history`

`craft_state`는 family별로 다르게 확장한다.

- POE형: prefix/suffix lock, fractured, corrupted, crafted_mod_count.
- D2형: socket_count, socketed_materials, runeword_state, ethereal/superior.
- Maple형: flame, starforce, potential_lines, trace_state.
- Lineage형: enchant_level, safe_limit, blessed_state, cursed_adjustment.
- Last Epoch형: forging_potential, sealed_affix, exalted_affix.
- Warframe형: capacity, polarity_slots, installed_mods.
- Noita형: cast_order, spells, wand_stats.

## 제작 패밀리

### POE형 제작대

목표: 하드코어 접사 제작의 기준점.

MVP 동사:

- normal -> magic
- normal -> rare
- magic -> rare
- reroll magic
- reroll rare
- add affix
- remove random affix
- reroll numeric values
- essence reroll with guaranteed tag
- bench craft 1 mod
- corrupt

제한:

- 초반 rare는 4 affix, 후반 rare는 6 affix.
- 접사 태그는 부위별 8~15개로 제한.
- corruption은 되돌릴 수 없지만 완전 파괴 확률은 낮게 둔다.

### D2형 제작대

목표: 베이스와 소켓이 드랍 가치를 만들게 한다.

MVP 동사:

- add socket
- insert rune/gem/jewel
- remove socketed material, material destroyed
- runeword validate
- base upgrade
- crafted family recipe
- special map recipe

제한:

- 룬은 8~12종으로 시작.
- 룬워드는 슬롯별 2~4개만 둔다.
- runeword가 rare/unique를 죽이지 않도록 행동 변형 중심으로 설계한다.

### Maple형 강화대

목표: 장비 한 개에 여러 장기 성장 레이어를 얹는다.

MVP 레이어:

- `Flame`: 드랍 보너스 1~3줄.
- `Starforce`: +0~+15 단계 강화.
- `Potential`: 2~3줄 옵션, 등급 상승.
- `Trace`: 파괴 또는 실패 누적을 완충하는 흔적.

제한:

- 현금형 cube는 없다.
- 큐브/재굴림은 항상 확률과 보장 게이지를 UI에 보여준다.
- 파괴는 흔적/파편/보장 진척을 남긴다.

### Lineage형 인챈트

목표: `+N` 장비 서사를 만든다.

MVP 동사:

- safe enchant to limit
- over-enchant
- blessed scroll +1~2 jump
- cursed scroll -1 adjust
- protection scroll, 엔드게임에서 제한 공급

제한:

- 완전 소실은 기본 루프가 아니라 high-risk mode로 분리한다.
- 일반 실패는 재료 소모 또는 단계 하락부터 시작한다.

### Last Epoch형 Forge

목표: 제작 실패가 파괴가 아니라 "수정 가능 수명 고갈"이 되게 한다.

MVP 동사:

- add affix by shard
- upgrade affix tier
- reroll affix value
- remove random affix
- seal affix
- shatter item into shards

제한:

- 모든 craft는 `ForgingPotential`을 소비한다.
- 고티어 affix는 드랍 전용으로 남겨 파밍 이유를 만든다.

### Skill Rune / Support Board

목표: 자동전투 행동을 플레이어가 설계하게 한다.

기준 참조: POE2, Undecember, Noita, Grim Dawn.

MVP 구조:

- active skill 4개.
- 각 active skill은 support socket 2개로 시작, 후반 4~5개까지 확장.
- support는 damage뿐 아니라 targeting, cooldown, projectile count, trigger, minion, area, duration을 바꾼다.
- 일부 unique support는 map/boss 보상으로만 나온다.

## 맵 키 시스템

MapKey는 POE map/POE2 waystone/D2 cow recipe/Last Epoch monolith를 합친다.

필드:

- `area_level`
- `biome`
- `monster_tags`
- `danger_mods`
- `reward_mods`
- `origin_bias`
- `boss_key_progress`
- `crafting_material_bias`

제작 동사:

- add danger mod
- reroll reward mod
- corrupt map key
- infuse family bias
- combine fragments into boss key

설계 원칙:

- 전투가 자동이므로 map key 실패는 완전 손실만 남기면 안 된다.
- 실패해도 재료 파편, atlas progress, pity, unlock 중 하나는 남긴다.

## MVP 범위

첫 프로토타입에 넣을 것:

- POE형 장비 제작.
- D2형 소켓/룬워드.
- Maple/Lineage hybrid 강화.
- Last Epoch형 forging potential.
- POE2/Undecember식 skill support board.
- MapKey 제작/강화.
- PassiveTree 축소판.
- 제작법 드랍/연구 도감.
- 장비 분해 자원.
- 제한형 CharmGridBoard.

첫 프로토타입에서 미룰 것:

- Warframe식 polarity/capacity 전체.
- Noita식 wand 내부 프로그램 전체.
- Siralim식 creature party 전체.
- Slormancer식 무기 정체성 진화 전체.
- Monster Hunter식 긴 재료 트리 전체.
- BDO/Lost Ark식 MMO 강화 경제 전체.

## 모듈 우선순위

### Prototype

Prototype은 "여러 게임 문법을 섞을 수 있다"는 핵심 가설을 검증해야 한다.
따라서 시스템 수를 줄이고, 각 문법이 충분히 다르게 느껴지는지에 집중한다.

- `PoeAffixWorkbench`: base, implicit, prefix/suffix, orb, essence, bench, corruption.
- `RunewordForge`: base, socket, rune order, runeword validation, cube recipe.
- `LayeredEnhancementBench`: flame-like drop bonus, +N 강화, potential lines, trace.
- `ForgingPotentialForge`: shard/glyph/rune, crafting life, sealed affix, shatter.
- `SkillSupportBoard`: active skill 4개, support socket, trigger/target/cooldown 변형.
- `MapKeyCrafting`: danger mod, reward mod, family drop bias, boss key fragment.
- `PassiveTreeLite`: 클래스 시작점, 3개 경로, keystone, jewel/charm hook.
- `RecipeUnlockLab`: data disk/blueprint식 제작법 드랍과 연구 도감.
- `SalvageResource`: 장비 분해 -> bits/shards/runes로 이어지는 제작 경제.
- `CharmGridBoard`: `6x5` 제한 보드에서 shape/adjacency/recipe만 검증.

### V1

V1은 빌드 표면을 넓히되, Prototype의 아이템 문법을 깨지 않는 모듈만 추가한다.

- `RuneLinkBoard`: Undecember식 방향/색상 link rune 보드.
- `ModCapacityBoard`: Warframe식 capacity/polarity/mod rank 퍼즐.
- `MaterialGearTree`: Monster Hunter/Terraria식 보스 재료 제작 트리.
- `CharmGridBoard Expansion`: Prototype의 `6x5` 보드를 더 많은 shape/recipe/edge marker로 확장.
- `SpellProgram`: Magicraft식 좌->우 자동 완드와 Noita식 queue compile의 제한판.
- `IdentityWeaponXP`: Slormancer식 무기 정체성 성장과 opt-in 부정 옵션.
- `AttachableTrait`: Siralim/Qud식 trait를 장비/소환수/스킬에 부착.
- `ComponentSocket`: Grim Dawn식 장비 부품과 auto-cast trigger.
- `CraftUntilRule`: Torchlight/Undecember식 목표 조건 자동 반복 제작.

### Later

Later 모듈은 강하지만 스코프와 UI 부담이 크다.

- `ProgrammableSkillItem`: Noita식 내부 프로그램 아이템.
- `CompanionCircuitBoard`: Siralim식 파티/유물/트리거 회로.
- `PityAndProtectionRail`: BDO/Lost Ark식 장기 실패 보정.
- `NamedItemVariantRoll`: Borderlands식 named item part/anointment 변형.
- `SimulatedCraftEconomy`: OSRS식 제작 경제.

## 공통 실패 모델

원작마다 실패 방식이 다르지만 목표 게임 내부에서는 5개 결과로 표준화한다.

- `resource_loss`: 재료만 사라진다.
- `bad_roll`: 아이템은 남지만 결과가 나쁘다.
- `craft_life_loss`: 제작 가능 수명이 줄어든다.
- `tier_loss`: 강화 단계가 하락한다.
- `item_break`: 아이템이 깨지지만 trace/fragment/progress를 남긴다.

패밀리별 매핑:

- POE형: `bad_roll`, `resource_loss`, `item_break` for corruption.
- D2형: `resource_loss`, 잘못된 socket/runeword는 `bad_roll`.
- Maple형: `resource_loss`, `tier_loss`, `item_break` with trace.
- Lineage형: `tier_loss`, high-risk에서만 `item_break`.
- Last Epoch형: `craft_life_loss`, shatter는 의도적 `item_break`.
- Undecember형: `bad_roll`, `resource_loss`, transfer는 source destruction.

## UI 최소 요건

아이템 툴팁은 3단계로 나눈다.

- Basic: DPS/생존/자동행동 변화 요약.
- Detail: affix, tier, source, craft state.
- Advanced: tag, weight/probability, blocked outcomes, expected cost.

제작 화면은 패밀리별로 달라도 아래 정보는 공통으로 보여야 한다.

- 현재 아이템 상태.
- 사용 재료.
- 가능한 결과 범위.
- 실패 결과.
- 되돌릴 수 없는 상태 변화.
- 보장/피티/trace 진행도.

## 다음 산출물 후보

- `12-prototype-data-schema.md`: Prototype 4개 아이템 패밀리의 JSON-like schema.
- `13-craft-actions-spec.md`: family별 craft action, input, output, failure enum.
- `14-skill-support-taxonomy.md`: 자동전투 support category 20개 이하 목록.
- `15-map-key-modifiers.md`: MapKey danger/reward/family-bias modifier 초안.

## 주요 리스크

- 아이템 패밀리가 너무 많으면 게임이 아니라 백과사전이 된다.
- 같은 슬롯에 너무 많은 성장 레이어가 겹치면 툴팁이 읽히지 않는다.
- 자동전투 결과와 제작 선택 사이의 인과가 약하면 플레이어가 왜 졌는지 모른다.
- 완전 랜덤 제작은 하드코어가 아니라 피로가 된다.
- 완전 보호 제작은 장기 목표를 죽인다.
- 드랍 필터가 없으면 POE식 아이템량은 자동전투 게임에서 바로 피로가 된다.

## 다음 리서치 질문

- 아이템 패밀리는 1차 출시에서 몇 개까지 허용할 것인가?
- POE형 접사 태그는 부위별 몇 개가 적정한가?
- 자동전투 스킬은 active skill 4개가 맞는가, 6개가 맞는가?
- 맵 키 실패 보상은 어떤 식으로 남겨야 불공정하지 않은가?
- 고위험 파괴형 강화는 싱글/프리미엄 게임에서 어느 단계 이후부터 허용할 것인가?
- 드랍량과 필터 UI를 어느 시점에 도입해야 하는가?
- Steam Deck/Windows/Mac에서 툴팁과 제작 UI가 읽히는 최소 폰트/패널 밀도는 어느 정도인가?
