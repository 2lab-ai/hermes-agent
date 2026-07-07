# Last Epoch / Undecember Deep Dive

작성일: 2026-05-25

## 범위와 주의

이 문서는 2026-05-25 기준 공개 웹 자료와 병렬 리서치 결과를 바탕으로 한다.
Last Epoch 세부 규칙은 Official Wiki/커뮤니티 위키 반영 지연 가능성이 있고,
Undecember는 LINE/FLOOR 공식 가이드가 상세하지만 2024~2025 업데이트 날짜가 섞여 있어 시즌/하드모드/카드 수치류는 변동 가능성이 있다.
정확한 드롭률보다 데이터 모델과 설계 구조를 우선한다.

## Last Epoch

### 데이터 모델

- 희귀도: Basic, Magic, Rare, Unique, Set, Legendary, Experimental.
- Magic은 1~2 affix, Rare는 3~4 affix.
- 장비는 base implicit 1~3개, normal affix 0~4개, sealed affix 0~1개를 가질 수 있다.
- 일반 affix는 사실상 prefix 2 + suffix 2 구조다.
- 제작 가능 affix는 T5까지, T6/T7은 드롭 전용 Exalted affix다.
- Exalted item은 최소 하나의 T6/T7 affix를 가진 장비이며 legendary crafting 재료가 된다.
- 핵심 제작 상태값: `ForgingPotential`, `sealed_affix`, `LegendaryPotential`, `WeaversWill`.

### 제작 행동

- Affix Shard로 빈 affix를 추가하거나 기존 affix tier를 올린다.
- Glyph는 제작 결과를 보정한다.
- Rune은 아이템 구조를 바꾸거나 파괴/변환한다.
- 대표 동사:
  - `shatter`: 아이템 파괴, affix shard 회수.
  - `remove_random_affix`: 랜덤 affix 제거 및 shard 획득.
  - `discover`: 빈 슬롯에 랜덤 T1 affix 추가.
  - `reroll_affix_value`: affix roll 재굴림.
  - `reroll_implicit`: implicit 재굴림.
  - `ascend`: 같은 슬롯의 random Unique/Set으로 변환.
  - `duplicate`: 복제하되 양쪽 Forging Potential 0.
  - `seal`: affix를 sealed slot으로 옮겨 수정/제거 불가 상태로 만든다.
- Legendary crafting은 `LP Unique + same base type Exalted`를 합성해 LP 수만큼 Exalted affix를 무작위 전이한다.

### 실패 모델

- 일반 제작 실패는 아이템 파괴가 아니라 Forging Potential 소모/고갈이다.
- FP 0이어도 장비는 착용 가능하지만 더 이상 제작할 수 없다.
- Shattering은 의도적 파괴다.
- Removal은 어떤 affix가 제거될지 모르는 리스크다.
- Legendary crafting은 Exalted item 소모와 원하는 affix가 안 넘어가는 확률 리스크다.
- Dungeon key는 입장 시 소모된다.

### 스킬/패시브/엔드게임

- 최대 5개 스킬을 전문화하고, 각 스킬은 별도 경험치와 skill tree point를 가진다.
- Class passive는 base tree에서 mastery tree로 이어진다.
- Idol은 별도 grid inventory에 넣는 수정 불가 장식물이며 prefix+suffix를 가진다.
- Monolith는 timeline -> echo web -> stability -> boss -> blessing 구조다.
- Echo modifier는 enemy modifier와 보상/위험 누적을 만든다.
- Timeline blessing은 장기 성장 보상이며, timeline별 활성 blessing을 선택한다.
- Dungeon은 key 기반 반복 콘텐츠이며 tier가 난이도/보상을 올린다.

### 목표 게임 UI 요구

- 툴팁:
  - rarity color
  - base implicit roll
  - prefix/suffix 2+2
  - sealed slot
  - affix tier
  - craftable cap vs drop-only tier
  - FP remaining
  - LP/Weaver-like state
  - legendary 재료 적합 여부
- 제작 화면:
  - 현재 affix grid
  - 예상 FP 소모 범위
  - 가능한 행동 only
  - 파괴/소모 경고
  - 결과 로그
  - shard 수량
  - legendary imprint 후보 affix preview

### 목표 게임 추출

- Copy:
  - `ForgingPotential` 기반 제작 수명.
  - 2 prefix/2 suffix + sealed fifth line.
  - drop-only high tier.
  - Unique + Exalted affix imprint.
  - timeline blessing.
- Simplify:
  - Glyph/Rune 종류는 6~8개로 축소.
  - Monolith는 `MapCard + node reward + corruption/danger`로 축소.
- Avoid:
  - sealed, experimental, weaver, set-reforged를 한 번에 모두 넣기.
  - 고급 rune 변형이 너무 많아 UI가 unreadable해지는 것.

제안 모듈:

- `ForgePotential`
- `FourSlotAffixGrid`
- `SealedFifthLine`
- `ExaltedDropLine`
- `LegendImprint`
- `EchoWeb`
- `TimelineBlessing`
- `DungeonKeyGate`

## Undecember

### 데이터 모델

- 장비 타입: weapon, armor, accessory, charm.
- 무기 타입은 사용 가능한 skill rune과 연결된다.
- Armor는 STR/DEX/INT 또는 hybrid 요구치에 따라 armor/dodge/barrier base가 달라진다.
- 희귀도/옵션 수:
  - Normal: base only.
  - Magic: 최대 3 options.
  - Rare: 최대 6 options.
  - Unique: 고정 option.
  - Legendary: 6 enchant options + 2 legendary exclusive options.
  - Ancient: 6 enchant + 2 legendary + 2 ancient exclusive options.
  - Holy: Unique base + holy exclusive option / holy set effect.
- Charm은 별도 규칙:
  - Magic: God’s Blessing value + 1 affix.
  - Rare: blessing + 2~3 affix.
  - Legendary: blessing + 2~3 affix + legendary option.
- item level이 높을수록 enchant에서 더 높은 tier option이 등장한다.
- 옵션은 prefix/suffix 최대 3+3 구조로 읽힌다.
- Authority는 12 Gods 계열 별도 축이다.

### 제작 행동

- Essence 기반 동사:
  - grade upgrade
  - option reroll
  - option count add
  - value reroll
  - remove 1 option
  - quality reroll
  - prefix-only reroll/remove
  - suffix-only reroll/remove
  - legendary/ancient/holy upgrade/imbue/reversion
  - authority imbue
  - tier preserving reroll
  - charm grade/value/tier/option change
- Repeat Settings:
  - 원하는 option type, tier, 포함 option 수를 조건으로 설정한다.
  - 조건 충족까지 반복 제작한다.
  - UI에 확률과 prefix/suffix 충돌 제약을 보여준다.
- Transfer:
  - gear/rune의 grade와 enchant state를 다른 item으로 이동한다.
  - material item/rune은 파괴된다.
  - transfer 받은 장비는 재transfer 불가.
  - partial transfer는 일부 prefix/suffix를 확률 전이한다.

### 실패 모델

- 기본 enchant는 item destruction보다 essence 소모와 option overwrite가 중심이다.
- Legendary로 올리면 기존 option은 더 이상 enchant 변경 불가다.
- Transfer는 source destruction이 핵심 비용이다.
- Lacrima는 장비를 장착하지 않고 효과를 흡수하지만, Lacrima 제거/교환 시 등록 gear가 파괴되는 강한 비용 모델을 가진다.

### 스킬/패시브/엔드게임

- Skill Rune은 hexagonal skill item이며 최대 6방향 link slot을 가진다.
- Link Rune은 support rune이며 color+tag가 맞아야 효과가 적용된다.
- White slot은 color restriction을 무시한다.
- Rune Cast는 skill/link/runestone을 배치하는 보드다.
- Runestone은 특정 위치 skill rune을 강화하고 최대 3개 장착한다.
- Rune growth는 gold+elements로 진행되며 EXP transfer가 있다.
- Zodiac은 stat points와 trait points로 구성된다.
- Charm은 Chaos Statue level에 따라 slot이 열리고 God’s Blessing total이 effect를 활성화한다.
- Chaos Dungeon은 Chaos Card로 생성되는 one-time instance dungeon이다.
- Chaos Card는 tier/grade/options/reward/mission을 가진다.
- Chaos Statue는 card tier limit, difficulty, card growth, mission, reward progression을 묶는 엔드게임 허브다.

### 목표 게임 UI 요구

- 아이템 툴팁:
  - grade
  - item level
  - max option count
  - prefix/suffix count
  - option tier
  - authority type
  - legendary/ancient/holy locked state
  - transfer eligibility
  - charm blessing value
  - lacrima absorb rate
- 제작 화면:
  - repeat 조건: type/tier/count
  - 남은 essence 수량
  - option pool chance
  - prefix/suffix 충돌
  - authority 적용 시 기존 옵션 변경 경고
  - legendary upgrade 이후 변경 불가 경고
- Rune 화면:
  - skill rune shape
  - link direction/color
  - tag match 여부
  - inactive link warning
  - rune level/grade
  - transfer material destruction preview
- Map/Card 화면:
  - card tier/grade/options
  - monster modifiers
  - player debuffs
  - reward lines
  - statue level/EXP
  - event slots
  - entrance cost

### 목표 게임 추출

- Copy:
  - repeat enchant 조건 저장.
  - prefix/suffix partial transfer.
  - rune-link color/tag socketing.
  - Chaos Card as map key.
  - Statue as endgame account progression.
  - charm blessing threshold.
  - Lacrima-like 보조 장비.
- Simplify:
  - 희귀도는 `Normal/Magic/Rare/Legendary/Relic` 정도로 축소.
  - 12 Gods authority는 6속성/6진영으로 축소.
  - Essence 이름은 동사 기반으로 통합.
- Avoid:
  - material destruction + paid recovery 느낌의 구조.
  - 너무 많은 essence 이름.
  - link color/tag mismatch인데 장착은 가능하고 효과가 없는 함정.

제안 모듈:

- `RuneSocketBoard`
- `LinkTagMatrix`
- `RepeatForgeRules`
- `AuthorityMark`
- `PartialTransfer`
- `CharmBlessingGrid`
- `LacrimaEchoGear`
- `ChaosCardGate`
- `StatueMastery`

## 통합 권고

목표 게임의 핵심 골격은 Last Epoch식 "읽기 쉬운 affix grid + FP 실패 모델"을 장비 코어로 쓰고,
Undecember식 "반복 제작 조건 + Rune/Link skill setup + 카드형 맵키"를 빌드/엔드게임 층에 얹는 것이다.

최소 모듈:

- `GearCore`: rarity, base, 2 prefix/2 suffix, tier, locked/sealed.
- `ForgePotential`: 실패는 파괴가 아니라 craft budget 소진.
- `RuneLoadout`: 자동전투 skill 3~5개 + link rune 1~3개씩.
- `PassiveConstellation`: Undecember Zodiac보다 작고 Last Epoch skill tree보다 넓은 계층형 노드.
- `MapCardEngine`: card tier/affix/reward/mission + statue level.
- `BlessingRelic`: Monolith blessing + charm blessing의 결합.

피해야 할 것:

- POE급 currency 폭증을 다시 만드는 것.
- Undecember의 전이/부분전이/권능/라크리마/고대/성물 전체를 한 번에 노출하는 것.
- 8-bit 화면에서 확률표를 숨기는 것.
- 반복 제작에서 목표 조건, 예상 소모, 중단 조건, 파괴 여부를 한 화면에 못 보여주는 것.

## 소스

- https://lastepoch.com/
- https://lastepoch.fandom.com/wiki/Equipment
- https://lastepoch.fandom.com/wiki/Crafting
- https://lastepoch.fandom.com/wiki/Unique_Equipment
- https://lastepoch.fandom.com/wiki/Skills
- https://lastepoch.fandom.com/wiki/Passives
- https://lastepoch.fandom.com/wiki/Idols
- https://lastepoch.fandom.com/wiki/Monolith_of_Fate
- https://lastepoch.fandom.com/wiki/Dungeons
- https://www.icy-veins.com/last-epoch/crafting-guide
- https://guide.floor.line.games/UD/en_US/detail/1166916752808800098
- https://guide.floor.line.games/UD/en_US/detail/1166917747181300461
- https://guide.floor.line.games/UD/en_US/detail/1166917161526100514
- https://guide.floor.line.games/UD/en_US/detail/1166916574409800978
- https://guide.floor.line.games/UD/en_US/detail/1166916632826400044
- https://guide.floor.line.games/UD/en_US/detail/1166917784809800682
- https://guide.floor.line.games/UD/en_US/detail/1170004138902100096
