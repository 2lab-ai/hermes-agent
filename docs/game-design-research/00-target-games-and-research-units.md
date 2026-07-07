# 하드코어 아이템/크래프팅 오토류 게임 리서치 매트릭스

작성일: 2026-05-25

## 목표

스팀 Windows/Mac에서 동작하는 8비트풍 오토 전투 게임을 전제로 한다.
전투는 Vampire Survivors 계열처럼 자동/시뮬레이션 틱 중심으로 단순화하고,
플레이어의 실제 깊이는 아이템, 장착, 크래프팅, 강화, 특성 트리, 맵 키 선택에 둔다.

핵심 가정은 아이템마다 출신 문법이 다르다는 것이다.
예를 들어 POE형 아이템은 POE식 접사/화폐 제작, 메이플형 아이템은 메이플식 다층 강화,
디아2형 아이템은 디아2식 베이스/소켓/룬워드/큐브 레시피로 성장한다.

## 공통 조사 단위

각 게임을 아래 단위로 쪼개 조사한다.

- `item_taxonomy`: 아이템 분류, 희귀도, 재료/화폐/키/젬/장비 구분
- `equip_slots`: 장착 슬롯, 인벤토리 제약, 부위별 옵션 풀
- `base_item`: 베이스 타입, 요구 조건, implicit, item level, tier
- `affix_model`: prefix/suffix, 옵션 수, 태그, 수치 범위, 고유 옵션
- `crafting_actions`: 추가, 삭제, 재굴림, 잠금, 변환, 업그레이드, 소켓, 타락
- `failure_model`: 실패, 파괴, 하락, 보호, 흔적, 보장/피티
- `skill_system`: 스킬, 젬, 룬, 패시브, 클래스 빌드 정체성
- `tree_system`: 특성 트리, 어센던시, 마스터리, 주얼/보드/별자리
- `endgame_keys`: 맵, 웨이스톤, 던전 키, 보스 키, 던전 모드, 보상 태그
- `economy_sink`: 재화 소각, 장비 소각, 거래, 시즌, 드랍 필터
- `ui_readability`: 툴팁 밀도, 제작 미리보기, 위험 표시, 외부 위키 의존도
- `auto_battle_translation`: 자동 전투에서 해당 시스템을 어떻게 행동/틱/시뮬레이션으로 바꿀지

## 1차 Deep Dive 대상

### Path of Exile 1

조사 이유: 가장 중요한 기준점. 화폐가 곧 제작 동사이고, 맵까지 아이템화되어 있다.

조사 단위:

- `poe1/item_taxonomy`: 장비, 화폐, 젬, 플라스크, 주얼, 지도, 조각, 카드
- `poe1/equips`: 무기/보조무기/갑옷/투구/장갑/신발/장신구/플라스크/주얼 슬롯
- `poe1/affix_model`: normal/magic/rare/unique, implicit/explicit, prefix/suffix 3+3, item level
- `poe1/crafting`: orb, essence, fossil/resonator, harvest, bench, meta-craft, eldritch, influence, fractured/synthesized/corrupted
- `poe1/skill`: skill gem, support gem, socket color, link, gem level/quality
- `poe1/tree`: passive tree, keystone, notable, mastery, jewel socket, ascendancy, atlas tree
- `poe1/maps`: map item, map mod, atlas, fragments, scarab/juice, boss/pinnacle loop
- `poe1/design_translation`: POE 제작 동사를 어느 정도까지 축소할지

1차 결론:

- 복사할 것: `base + implicit + explicit prefix/suffix + item level/tier`, 화폐를 제작 동사로 쓰기, 맵/키 아이템화.
- 줄일 것: 모든 리그 제작을 한 번에 넣지 말고 `Orb`, `Essence`, `Bench`, `Corruption`, `Map craft`부터.
- 피할 것: 외부 위키 없이는 기대 결과를 알 수 없는 제작, 무작위 chaos spam만 남는 구조.

### Path of Exile 2

조사 이유: POE1의 복잡도를 줄이고 스킬 젬/장비 소켓을 분리한 최신 변형.

조사 단위:

- `poe2/item_taxonomy`: equipment, currency, flasks, jewels, skill gems, waystones, relics, socketables
- `poe2/equips`: 무기/off-hand/armour/jewellery/trinket, 장비 소켓과 rune/soul core
- `poe2/crafting`: transmutation/alchemy/regal/exalted/annul/chaos/essence/omen/rune
- `poe2/skill`: skill gem 자체 support socket, support 중복 제한, spirit reservation
- `poe2/tree`: passive tree, weapon set specialization, ascendancy, endgame passive
- `poe2/maps`: waystone, atlas node, encounter/tablet, boss key
- `poe2/design_translation`: 자동전투에는 POE2식 "스킬 카드에 support를 꽂는 구조"가 더 적합한지 검토

1차 결론:

- 복사할 것: 장비 링크 대신 스킬 자체에 support socket을 붙이는 방식.
- 줄일 것: POE1식 influence/fossil/harvest 전체 복제.
- 피할 것: Early Access 정보는 패치 변동이 크므로 수치보다 구조만 차용.

### Diablo II / Diablo II: Resurrected

조사 이유: POE와 전혀 다른 "베이스 + 소켓 + 룬워드 + 큐브 레시피" 문법의 기준점.

조사 단위:

- `d2/item_taxonomy`: normal/magic/rare/set/unique/crafted/runeword, rune, gem, jewel, charm
- `d2/equips`: 장비 슬롯, 용병 장비, 벨트, 격자 인벤토리, charm 공간
- `d2/base_item`: low/normal/superior/ethereal, normal/exceptional/elite, 최대 소켓
- `d2/affix_model`: magic prefix/suffix, rare 2~6, crafted 고정+랜덤 affix, item level
- `d2/crafting`: Horadric Cube, crafted item families, socket recipes, upgrade recipes, reroll recipes, gambling, imbue
- `d2/runewords`: 정확한 베이스 타입, 소켓 수, 룬 순서, non-magic 조건
- `d2/skill`: 클래스별 3탭, synergy, +skills, aura/proc/charge/item-granted skill
- `d2/endgame`: boss run, cow level, terror zone, uber key, ladder reset
- `d2/design_translation`: 자동전투에서 룬워드가 행동 규칙을 바꾸게 만들기

1차 결론:

- 복사할 것: 룬워드, crafted family, base upgrade, charm loadout, cube recipe로 여는 고밀도 파밍맵.
- 줄일 것: 룬 33종과 외워야 하는 레시피 수.
- 피할 것: 필수 룬워드가 모든 rare/unique를 죽이는 상황.

### MapleStory

조사 이유: 한 아이템에 여러 독립 강화 레이어를 누적하는 대표 사례.

조사 단위:

- `maple/item_taxonomy`: weapon, secondary, armor, accessory, set equipment
- `maple/equips`: 직업별 보조무기, 슬롯별 잠재 옵션 풀, 세트 보너스
- `maple/scroll`: 주문서/Spell Trace, 업그레이드 슬롯, Innocence/Clean Slate/Golden Hammer
- `maple/starforce`: 별 강화, 비용, 실패, 하락, 파괴, Equipment Trace
- `maple/potential`: Rare/Epic/Unique/Legendary, main/additional potential, cubes, tier-up guarantee
- `maple/flame`: bonus stats, rebirth flame, 드랍 순간 추가옵션
- `maple/economy`: meso sink, cube/flame/scroll sink, cash-system risk
- `maple/design_translation`: 프리미엄 Steam 게임용으로 현금 큐브를 플레이 재료/보장으로 변환

1차 결론:

- 복사할 것: 슬롯별 옵션 풀, 드랍 보너스, 잠재 2~3줄, 파괴 시 흔적/이전.
- 줄일 것: 주문서/별/잠재/에디셔널/플레임/소울을 모두 초반부터 넣는 것.
- 피할 것: 현금 큐브형 무한 재굴림.

### Lineage 1

조사 이유: 단순한 `+N` 강화 표기와 강한 파괴 리스크가 아이템 서사를 만드는 사례.

조사 단위:

- `lineage1/item_taxonomy`: weapon, armor, accessory, scroll, material
- `lineage1/equips`: 무기, 투구, 갑옷, 티셔츠, 부츠, 망토, 장갑, 방패/가더, 반지, 목걸이, 귀걸이
- `lineage1/enchant`: 안전 강화선, 일반/축복/저주 주문서, +1/+1~3/-1
- `lineage1/failure`: 안전선 이후 파괴, 예외 재질, 보호/복구의 부재 또는 제한
- `lineage1/economy`: 장비 소각, 주문서 소각, 고강 장비 시장, 거래 리스크
- `lineage1/design_translation`: 안전선은 도입하되 완전 소실은 엔드게임 선택지로 제한

1차 결론:

- 복사할 것: `+N` 표기, 안전선, 축복 점프, 저주 -1 조정.
- 줄일 것: 장비 완전 소실의 빈도.
- 피할 것: Steam 프리미엄 게임에서 보호 없는 파괴형 강화가 기본 루프가 되는 것.

## 2차 우선 조사 후보

### Torchlight: Infinite

조사 이유: POE의 영향을 받았지만 모바일/시즌 ARPG식 자동 제작, affix tier, ember류 재료 문법이 다르다.

조사 단위:

- `tli/item_taxonomy`: gear, affix, trait/card, hero relic/memory, crafting material
- `tli/equips`: 장비 슬롯, hero trait와 장비 상호작용
- `tli/crafting`: prototype crafting, targeted affix, ember/flame sand, tier breakpoints
- `tli/endgame`: Netherrealm, map-like stages, 시즌 mechanic
- `tli/design_translation`: 자동 제작 UI와 affix 목표 설정을 어떻게 가져올지

우선순위: Medium. 자동 발동/지원 스킬 설계는 중요하지만, 제작 시스템은 시즌 변화와 비공식 자료 의존이 커서 보조 참고가 적절하다.

### Last Epoch

조사 이유: POE보다 훨씬 읽기 쉬운 deterministic-ish forge 시스템. `Forging Potential`은 제작 횟수 제한으로 매우 유용하다.

조사 단위:

- `le/item_taxonomy`: common/magic/rare/exalted/unique/set/legendary
- `le/affix_model`: prefix/suffix, affix shard, sealed affix, experimental affix
- `le/crafting`: forge, forging potential, shard, glyph, rune, shattering/removal/chaos/order/despair
- `le/legendary`: Legendary Potential, exalted affix transfer
- `le/endgame`: monolith, echo rewards, target farming
- `le/design_translation`: 아이템마다 제작 예산을 주는 구조

우선순위: Deep Dive. POE식 복잡도를 줄이는 데 가장 직접적으로 유용.

### Grim Dawn

조사 이유: 부위별 component/augment와 Devotion이 장비 밖 빌드 레이어를 만든다.

조사 단위:

- `gd/item_taxonomy`: magic/rare/epic/legendary/monster infrequent/component/augment/blueprint
- `gd/equips`: 장비 슬롯, component 1개, augment, faction gear
- `gd/crafting`: blacksmith, blueprint, affix craft/gambling, relic craft
- `gd/tree`: dual mastery, devotion constellation, item-granted skill
- `gd/design_translation`: 자동전투용 장비 밖 별자리/컴포넌트 레이어

우선순위: Medium. 제작보다 item skill, auto-cast trigger, component/devotion 연결을 조사한다.

### Undecember

조사 이유: 스킬 룬/링크 룬/장비 인챈트가 POE와 비슷하지만 별도 UX와 BM 리스크가 있다.

조사 단위:

- `undecember/item_taxonomy`: gear, skill rune, link rune, essence/currency
- `undecember/crafting`: enchant, option birth/change/expand, authority, quality
- `undecember/skill`: skill rune board, link rune 방향/색, zodiac
- `undecember/design_translation`: 스킬 보드와 자동전투 행동 조합 가능성

우선순위: Deep Dive. 장비 제작, 스킬 룬/링크 룬, 참/축복, 조디악, 이전/계승이 목표 게임의 핵심 표면과 많이 겹친다.

### Chronicon

조사 이유: 2D 픽셀 ARPG에 가까운 시각/스케일 참조. 아이템 옵션 재굴림/강화/룬/인챈트가 가볍다.

조사 단위:

- `chronicon/item_taxonomy`: gear rarity, set, rune, enchant
- `chronicon/crafting`: transmutation, enchant/reroll, augment, socket/rune
- `chronicon/endgame`: anomaly, difficulty scaling
- `chronicon/design_translation`: 픽셀 자동전투 UI 밀도 기준

우선순위: Medium. 그래픽/스코프 감각 확인용.

### Siralim Ultimate

조사 이유: 자동전투/파티 빌드/장기 파밍이 목표 장르와 매우 가깝다. 크리처, trait, artifact, spell gem이 빌드 회로처럼 맞물린다.

조사 단위:

- `siralim/creatures`: 크리처 6마리 파티, trait, fusion, build role
- `siralim/artifact`: artifact slot, socket, material, trait extraction
- `siralim/spell_gem`: 자동전투에서 주문/트리거를 장착형 자원으로 쓰는 방식
- `siralim/endgame`: realm, project, long-tail unlock, 파밍 루프
- `siralim/design_translation`: 아이템 대신 "유닛+유물+트리거"가 빌드 본체가 되는 구조

우선순위: Deep Dive. 자동 시뮬레이션 전투에 가장 직접적으로 맞는 비-POE 계열이다.

## 3차 심화 조사 후보

### Backpack Battles / Backpack Hero / God of Weapons

조사 이유: 자동전투와 아이템 배치 퍼즐이 직접 연결된다. 아이템의 모양, 위치, 인접 조건, 레시피가 곧 전투 성능이 된다.

조사 단위:

- `backpack/shape`: 아이템 칸, 회전, 충돌, 가방 확장, 보관함
- `backpack/adjacency`: 직교/대각/행/열/소켓/태그 기반 연결
- `backpack/recipe`: 인접 재료, 촉매, 잠금, 발견 상태, 실루엣 힌트
- `backpack/combat`: 웨이브 시작 snapshot, 쿨다운, 인접 보너스, 태그 시너지
- `backpack/design_translation`: 전체 인벤토리가 아니라 `CharmGridBoard`로 축소

우선순위: Deep Dive. Prototype 보조 빌드 표면으로 바로 검증 가능하다.

### Noita / Magicraft

조사 이유: 아이템이 affix 묶음이 아니라 좌->우로 실행되는 주문 프로그램이 된다.

조사 단위:

- `wand/chassis`: mana, recharge, cast delay, capacity, spread, shuffle
- `wand/spell_queue`: projectile, modifier, multicast, trigger, timer, payload
- `wand/compile`: scope bracket, wrap 제한, deterministic RNG stream, fixed tick bytecode
- `wand/ui`: 슬롯 줄, always-cast 고정 슬롯, 예상 발사 패턴 preview
- `wand/design_translation`: V1 고급 스킬 아이템으로 격리

우선순위: Deep Dive. 하드코어 깊이는 높지만 가독성 리스크가 커서 Prototype에서는 일부만 쓴다.

### Warframe / The Slormancer

조사 이유: mod capacity, polarity, negative affix compensation, weapon identity evolution이 POE affix와 다른 장기 투자 문법을 만든다.

조사 단위:

- `mod/capacity`: capacity, drain, slot, polarity, rank
- `mod/risk_reward`: negative option, compensation scalar, blocked build tag
- `weapon/identity`: 고유 무기 효과, XP, kill milestone, evolution, opt-in malediction
- `weapon/reforge`: preview, locked stat, possible roll range
- `weapon/design_translation`: V1 장비 투자층

우선순위: Deep Dive. 라이브서비스 반복은 버리고 구현 원자만 추출한다.

### Caves of Qud

조사 이유: data disk, bits, item mod cap이 작고 단단한 레시피/분해/개조 루프를 만든다.

조사 단위:

- `qud/data_disk`: 레시피 발견, 사용 후 영구 제작법
- `qud/bits`: 분해 자원, 보장 회수, 랜덤 회수
- `qud/item_mod`: mod slot cap, 적용 제한, bit cost
- `qud/design_translation`: `RecipeUnlock`과 `SalvageResource`의 기준

우선순위: Deep Dive. Prototype 제작 경제에 바로 반영 가능하다.

### Warframe

조사 이유: 장비 자체보다 mod, capacity, polarity, fusion, riven이 빌드의 본체다. POE식 affix와 완전히 다른 "슬롯 예산 퍼즐"을 준다.

조사 단위:

- `warframe/mods`: mod slot, capacity, polarity, fusion, forma
- `warframe/riven`: 랜덤 옵션 재굴림, disposition, 무기별 고유 빌드
- `warframe/valence`: 중복 장비 흡수형 상한 추격
- `warframe/foundry`: blueprint, crafting time/resource, part farming
- `warframe/design_translation`: 장비에 꽂는 카드형 빌드와 용량 제약

우선순위: Deep Dive. 장비 affix가 아니라 "장비에 장착하는 빌드 카드" 관점에서 반드시 비교한다.

### Monster Hunter World/Rise/Sunbreak/Wilds

조사 이유: 드랍 affix보다 몬스터 재료, 장비 제작, armor skill, decoration, talisman 조합이 빌드를 만든다.

조사 단위:

- `mh/materials`: 몬스터 부위/희귀 재료, 장비 트리
- `mh/equips`: weapon tree, armor skill, set bonus, decoration slot, charm/talisman
- `mh/crafting`: upgrade path, augmentation, qurious crafting, decoration grind
- `mh/endgame`: 보스별 재료 타깃 파밍, 난이도별 장비 갱신
- `mh/design_translation`: 맵/보스별 재료가 특정 아이템 문법을 열게 만들기

우선순위: Deep Dive. 목표 게임의 "자동 보스런 -> 재료 -> 장비 문법 해금" 구조에 유용하다.

### Noita

조사 이유: 아이템이 stat stick이 아니라 실행 문법이다. wand가 spell list를 순서대로 해석하고 modifier/multicast/trigger가 행동을 만든다.

조사 단위:

- `noita/wands`: wand stats, cast delay, recharge, mana, shuffle, capacity
- `noita/spells`: projectile, modifier, multicast, trigger, timer, utility
- `noita/failure`: 자기 피해, 오작동, 조합 위험
- `noita/design_translation`: 자동전투 스킬 젬/룬을 "아이템 내부 프로그램"으로 만들 수 있는지

우선순위: Deep Dive. 물리 시뮬레이션 전체는 가져오지 않더라도, 스킬 조합 문법은 강하게 참고한다.

### Terraria

조사 이유: 2D/레트로 감성, 긴 crafting chain, accessory fusion, reforging이 목표 톤과 잘 맞는다.

조사 단위:

- `terraria/accessory`: accessory slot, modifier/reforge, utility stacking
- `terraria/crafting`: station tiers, material chains, boss-gated progression
- `terraria/progression`: hardmode 전환, biome/boss gated item pool
- `terraria/design_translation`: 액세서리 합성과 간단 affix 재굴림을 장기 목표로 쓰기

우선순위: Deep Dive. POE와 다른 "재료 체인 + 액세서리 합성" 문법으로 가치가 크다.

### Backpack Hero / Backpack Battles

조사 이유: 아이템 배치와 인접 시너지가 전투 로직이 되는 사례.

조사 단위:

- `backpack/item_space`: 공간/형태/인접 조건
- `backpack/synergy`: 조합, 합성, 트리거, 쿨다운
- `design_translation`: charm board 또는 relic board로 제한 도입

우선순위: Deep Dive. 전체 장비 시스템을 복제하지는 않더라도, 공간형 장비 슬롯과 인접 시너지는 목표 게임의 charm/relic board 후보로 중요하다.

## 3차 Medium 후보

### Black Desert Online

조사 이유: failstack, Cron Stone, Caphras처럼 실패 확률/보호/누적 성장 문법이 강하다.

조사 단위:

- `bdo/enhancement`: PRI/DUO/TRI/TET/PEN, failstack, cron, downgrade, destruction
- `bdo/caphras`: 누적 재료 투입으로 단계 성장, 일부 회수
- `bdo/design_translation`: 고위험 강화의 보호/누적 보상 설계

우선순위: Medium. F2P 경제를 그대로 복제하지 말고 실패 보정만 추출.

### Lost Ark

조사 이유: honing, engraving, ability stone은 연구 가치가 있지만 raid MMO vertical treadmill 의존도가 크다.

조사 단위:

- `lostark/honing`: 장비 단계 강화, 재료, 확률/보조 재료, pity
- `lostark/engraving`: 각인 조합, 책/액세서리/어빌리티 스톤
- `lostark/ability_stone`: 성공확률 기반 positive/negative node 깎기
- `lostark/design_translation`: 작은 미니게임형 강화 실패 모델

우선순위: Medium. Ability Stone faceting 중심으로만 조사한다.

### Deep Rock Galactic: Survivor

조사 이유: 자동전투 장르 안에서 weapon upgrade/overclock을 쓰는 최신 참고점.

조사 단위:

- `drgs/weapons`: 자동 발사 무기, weapon level, stat upgrade
- `drgs/overclocks`: 무기 행동 변형, milestone unlock
- `drgs/meta`: class/subclass/mastery/permanent upgrade
- `drgs/design_translation`: 자동전투 중 선택지가 장기 아이템 파밍과 어떻게 연결될지

우선순위: Medium. 전투 루프와 장기 장비 루프 연결용.

### Vampire Survivors / Halls of Torment

조사 이유: 자동전투 기본 루프, 무기 진화, 패시브 조합, 메타 해금의 기준.

조사 단위:

- `vs/weapons`: 자동 발사, level-up choice, weapon rarity, passive item
- `vs/evolution`: weapon + passive + chest 조건
- `hot/items`: 장비 슬롯, chest item, retrieval/unlock, traits
- `design_translation`: 짧은 런 중 빌드 선택과 장기 아이템 제작의 연결

우선순위: Reference Only. 딥 아이템 후보는 아니고 자동전투 UX, 무기 진화, 메타 진행 대비군으로만 사용한다.

### Old School RuneScape / RuneScape

조사 이유: 장비 제작 스킬, 재료 가공, item sink, 장기 경제 참고.

조사 단위:

- `rs/skills`: smithing/crafting/fletching/runecrafting
- `rs/item_sink`: high alchemy, degradation, repair, charges
- `design_translation`: 전투 외 제작 숙련을 넣을지 여부

우선순위: Medium. 장비 제작보다 스킬 XP, 재료 시장, 완제품 소비 경제만 참고한다.

### Borderlands

조사 이유: 총기 manufacturer, part roll, anointment 같은 "드랍 순간 빌드 정체성" 참고.

조사 단위:

- `borderlands/gun_parts`: manufacturer, parts, rarity, prefix
- `borderlands/anointment`: build-specific bonus
- `design_translation`: 아이템 원산지별 문법 분리

우선순위: Medium. 제작은 약하지만 part/anointment/mayhem식 드랍 변형은 "같은 이름의 아이템도 계속 파밍할 이유"를 만든다.

## 제외 또는 보류

- Diablo III: Kanai's Cube, legendary power extraction은 참고하되 D2보다 우선순위 낮음.
- Diablo IV: Tempering/Masterworking는 참고 가치가 있지만 현재 패치 의존도가 큼. D2/Last Epoch 이후.
- EVE Online: 제작/경제는 깊지만 자동전투 ARPG 아이템 문법과 거리가 너무 큼.

## 병렬 리서치 배치

현재 1차 배치:

- Batch A: `poe1/*`, `poe2/*`
- Batch B: `d2/*`, Diablo-family adjacent lessons
- Batch C: `maple/*`, `lineage1/*`
- Batch D: `torchlight_infinite/*`, `last_epoch/*`, `grim_dawn/*`, `chronicon/*`, `undecember/*`
- Batch E: `other_candidates/*`: Warframe, Monster Hunter, BDO, DRG Survivor, Vampire Survivors, Halls of Torment, Backpack 계열, Siralim 등

다음 산출물:

- `01-poe1-poe2.md`: POE1/2 상세 리서치와 target-game 설계 추출
- `02-diablo2.md`: 디아2 상세 리서치와 룬워드/큐브 설계 추출
- `03-maplestory-lineage1.md`: 메이플/리니지 강화 설계 추출
- `04-other-arpgs.md`: Torchlight: Infinite, Last Epoch, Grim Dawn, Chronicon, Undecember 우선순위
- `05-non-poe-candidates.md`: Siralim, Warframe, Monster Hunter, Noita, Terraria, Backpack, BDO, Lost Ark 등 최종 채택/보류
- `10-target-game-system-draft.md`: 목표 게임용 통합 아이템 문법 초안

## 현재 기준 소스 앵커

- Path of Exile 공식 게임 소개: https://www.pathofexile.com/game
- PoE Wiki Crafting: https://www.poewiki.net/wiki/Crafting
- PoE Wiki Atlas of Worlds: https://www.poewiki.net/wiki/Atlas_of_Worlds
- PoE2 Wiki Crafting: https://www.poe2wiki.net/wiki/Crafting
- PoE2 Wiki Waystone: https://www.poe2wiki.net/wiki/Waystone
- Diablo II Arreat Summit Items: https://classic.battle.net/diablo2exp/items/
- Diablo II Arreat Summit Horadric Cube: https://classic.battle.net/diablo2exp/items/cube.shtml
- Diablo II Arreat Summit Rune Words: https://classic.battle.net/diablo2exp/items/runewords.shtml
- Wowhead D2R Horadric Cube guide: https://www.wowhead.com/diablo-2/guide/horadric-cube-recipes
- Wowhead D2R Runewords guide: https://www.wowhead.com/diablo-2/guide/runewords-types-bonuses-sockets
- Nexon MapleStory Star Force support: https://support-maplestory.nexon.com/hc/en-us/articles/204088639-How-do-I-enhance-equips-with-Star-Force
- Nexon MapleStory Spell Traces support: https://support-maplestory.nexon.com/hc/en-us/articles/204744535-What-are-Spell-Traces
- MapleStory Wiki Potential: https://maplestorywiki.net/w/Potential
- MapleStory Wiki Star Force: https://maplestorywiki.net/w/Star_Force_Enhancement
- Lineage Open Wiki Enchanting: https://lineage-open.fandom.com/wiki/Enchanting
- Last Epoch Wiki Crafting: https://lastepoch.fandom.com/wiki/Crafting
- Last Epoch 공식 skills/endgame: https://lastepoch.com/skills/ , https://lastepoch.com/end-game/
- Grim Dawn official crafting guide: https://www.grimdawn.com/guide/items/crafting/
- Grim Dawn official Devotion guide: https://www.grimdawn.com/guide/character/devotion
- Undecember official gear/rune guides: https://guide.floor.line.games/UD/en_US/detail/1166916752808800098 , https://guide.floor.line.games/UD/en_US/detail/1166916549917300337
- Torchlight: Infinite official data: https://torchlight.xd.com/en/data
- Siralim Ultimate Steam/wiki: https://store.steampowered.com/app/1289810/Siralim_Ultimate/ , https://siralimultimate.wiki.gg/wiki/Artifacts
- Warframe official mod guide: https://www.warframe.com/news/mods-guide
- Monster Hunter Rise official manual: https://game.capcom.com/manual/MHRISE/en/steam/page/9/1
- Noita wiki wand mechanics: https://noita.wiki.gg/wiki/Guide:_Wand_Mechanics
- Terraria official wiki modifiers/accessories: https://terraria.wiki.gg/wiki/Modifiers , https://terraria.wiki.gg/wiki/Accessories
- Black Desert official Caphras Enhancement: https://www.naeu.playblackdesert.com/en-us/Wiki?wikiNo=146
- DRG Survivor official wiki weapons: https://deeprockgalactic.wiki.gg/wiki/Survivor:Weapons
- Vampire Survivors Wiki weapons: https://vampire-survivors.fandom.com/wiki/Weapons
