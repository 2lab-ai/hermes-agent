# Diablo II / Diablo II: Resurrected 아이템·룬워드·큐브 리서치

작성일: 2026-05-25

## 출처 기준

- 공식/1차: Blizzard Arreat Summit, Blizzard D2R news.
- 커뮤니티/2차: Wowhead D2R guides, Diablo Wiki item generation.

## 핵심 구조

Diablo II는 POE와 다르게 "희귀도"보다 "베이스 물성 + 소켓 + 룬워드 + 큐브 레시피"가 강하다.

### 아이템 분류

- 희귀도/품질: normal, magic, rare, set, unique, crafted.
- 베이스 상태: low quality, normal, superior, ethereal, socketed.
- 베이스 계층: normal -> exceptional -> elite.
- 소켓 재료: rune, gem, jewel.
- 인벤토리 패시브: charm.

### 장비와 인벤토리

- 장비 슬롯: 무기/방패 또는 양손, 머리, 갑옷, 장갑, 벨트, 부츠, 반지 2, 목걸이.
- 용병도 장비를 착용해 빌드 일부가 된다.
- 격자 인벤토리와 아이템 크기가 파밍 선택을 만든다.
- Horadric Cube는 제작 도구이면서 2x2를 차지하고 내부 4x3 저장공간을 주는 가방이다.
- Charm은 들고만 있어도 효과가 있어 "공간을 능력치로 바꾸는" 구조다.

## Affix와 소켓

- Magic은 일반적으로 1~2개 속성, Rare는 2~6개 속성.
- Crafted는 고정 속성 + 랜덤 affix 구조다.
- 드롭 순간 아이템 정체성이 확정되고, 식별은 정보를 공개할 뿐 결과를 다시 굴리지 않는다.
- 소켓 수와 베이스 타입은 룬워드 가치의 핵심이다.
- 룬워드는 정확한 아이템 타입, 정확한 소켓 수, non-magic socketed item, 정확한 룬 순서가 모두 맞아야 한다.

## Horadric Cube 제작

큐브는 단일 제작대가 아니라 범용 변환 시스템이다.

- 룬/보석 업그레이드.
- 장비 소켓 추가.
- socketed item에서 재료 제거. 이때 소켓 안 재료는 파괴된다.
- Magic/Rare item reroll.
- Normal/Exceptional/Elite base upgrade.
- Crafted item family 제작.
- Secret Cow Level 등 특수 지역 개방.

## Crafted Item Family

Blood, Caster, Hit Power, Safety 같은 제작군은 목표 게임에 특히 적합하다.

- 입력: 특정 base item + rune + gem + jewel.
- 출력: 계열별 고정 옵션 + 랜덤 affix.
- 장점: 플레이어가 목표 계열을 고르지만 결과는 완전히 고정되지 않는다.
- 목표 게임 변환: 흡혈형, 시전형, 방어형, 소환형, 탄막형 같은 자동전투 제작군으로 바꾸기 좋다.

## 룬워드의 교훈

- 룬워드는 "드랍 고유 아이템"이 아니라 플레이어가 베이스와 재료를 모아 목적형 전설 아이템을 만드는 구조다.
- 같은 룬워드라도 elite/superior/ethereal/base speed/socket 수가 가치 차이를 만든다.
- 자동전투에서는 룬워드가 단순 스탯보다 행동 규칙을 바꾸는 편이 좋다.
- 위험: 룬워드가 너무 강하면 rare/unique/set이 죽는다.

## 스킬과 아이템

- 클래스마다 3개 스킬 탭이 있고 선행 조건과 synergy가 있다.
- 아이템은 `+skill`, `+skill tab`, `+all skills`, aura when equipped, charges, proc, -enemy resistance 등으로 빌드를 재정의한다.
- 자동전투 변환: 아이템 속성이 AI 행동 우선순위, 소환, 탄막, 오라, chain, explosion trigger를 바꿔야 한다.

## 엔드게임 루프

- 보스런, 고레벨 지역런, 카우런, 룬 파밍, 매직파인드 세팅.
- Secret Cow Level은 큐브 레시피로 여는 고밀도 파밍 공간이다.
- Terror Zones는 특정 지역을 시간 단위로 고레벨화해 반복 루프를 분산한다.
- Uber/Pandemonium 계열은 보스 키와 고유 보상 구조로 볼 수 있다.

## 목표 게임으로 추출할 원시 타입

- `BaseItem`: 슬롯, 크기, 요구 레벨, 기본 피해/방어, 최대 소켓, 태그.
- `QualityLayer`: Normal, Magic, Rare, Set, Unique, Crafted, Runeword.
- `MaterialSocket`: rune/gem/jewel 삽입과 조합 조건 검사.
- `Recipe`: 입력 아이템 + 재료 + 출력 규칙.
- `CraftFamily`: 고정 속성 묶음 + 랜덤 affix pool.
- `CharmLoadout`: 격자 인벤토리 대신 제한된 charm board.
- `MapKey`: 큐브 레시피나 드랍으로 여는 고밀도 자동전투 맵.

## 복사할 것

- 베이스 + 소켓 + 룬워드.
- Crafted family.
- 저레벨 고유/레어를 상위 base로 올리는 upgrade recipe.
- Charm board.
- 큐브 레시피로 여는 특수 파밍맵.

## 단순화할 것

- 룬은 33종 대신 8~12종부터.
- 보석 등급도 3단계면 충분하다.
- Affix level/treasure class/quality level은 내부 공식으로 숨기고, UI에는 드롭 레벨/가능 속성/최대 소켓만 보여준다.
- 격자 인벤토리는 charm/relic board에만 제한적으로 사용한다.

## 피할 것

- 외부 위키 없이는 알 수 없는 레시피.
- 과도한 인벤토리 테트리스.
- 필수 룬워드 독점.
- 면역 때문에 빌드가 특정 콘텐츠를 아예 못 도는 구조.

## 소스

- https://classic.battle.net/diablo2exp/items/
- https://classic.battle.net/DIABLO2EXP/ITEMS/basics.shtml
- https://classic.battle.net/diablo2exp/items/cube.shtml
- https://classic.battle.net/diablo2exp/items/runewords.shtml
- https://classic.battle.net/diablo2exp/skills/basics.shtml
- https://news.blizzard.com/en-us/diablo2/23816418/diablo-ii-resurrected-ptr-2-5-terror-zones-now-live
- https://www.wowhead.com/diablo-2/guide/horadric-cube-recipes
- https://www.wowhead.com/diablo-2/guide/runewords-types-bonuses-sockets
- https://diablo2.diablowiki.net/V1.09_Item_Generation
