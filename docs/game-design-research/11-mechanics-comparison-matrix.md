# 메커닉 비교 매트릭스

작성일: 2026-05-25

이 문서는 각 게임을 "목표 게임에 넣을 수 있는 모듈" 단위로 비교한다.
목표는 모든 원작 시스템을 복제하는 것이 아니라, 아이템 출신별로 서로 다른 제작 문법을 만들 때 필요한 설계 원자를 뽑는 것이다.

## 비교 축

- `data_model`: 아이템/스킬/장비가 어떤 상태값을 갖는가.
- `craft_actions`: 플레이어가 어떤 동사를 수행하는가.
- `failure_cost`: 실패가 무엇을 소모하거나 망가뜨리는가.
- `build_depth`: 전투 조작이 적어도 빌드 깊이가 생기는 이유.
- `ui_must_show`: 자동전투 게임의 제작/툴팁 UI에 반드시 보여야 하는 정보.
- `target_module`: 목표 게임에서의 모듈명.
- `priority`: Prototype, V1, Later, Reference.

## 핵심 ARPG/강화 게임

| 게임 | data_model | craft_actions | failure_cost | build_depth | target_module | priority |
|---|---|---|---|---|---|---|
| Path of Exile 1 | base, item level, rarity, implicit, prefix/suffix, influence/special state, corruption | rarity upgrade, reroll, add/remove affix, tag-guaranteed reroll, bench craft, corrupt, map craft | currency loss, bad affix, irreversible corruption, possible brick | affix 조합과 crafting route가 빌드 성능을 결정 | `PoeAffixWorkbench` | Prototype |
| Path of Exile 2 | equipment, skill gem support sockets, rune/soul core sockets, waystone | simpler orb crafting, essence, omen, rune socketing, waystone modification | currency loss, early-access volatility, waystone failure pressure | 장비 링크보다 skill gem 자체가 빌드 표면 | `SkillSupportBoard`, `WaystoneMapKey` | Prototype |
| Diablo II | base quality, socket count, rune/gem/jewel, runeword state, crafted family | socket, insert rune, validate runeword, cube recipe, base upgrade, crafted item recipe | wrong runeword input, consumed socket materials, recipe opportunity cost | 베이스 선택과 룬 조합이 목적형 전설을 만든다 | `RunewordForge`, `CubeRecipeBook` | Prototype |
| MapleStory | equipment slot, upgrade slots, starforce, flame, potential, trace | scroll/spell trace, starforce, cube, flame, transfer trace | slot loss, meso/material loss, star drop, destruction with trace | 한 장비에 독립 성장 레이어가 누적된다 | `LayeredEnhancementBench` | Prototype |
| Lineage 1 | base item, enchant level, safe limit, scroll type | safe enchant, over-enchant, blessed jump, cursed downgrade | scroll loss, item destruction after safe line | 단순한 `+N` 표기가 아이템 서사를 만든다 | `RiskEnchantBench` | Prototype |
| Last Epoch | affix slots, shards, glyph/rune, forging potential, exalted/sealed affix | add/upgrade affix, remove, seal, shatter, reroll value, legendary transfer | forging potential depletion, item shatter, lost crafting life | 아이템마다 제작 수명이 있어 파괴 없이 긴장감이 생긴다 | `ForgingPotentialForge` | Prototype |
| Undecember | gear grade, prefix/suffix, essence, skill rune, link rune, zodiac, charm blessing | grade change, option reroll, prefix/suffix reroll/removal, repeat enchant, rune link/growth, transfer | essence loss, result churn, legendary lock, transfer destroys source | 장비/스킬룬/참/조디악이 분리된 성장판 | `RuneLinkBoard`, `RepeatEnchantWorkbench` | V1 |

## 비-POE 빌드 문법

| 게임 | data_model | craft_actions | failure_cost | build_depth | target_module | priority |
|---|---|---|---|---|---|---|
| Siralim Ultimate | creature party, trait, artifact, spell gem, artifact socket/trigger | artifact socketing, trait stacking, spell gem setup, creature fusion | build complexity, bad synergy, grind time | 자동전투에서 유닛/유물/트리거가 회로처럼 작동 | `CompanionCircuitBoard` | V1 |
| Warframe | equipment level, mod capacity, mod slot, polarity, mod rank, forma | install mod, fuse mod, polarize slot, capacity expansion, riven reroll | capacity mismatch, forma/time/resource cost, over-specialization | 강한 효과를 넣기 위한 슬롯 예산 퍼즐 | `ModCapacityBoard` | V1 |
| Monster Hunter | material, weapon tree, armor skill, decoration slot, talisman/charm, set bonus | craft gear from monster materials, upgrade tree, slot decoration, augment/qurious | monster grind, rare material bottleneck, RNG augment | 장비 조합이 스킬 레벨 합산표가 된다 | `MaterialGearTree` | V1 |
| Noita | wand stats, spell slots, cast order, modifier, multicast, trigger | arrange spells, combine modifiers/triggers, wand selection | self-damage, chaotic behavior, failed internal program | 아이템이 스킬 실행 문법 자체가 된다 | `ProgrammableSkillItem` | Later |
| Magicraft | wand slots, boost/passive, MP, cast interval, cooldown, scatter | arrange spells left-to-right, bind boost scope, automate wand spirit | MP loop abuse, hidden scope confusion, bad spell order | Noita식 주문 프로그램을 더 자동전투 친화적으로 보여준다 | `SpellProgram` | V1 |
| Terraria | accessory, modifier, crafting station, material chain, boss/biome gate | accessory fusion, reforge, station-tier craft, boss-gated recipe | gold/material cost, reroll variance, progression gate | 액세서리가 계속 합쳐져 장기 목표가 된다 | `AccessoryFusionChain` | V1 |
| Backpack Hero / Battles | item shape, grid position, adjacency, trigger/cooldown | place, rotate, combine, adjacency optimize | board space opportunity cost, UI burden | 위치 자체가 빌드 스탯이다 | `CharmGridBoard` | V1 |
| Caves of Qud | data disk, bits, item mod cap, schematic tier | learn recipe, disassemble, attach limited mods | recipe scarcity, salvage opportunity cost | 레시피 발견과 분해 자원이 작은 제작 경제를 만든다 | `RecipeTraitLab`, `SalvageResource` | Prototype |
| The Slormancer | identity weapon, weapon XP, primordial positive/negative, reforge preview | evolve weapon, toggle risk form, preview/reroll stats | over-specialization, material sink, bad malediction | 무기 자체가 빌드 정체성으로 성장한다 | `IdentityWeaponXP` | V1 |

## Medium / 참고 모듈

| 게임 | 핵심 참고 | target_module | priority |
|---|---|---|---|
| Torchlight: Infinite | activation medium, support skill, 목표 조건 반복 제작 UI | `AutoTriggerSupport`, `CraftUntilRule` | V1 |
| Grim Dawn | component, augment, item-granted skill, devotion trigger | `ComponentSocket`, `DevotionTrigger` | V1 |
| Chronicon | 픽셀 ARPG에서 enchant/gem/rune/crafting UI를 다루는 스케일 | `PixelTooltipBudget` | Reference |
| Black Desert Online | failstack, cron, Caphras 누적 보조 성장 | `PityAndProtectionRail` | Later |
| Lost Ark | ability stone faceting, honing pity | `PositiveNegativeFacet` | Later |
| Borderlands | named item + parts/anointment + mayhem power | `NamedItemVariantRoll` | Later |
| OSRS/RuneScape | 제작물이 장비 가치보다 XP/경제 sink로 소비됨 | `SimulatedCraftEconomy` | Later |
| DRG Survivor | 자동발사 무기 upgrade/overclock | `RunUpgradeToPermanentCraftBridge` | Reference |
| Vampire Survivors | weapon + passive evolution, reroll/skip/banish | `SimpleEvolutionRule` | Reference |
| Halls of Torment | quest unlock, trait/item/ability synergy | `QuestUnlockMetaLayer` | Reference |

## Prototype에 반드시 들어갈 모듈

### 1. `PoeAffixWorkbench`

목표: 하드코어 item affix 제작의 기준.

필수 상태:

- item level
- rarity
- implicit
- prefix slots
- suffix slots
- affix tags
- crafted mod
- corrupted flag

필수 동사:

- rarity upgrade
- reroll all
- add affix
- remove affix
- reroll value
- essence guaranteed tag
- bench craft
- corrupt

UI 필수:

- 현재 prefix/suffix 개수
- 가능한 affix tag
- 잠긴/제작된/타락한 상태
- 사용 후 가능한 결과 범위
- 되돌릴 수 없는 행동 경고

### 2. `RunewordForge`

목표: 베이스와 재료의 순서가 의미 있는 제작.

필수 상태:

- base type
- socket count
- socketed materials
- rune order
- superior/ethereal-like flags

필수 동사:

- add socket
- insert material
- clear socket with material loss
- validate runeword
- upgrade base tier

UI 필수:

- 이 베이스에서 가능한 runeword 목록
- 필요한 소켓 수와 현재 소켓 수
- 순서 오류 경고
- 결과 행동 변형 preview

### 3. `LayeredEnhancementBench`

목표: MapleStory/Lineage식 장기 강화와 단순 `+N` 목표를 결합.

필수 상태:

- enchant level
- safe limit
- star tier
- flame bonus lines
- potential lines
- trace/pity progress

필수 동사:

- safe enhance
- over-enhance
- blessed jump
- cursed downgrade
- reroll potential
- reroll flame
- restore from trace

UI 필수:

- 성공/실패/하락/파괴 확률
- 보장 게이지
- 실패 시 남는 것
- 현재 총 성장 레이어 요약

### 4. `ForgingPotentialForge`

목표: 완전 파괴 없이 제작 긴장감을 만드는 수명 제한.

필수 상태:

- forging potential
- normal affix
- exalted/high-tier affix
- sealed affix
- available shards

필수 동사:

- add affix by shard
- upgrade tier
- remove random affix
- seal affix
- shatter into shards

UI 필수:

- 남은 crafting life
- 이번 craft의 potential cost range
- craft 후 더 이상 수정할 수 없는 위험
- shatter 시 기대 shard

### 5. `SkillSupportBoard`

목표: 자동전투 행동을 수동 조작 대신 빌드로 설계.

필수 상태:

- active skill slots
- support sockets per skill
- support categories
- trigger/cooldown/targeting rules
- reservation or capacity cost

필수 동사:

- socket support
- upgrade support socket count
- swap active skill
- bind trigger condition
- set behavior priority

UI 필수:

- 어떤 support가 어떤 skill에 적용되는지
- cooldown/targeting/area/projectile 변화
- 중복 제한
- 자동전투 행동 우선순위

### 6. `MapKeyCrafting`

목표: 전투 선택 자체를 아이템/제작 루프에 포함.

필수 상태:

- area level
- biome
- monster tags
- danger mods
- reward mods
- origin family bias
- boss fragment progress

필수 동사:

- add danger
- reroll reward
- corrupt key
- bias family drops
- combine boss key fragments

UI 필수:

- 위험 상승과 보상 상승의 교환비
- 자동전투 실패 시 손실과 보상
- 드랍 family bias
- 보스/엔드게임 진행도

## V1에 넣을 모듈

- `RuneLinkBoard`: Undecember식 방향/색상 link rune 보드.
- `ModCapacityBoard`: Warframe식 capacity/polarity/mod rank 퍼즐.
- `MaterialGearTree`: Monster Hunter/Terraria식 보스 재료 제작 트리.
- `CharmGridBoard`: Diablo charm + Backpack adjacency를 결합한 제한 보드.
- `SpellProgram`: Magicraft식 좌->우 자동 완드와 Noita식 queue compile의 축소판.
- `IdentityWeaponXP`: Slormancer식 무기 정체성 성장과 opt-in 부정 옵션.
- `RecipeTraitLab`: Siralim/Qud식 레시피 발견, 분해 bits, trait 부착.
- `ComponentSocket`: Grim Dawn식 장비 보조 부품과 auto-cast trigger.
- `CraftUntilRule`: Torchlight/Undecember식 목표 조건 자동 반복 제작.

## Later로 미룰 모듈

- `ProgrammableSkillItem`: Noita식 내부 프로그램 아이템.
- `CompanionCircuitBoard`: Siralim식 파티/유물/트리거 회로.
- `PityAndProtectionRail`: BDO/Lost Ark식 장기 실패 보정.
- `NamedItemVariantRoll`: Borderlands식 named item part/anointment 변형.
- `SimulatedCraftEconomy`: OSRS식 제작 경제.

## 설계 충돌과 해결

### 충돌: 아이템 패밀리가 너무 많다

해결: Prototype에서는 4개 패밀리만 활성화한다.

- POE형
- D2형
- Maple/Lineage hybrid형
- Last Epoch형

나머지는 드랍은 가능하더라도 "sealed research item"처럼 잠가두거나 V1로 미룬다.

### 충돌: 자동전투인데 제작 UI가 너무 무겁다

해결: 런 중에는 선택지만 가볍게, 런 밖에서 상세 제작을 한다.

- 런 중: 스킬/패시브/임시 강화 선택.
- 런 후: 아이템 식별, 제작, 맵 키 조정, 장비 교체.

### 충돌: 원작별 실패 모델이 서로 다르다

해결: 실패 결과를 5개 공통 카테고리로 표준화한다.

- `resource_loss`: 재료만 사라짐.
- `bad_roll`: 아이템은 남지만 결과가 나쁨.
- `craft_life_loss`: 제작 수명이 줄어듦.
- `tier_loss`: 강화 단계가 하락.
- `item_break`: 아이템이 깨지지만 trace/fragment를 남김.

### 충돌: 툴팁이 읽히지 않는다

해결: 툴팁을 3단으로 나눈다.

- 기본: DPS/생존/자동행동 변화 요약.
- 상세: affix, tier, source, craft state.
- 고급: weight, tag, probability, blocked outcomes.

## 다음 조사 우선순위

1. Prototype 4개 패밀리의 실제 데이터 스키마를 정의한다.
2. 각 패밀리별 craft action을 JSON-like spec으로 정리한다.
3. 실패 모델 공통 enum과 family-specific override를 만든다.
4. 자동전투 스킬 support category를 20개 이하로 제한해 목록화한다.
5. MapKey modifier를 danger/reward/family bias로 나눠 초안화한다.

## 소스 앵커

- POE 공식 게임 소개: https://www.pathofexile.com/game
- POE Crafting Wiki: https://www.poewiki.net/wiki/Crafting
- POE2 Crafting Wiki: https://www.poe2wiki.net/wiki/Crafting
- Diablo II Horadric Cube: https://classic.battle.net/diablo2exp/items/cube.shtml
- Diablo II Runewords: https://classic.battle.net/diablo2exp/items/runewords.shtml
- MapleStory Star Force: https://support-maplestory.nexon.com/hc/en-us/articles/204088639-How-do-I-enhance-equips-with-Star-Force
- MapleStory Potential: https://maplestorywiki.net/w/Potential
- Lineage Enchanting: https://lineage-open.fandom.com/wiki/Enchanting
- Last Epoch Crafting: https://lastepoch.fandom.com/wiki/Crafting
- Undecember Gear: https://guide.floor.line.games/UD/en_US/detail/1166916752808800098
- Undecember Gear Enchants: https://guide.floor.line.games/UD/en_US/detail/1166917747181300461
- Warframe Mods Guide: https://www.warframe.com/en/news/mods-guide
- Siralim Artifacts: https://siralimultimate.wiki.gg/wiki/Artifacts
- Terraria Modifiers: https://terraria.wiki.gg/wiki/Modifiers
- Noita Wand Mechanics: https://noita.wiki.gg/wiki/Guide:_Wand_Mechanics
