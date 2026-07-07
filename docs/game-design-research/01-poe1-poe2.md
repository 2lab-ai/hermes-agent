# POE1/POE2 아이템·스킬·트리·맵 리서치

작성일: 2026-05-25

## 출처 기준

- 공식: Path of Exile game overview, item data, passive tree, atlas tree, POE2 공식 소개/업데이트.
- 커뮤니티 위키: PoE Wiki, PoE2 Wiki. POE2는 Early Access라 세부 수치와 시스템명이 바뀔 수 있다.

## POE1 핵심 구조

### 아이템과 장비

- 아이템 분류: 장비, 화폐, 카드, 퀘스트 아이템, 젬.
- 장비 분류: 무기, 보조무기, 갑옷, 투구, 장갑, 신발, 방패, 장신구, 플라스크.
- 특수 장착: 주얼은 패시브 트리 슬롯에 장착되고, 플라스크도 persistent item처럼 mod를 가진다.
- 희귀도: normal, magic, rare, unique가 기본. magic은 prefix/suffix 각 1개, rare는 최대 prefix 3 + suffix 3.
- 가치 구조: `base item`, `implicit`, `explicit`, `item level`, `influence/special state`, `corruption`이 결합된다.

### 제작 동사

POE1의 핵심은 화폐가 돈이 아니라 제작 동사라는 점이다.

- 희귀도 상승: Transmutation, Alchemy, Regal, Chance, Binding.
- 전체 재굴림: Alteration, Chaos, Essence, Fossil, Harvest.
- 접사 추가/삭제: Augmentation, Exalted, Annul, Scouring.
- 수치 재굴림: Divine, Blessed, quality currency.
- 태그 제어: Essence는 보장 affix, Fossil은 태그 가중치, Harvest는 태그 보장 재굴림.
- 고급 제어: Crafting Bench, meta-craft, prefix/suffix lock, cannot roll attack/caster 계열.
- 특수 상태: Fractured는 접사를 잠그고, Eldritch는 implicit 경쟁축을 만들며, Corruption은 되돌릴 수 없는 고위험 변형이다.

### 스킬과 특성

- 스킬은 젬 아이템이며 장비 소켓에 꽂는다.
- Support Gem은 링크된 Skill Gem에만 적용된다.
- 하나의 핵심 스킬이 4~6링크를 구성하고, 장비 소켓 색/링크가 빌드 제약이 된다.
- 모든 클래스가 거대한 패시브 트리를 공유한다.
- 시작 위치, Keystone, Notable, Mastery, Jewel, Ascendancy가 빌드 정체성을 만든다.

### 엔드게임

- Map은 소모형 아이템이며 modifier로 난이도와 보상이 바뀐다.
- Atlas는 맵 진행, 보스, 보상 전문화, league mechanic 선택을 묶는 장기 성장판이다.
- 맵/조각/보스 키가 아이템으로 떨어지기 때문에 전투, 드랍, 제작, 엔드게임 진입이 한 경제 안에 묶인다.

## POE2 핵심 구조

### POE1과 다른 점

- 아이템 예시: equipment, currency, flasks, jewels, skill gems, waystones, relics, socketables.
- 장비 소켓은 주로 rune/soul core 같은 장비 enchant에 쓰인다.
- Skill Gem 자체가 support socket을 가진다. 즉 장비 링크 퍼즐보다 스킬 카드 빌드에 가깝다.
- Waystone이 POE1의 map item 역할을 하며 atlas node에 사용된다.
- POE2 현재 제작은 POE1보다 단순하다: transmutation, alchemy, regal, exalted, annul, chaos, essence, omen, rune 중심.

### 자동전투에 더 적합한 부분

- 장비에 skill link를 만드는 POE1 방식보다 POE2식 "스킬 자체 support socket"이 읽기 쉽다.
- 자동전투 게임에서는 스킬 카드마다 targeting, cooldown, projectile, area, trigger support를 꽂는 방식이 UI와 시뮬레이션에 잘 맞는다.
- Spirit reservation은 permanent minion, persistent buff, trigger meta skill을 제한하는 자원으로 번역 가능하다.

## 목표 게임으로 추출할 원시 타입

- `BaseItem`: 슬롯, 요구 레벨, 요구 능력치, 기본 피해/방어, implicit.
- `Affix`: prefix/suffix, tier, tag, numeric range, weight.
- `Rarity`: normal, magic, rare, unique, crafted, corrupted.
- `CraftAction`: rarity upgrade, add affix, remove affix, reroll all, reroll tagged, lock affix, reroll values, corrupt.
- `CurrencyAsVerb`: 화폐가 "돈"이 아니라 구체 행동을 수행한다.
- `SkillGem`: 자동전투 행동의 기본 단위.
- `Support`: targeting, area, cooldown, trigger, projectile count, ailment, reservation을 변형한다.
- `PassiveNode`: 수치 노드, notable, keystone, mastery.
- `MapKey`: 지역 레벨, 적 태그, 위험 modifier, 보상 태그를 가진 소모품.

## 복사할 것

- POE1의 `base + implicit + explicit prefix/suffix + item level/tier` 모델.
- 화폐를 제작 동사로 쓰는 구조.
- 맵/키도 아이템화해서 드랍과 크래프팅 루프에 포함하는 구조.
- 주얼/패시브/마스터리처럼 장비 밖 빌드 표면을 두는 것.
- POE2식 skill gem 자체 support socket.

## 단순화할 것

- 프로토타입 제작 계층은 `Orb`, `Essence`, `Bench`, `Corruption`, `Map craft`부터.
- Rare는 초반 최대 4 affix, 엔드게임에서 6 affix 해금.
- 접사 풀은 부위별 8~15개 태그로 제한.
- 패시브 트리는 거대 그래프가 아니라 클래스 시작점, 3개 경로, 주얼 슬롯, 마스터리 정도로 시작.

## 피할 것

- 모든 POE 리그 제작을 한 번에 넣는 것.
- 제작 결과를 외부 위키 없이는 예측할 수 없는 구조.
- Chaos spam 같은 완전 무작위 반복만 남기는 구조.
- 매직파인드가 전투력 장비보다 최적이 되는 구조.
- 자동전투에서 실패한 맵 키가 완전 손실만 남는 구조.

## 소스

- https://www.pathofexile.com/game
- https://www.pathofexile.com/item-data
- https://www.pathofexile.com/fullscreen-passive-skill-tree
- https://www.pathofexile.com/fullscreen-atlas-skill-tree
- https://www.poewiki.net/wiki/Item
- https://www.poewiki.net/wiki/Crafting
- https://www.poewiki.net/wiki/Crafting_Bench
- https://www.poewiki.net/wiki/Item_socket
- https://www.poewiki.net/wiki/Atlas_of_Worlds
- https://www.poe2wiki.net/wiki/Item
- https://www.poe2wiki.net/wiki/Crafting
- https://www.poe2wiki.net/wiki/Support_gem
- https://www.poe2wiki.net/wiki/Spirit
- https://www.poe2wiki.net/wiki/Waystone
