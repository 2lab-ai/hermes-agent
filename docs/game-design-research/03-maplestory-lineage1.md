# MapleStory / Lineage 1 강화 시스템 리서치

작성일: 2026-05-25

## 출처 기준

- MapleStory: Nexon/MapleStorySEA 공식 문서와 KMS 확률 페이지, MapleStory Wiki 보조.
- Lineage 1: 공식 공개 문서가 빈약해 Inven, Lineage Open Wiki, Lineage Compendium 등 커뮤니티 출처 보조. LineageW 자료는 현대 NC식 변형으로만 취급한다.

## MapleStory

### 아이템과 슬롯

- 큰 축: weapon, secondary weapon, armor, accessory, equipment set.
- 슬롯별 옵션 풀이 중요하다. 무기, 엠블렘, 보조무기, 방패, 모자, 상의, 한벌옷, 하의, 신발, 장갑, 망토, 벨트, 어깨장식, 얼굴장식, 눈장식, 귀고리, 반지, 펜던트, 기계심장 등으로 옵션 가능성이 갈린다.
- 세트 장비는 장착 개수별 보너스를 별도 성장 레이어로 더한다.

### 강화 레이어

- 주문서/Spell Trace: 업그레이드 슬롯을 소비해 능력치를 붙인다. 실패하면 슬롯이 사라질 수 있다.
- Golden Hammer: 업그레이드 슬롯 추가 계열.
- Innocence/Clean Slate: 업그레이드 상태 리셋 또는 실패 슬롯 복구.
- Bonus Stats/Flame: 드랍 순간 또는 flame 사용으로 붙는 추가 스탯.
- Star Force: 업그레이드 슬롯을 모두 사용한 뒤 별을 올리는 meso 기반 강화. 고성 구간부터 실패, 하락, 파괴가 생긴다.
- Potential/Additional Potential: Rare/Epic/Unique/Legendary, 최대 3줄. Cube로 라인과 등급을 재굴림한다.
- Soul Weapon: 별도 무기 강화 레이어.

### 실패와 복구

- 주문서 실패: 슬롯 손실.
- Star Force 실패: 유지, 하락, 파괴가 구간별로 발생.
- 장비 파괴: Equipment Trace로 같은 장비에 일부 상태를 이전한다.
- Potential Scroll 실패: 일부 문서 기준 장비 파괴 가능.
- Cube: 재료/메소/캐시 소모, 등급 상승 보장 횟수 같은 pity가 존재하는 지역/시스템이 있다.

### 목표 게임에 쓸 것

- 드랍 순간의 `flame-like bonus`.
- 슬롯별 옵션 풀.
- 잠재 2~3줄.
- 파괴 시 완전 소실 대신 trace/fragment/transfer.
- 큐브류 재굴림에는 명시 확률과 보장 게이지.

### 피할 것

- 현금 큐브형 무한 재굴림.
- 초반부터 주문서, 별, 잠재, 에디셔널, 플레임, 소울을 모두 넣는 것.
- 옵션 풀이 너무 커져 전투보다 툴팁 해석이 길어지는 것.

## Lineage 1

### 아이템과 슬롯

- 기본 축: weapon, armor, accessory, scroll, material.
- 대표 슬롯: 무기, 투구, 갑옷, 티셔츠, 부츠, 망토, 장갑, 방패/가더, 벨트, 반지 2, 목걸이, 귀걸이.
- 원작형 가치는 복잡한 affix보다 베이스 희소성과 `+N` 인챈트 수치가 중심이다.

### 인챈트

- 일반 무기/갑옷 마법 주문서: 보통 +1.
- 안전 강화선: 무기 +6, 방어구 +4가 전형적 기준으로 알려져 있다. 재질/아이템별 예외가 있다.
- 안전선 이후 실패: 장비와 주문서 소멸이 기본 축.
- 축복 주문서: 성공 시 +1~+3 같은 점프 강화.
- 저주 주문서: -1로 낮춰 재시도 세팅에 쓰인다.
- 속성 인챈트: 일반 인챈트와 별도 레이어. 실패 시 장비 대신 속성 주문서만 소멸하는 방식으로 설명되는 자료가 있다.

### 경제와 리스크

- 강화 실패가 장비 공급 자체를 태우기 때문에 고강 장비 프리미엄이 크다.
- 핵심 sink는 주문서, 아데나, 베이스 장비다.
- 보호/피티는 MapleStory보다 약하고, 안전선과 축복/저주 주문서 운용이 완충 장치다.

### 목표 게임에 쓸 것

- `+N` 단순 표기.
- 안전 강화선.
- 축복 주문서의 점프 강화.
- 저주 주문서의 의도적 -1 조정.
- 고강 장비가 장기 목표가 되는 구조.

### 피할 것

- 보호 없는 완전 소실을 기본 루프로 두는 것.
- 거래 경제 없이는 의미가 약한 장비 소각 압박.
- F2P식 확률 강화 스트레스.

## 통합 설계 추출

- 프로토타입 장비 레이어는 `베이스 드랍 옵션`, `+강화`, `잠재/룬 2~3줄` 3개로 시작한다.
- 강화 실패는 세 종류로 분리한다: 재료 소모, 단계 하락, 엔드게임 선택형 파괴.
- 파괴가 있다면 항상 trace, fragment, pity, insurance 중 하나를 남긴다.
- 축복/저주 주문서는 고위험 제작의 조정 도구로 쓰고, 현금이 아니라 맵/보스/제작 재료로 공급한다.

## 소스

- https://support-maplestory.nexon.com/hc/en-us/articles/204088639-How-do-I-enhance-equips-with-Star-Force
- https://support-maplestory.nexon.com/hc/en-us/articles/204744535-What-are-Spell-Traces
- https://maplestory.nexon.com/Guide/OtherProbability/cube/red
- https://www.maplesea.com/wiki/Equipment/UpgradeTip
- https://www.maplesea.com/info/potential_system/
- https://maplestorywiki.net/w/Equipment
- https://maplestorywiki.net/w/Star_Force_Enhancement
- https://maplestorywiki.net/w/Potential
- https://www.inven.co.kr/webzine/news/?news=91780&site=lineage
- https://lineage-open.fandom.com/wiki/Enchanting
- https://www.lineagecompendium.com/
