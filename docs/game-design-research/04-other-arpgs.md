# Other ARPG 제작·스킬·엔드게임 후보 리서치

작성일: 2026-05-25

## 결론

- Deep Dive: Last Epoch, Undecember.
- Medium: Torchlight: Infinite, Grim Dawn, Chronicon.
- Skip: 없음. 다만 Torchlight는 제작보다 자동 발동 스킬, Grim Dawn은 제작보다 아이템 스킬/Devotion, Chronicon은 픽셀 ARPG 스케일 참고에 집중한다.

## Torchlight: Infinite

### 조사 이유

POE 영향을 받았지만 시즌 ARPG, 모바일/PC UX, 자동 제작, support skill/activation medium 쪽이 다르다.

### 핵심 단위

- 아이템/슬롯: 무기, 방어구, 장신구, 레어/레전더리 기반.
- 제작: Flame Sand, Elementium, affix 추가/교체/리롤, 목표 조건 자동 반복 계열.
- 스킬: Support Skill, Exclusive Support Skill, Activation Medium.
- 엔드게임: Netherrealm과 시즌별 콘텐츠.

### 목표 게임에 쓸 것

- 자동 발동/트리거 주기/수동 사용 페널티를 다루는 Activation Medium 계열.
- 제작 UI에서 목표 affix/tier를 지정하고 반복하는 UX.

### 주의점

- 시즌마다 제작 구조가 크게 바뀐다.
- 공식 문서보다 커뮤니티 DB 의존도가 높다.

우선순위: Medium.

## Last Epoch

### 조사 이유

POE보다 읽기 쉬운 deterministic-ish crafting. `Forging Potential`은 제작 실패 모델로 매우 좋다.

### 핵심 단위

- 아이템: common, magic, rare, exalted, unique, set, legendary.
- Affix: prefix/suffix, affix shard, sealed affix, experimental affix.
- 제작: Forge, Forging Potential, Shard, Glyph, Rune.
- Legendary: Unique의 Legendary Potential과 Exalted item affix transfer.
- 엔드게임: Monolith, Echo, Timeline, Blessing, Dungeon key.

### 목표 게임에 쓸 것

- 제작할수록 아이템의 수정 가능 수명이 줄어드는 `Forging Potential`.
- 실패가 파괴가 아니라 "더 이상 손댈 수 없음"으로 귀결되는 모델.
- Rune of Shattering/Removal/Discovery/Creation 같은 명확한 제작 동사.
- 드랍 전용 고티어 affix와 제작 가능 저티어 affix 분리.

우선순위: Deep Dive.

## Grim Dawn

### 조사 이유

제작 자체보다 component, augment, item skill, auto-cast trigger, Devotion 연결이 자동전투에 유용하다.

### 핵심 단위

- 아이템: magic, rare, epic, legendary, monster infrequent, component, augment, relic, blueprint.
- 제작: Blacksmith, blueprint, 재료, relic craft.
- 장착 강화: Component 1개, augment, faction reward.
- 빌드: Dual mastery, Devotion constellation, item-granted skill.
- 엔드게임: Shattered Realm, mutator, waystone.

### 목표 게임에 쓸 것

- 장비에 붙는 component가 active/passive/trigger skill을 주는 구조.
- Devotion 같은 장비 밖 별자리 트리.
- 특정 스킬에 Celestial Power를 연결해 자동 발동시키는 구조.

우선순위: Medium.

## Chronicon

### 조사 이유

2D 픽셀 ARPG에 가까운 스케일과 UI 참고. 깊은 장비 시스템을 픽셀 톤으로 처리하는 기준점.

### 핵심 단위

- 아이템: unique, randomized item, set, rune, gem.
- 제작: enchanting, scramble, augment, lock, gem, rune, transmutation.
- 엔드게임: randomized dungeon, anomaly, endgame crafting.
- 성장: 대량 skill/perk, endless mastery.

### 목표 게임에 쓸 것

- 8-bit/pixel ARPG에서 툴팁과 제작 UI를 어느 정도까지 밀도 있게 가져갈 수 있는지.
- deterministic crafting과 long-tail mastery의 조합.

우선순위: Medium.

## Undecember

### 조사 이유

장비 제작, 스킬 룬, 링크 룬, 조디악, 참, 라크리마, 이전/계승이 목표 게임의 핵심 표면과 많이 겹친다.

### 핵심 단위

- 장비: 무기, 오프핸드, 방어구, 장신구, charms.
- 등급: Normal, Magic, Rare, Unique, Legendary, Ancient, Holy.
- 제작: Essence 기반 등급, 옵션 수, 옵션 종류, 옵션 값, tier, authority 변경.
- 반복 설정: 원하는 옵션/티어 조건까지 자동 반복.
- 스킬: Skill Rune + Link Rune + Runestone, 최대 6방향 link slot, 색상/태그 매칭.
- 패시브: Zodiac.
- 보조 성장: Relic, Charm blessing total, Lacrima.
- 엔드게임: Chaos Dungeon, Chaos Card, Chaos Statue.

### 목표 게임에 쓸 것

- 스킬 룬 보드와 링크 방향/색상.
- 장비 성장값 이전/계승.
- 참/축복 총합으로 효과가 켜지는 구조.
- 자동 반복 인챈트 조건 설정.

우선순위: Deep Dive.

## 소스

- https://torchlight.xd.com/en/ep8/
- https://torchlight.xd.com/ep6
- https://torchlight.xd.com/en/data
- https://tlidb.com/Flame_Sand
- https://www.vhpg.com/torchlight-infinite-crafting/
- https://lastepoch.com/skills/
- https://lastepoch.com/end-game/
- https://lastepoch.fandom.com/wiki/Crafting
- https://lastepoch.fandom.com/wiki/Runes
- https://www.grimdawn.com/guide/items/crafting/
- https://www.grimdawn.com/guide/items/components/
- https://www.grimdawn.com/guide/character/devotion
- https://www.grimdawn.com/guide/character/item-skills/
- https://www.grimdawn.com/guide/game-settings/shattered-realm
- https://store.steampowered.com/app/375480/Chronicon/
- https://chronicon.fandom.com/wiki/Crafting_Materials
- https://chronicon.fandom.com/wiki/Enchanting
- https://chronicon.fandom.com/wiki/Runes
- https://guide.floor.line.games/UD/en_US/detail/1166916752808800098
- https://guide.floor.line.games/UD/en_US/detail/1166917747181300461
- https://guide.floor.line.games/UD/en_US/detail/1166916549917300337
- https://guide.floor.line.games/UD/en_US/detail/1166916574409800978
- https://guide.floor.line.games/UD/en_US/detail/1166916634911400879
