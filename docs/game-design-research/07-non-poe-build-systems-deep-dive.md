# Non-POE Build Systems Deep Dive

작성일: 2026-05-25

## 출처 기준

- 공식: Steam, 제작사/지원 문서.
- 커뮤니티: wiki.gg, Warframe Wiki, Fextralife 등.
- 큰 구조는 공식 설명으로 잡고, 세부 슬롯/재료/규칙은 커뮤니티 위키로 보강했다.

## Siralim Ultimate

### 데이터 모델

- 크리처 6체 파티.
- 각 크리처는 innate/fusion/artifact trait을 가진다.
- 각 크리처는 spell gem을 장착할 수 있다.
- Artifact는 크리처당 1개 장착하고 stat, trait, spell, nether slot을 가진다.
- Spell gem은 charge 기반이고 성으로 복귀해야 충전된다.
- Relic, card, account-wide 보너스가 장기 진행을 만든다.

### POE와 다른 핵심

장비 affix보다 "전투 규칙을 바꾸는 trait 조합"이 본체다.
개별 아이템 수치가 아니라 파티 전체의 조건문 네트워크가 빌드를 만든다.

### 실패/비용/진행

- 반복 realm 진행.
- 재료 소모 강화.
- spell charge 소모.
- 희귀 trait material / nether stone 파밍.
- 실패는 장비 파괴보다 시간, 재료, 층 진행 손실이다.

### 자동전투 번역

`TraitGraph` 모듈로 채택한다.

- 유닛 3~4체.
- 각 유닛은 고유 trait 1개, 장비 trait 1개, support trigger 1개.
- 전투 로그는 "시작 시 / 공격 시 / 피격 시 / 처치 시 / 사망 시" 트리거를 보여준다.

### 복사/단순화/회피

- 복사: trait 시너지, artifact socket, 자동 spell trigger.
- 단순화: 1200+ 크리처가 아니라 직업 8개, trait 80개, 유닛 3~4체.
- 회피: 빌드 조합 수가 UI와 디버깅을 압도하는 것.

## Warframe

### 데이터 모델

- 장비 본체.
- mod slot.
- mod capacity.
- polarity.
- mod rank.
- fusion cost.
- forma/polarization.
- blueprint/foundry/resource.

### POE와 다른 핵심

드랍 아이템 affix보다 "같은 장비에 어떤 카드를 얼마만큼 수용할지"가 빌드다.
Forma와 polarity는 장비를 특정 빌드로 영구 투자하게 만든다.

### 실패/비용/진행

- 실패는 파괴보다 투자 잠금과 재화/시간 소모다.
- Endo, credit, forma, slot, blueprint/resource가 비용이다.
- 반복 전투는 mod, resource, blueprint, reputation을 동시에 진척시킨다.

### 자동전투 번역

`CapacityModding` 모듈로 채택한다.

- 장비마다 mod slot 6개.
- mod는 cost, polarity, rank, tag를 가진다.
- polarity 일치 시 cost 감소.
- rank를 올릴수록 강해지지만 capacity 부담도 커진다.

### 복사/단순화/회피

- 복사: capacity, polarity, upgrade rank.
- 단순화: 실시간 제작 대기 제거.
- 회피: 과도한 재화 종류와 mobile/F2P식 시간 게이트.

## Monster Hunter World / Rise / Sunbreak

### 데이터 모델

- weapon tree.
- armor 5부위.
- charm/talisman.
- decoration slot.
- skill level threshold.
- set bonus.
- augment/qurious roll.
- monster material.

### POE와 다른 핵심

Affix item hunt가 아니라 "몬스터별 부품 제작 + 부위 조합 + 스킬 레벨 임계값"이다.
스킬은 한 줄 옵션이 아니라 여러 부위 합산으로 발동/강화된다.

### 실패/비용/진행

- 사냥 실패는 시간/소모품 손실.
- 성공은 특정 몬스터 소재.
- 고난도 변형 몬스터는 더 좋은 augment 재료를 준다.
- 반복 사냥은 무기 트리, 장식주, 호석, 방어구 부위, augment 재료 각각을 밀어준다.

### 자동전투 번역

`SkillThresholdGear` 모듈로 채택한다.

- 장비 부위마다 skill point를 가진다.
- 특정 threshold에서 효과가 켜진다.
- 예: 독저항 3레벨이면 독맵 자동전투 페널티 무시.
- 예: 광전사 5레벨이면 체력 30% 이하 틱 가속.

### 복사/단순화/회피

- 복사: 부위별 스킬 합산, 보스 소재 타깃 파밍.
- 단순화: 액션 숙련 의존은 자동 전투 시뮬레이션으로 치환.
- 회피: 장식주 극저확률 RNG를 그대로 복제.

## Noita

### 데이터 모델

- wand chassis.
- ordered spell list.
- modifier.
- multicast.
- trigger/timer.
- projectile.
- mana.
- cast delay.
- recharge time.
- perk.

### POE와 다른 핵심

옵션 합산이 아니라 "작은 명령어를 순서대로 실행하는 주문 프로그램"이다.
같은 spell도 순서와 trigger 위치에 따라 전혀 다른 무기가 된다.

### 실패/비용/진행

- Permadeath.
- 자기가 만든 폭발/산/반사에 죽는 자해 리스크.
- 편집 가능 구역 제한.
- 실패는 학습을 만든다.

### 자동전투 번역

`SpellSequencer` 모듈로 채택한다.

- 스킬 슬롯을 왼쪽부터 실행한다.
- 예: projectile -> multicast -> trigger explosion -> leech.
- 전투 로그에 실행 순서를 표시한다.
- 위험 태그와 시뮬레이션 preview를 제공한다.

### 복사/단순화/회피

- 복사: 주문 순서, trigger, 자해 리스크.
- 단순화: 픽셀 물리 전체 제거.
- 회피: 즉사급 예측 불가능성.

## Terraria

### 데이터 모델

- weapon/armor/accessory.
- prefix modifier.
- crafting tree.
- crafting station.
- boss/biome progression gate.
- world resource.

### POE와 다른 핵심

Endgame map보다 world progression이 재료, 제작법, 보스, NPC를 순차 개방한다.
Accessory fusion tree가 장기 목표다.

### 실패/비용/진행

- 핵심 비용은 gold reforge와 탐험/파밍 시간.
- 보스를 잡으면 월드 상태와 제작 가능 풀이 변한다.
- Reforge는 간단한 modifier reroll sink다.

### 자동전투 번역

`AccessoryFusionChain` 모듈로 채택한다.

- 낮은 티어 부품을 버리지 않고 상위 액세서리로 연결한다.
- 맵/키 엔드게임은 특정 보스 소재로 열린다.
- 특정 accessory branch가 자동전투 행동을 바꾼다.

### 복사/단순화/회피

- 복사: 액세서리 합성 트리, reforge sink.
- 단순화: world sandbox, 채굴, 건축 제거.
- 회피: crafting tree가 너무 길어져 목표가 흐려지는 것.

## Backpack Hero / Backpack Battles

### 데이터 모델

- 격자 가방.
- 회전 가능한 item shape.
- 인접/행/열/내부 bag 조건.
- recipe merge.
- stamina/trigger timer.
- curse/hazard.

### POE와 다른 핵심

아이템 옵션보다 물리적 배치가 곧 빌드다.
전투는 거의 자동이고 실력은 shop/build phase와 공간 최적화에 있다.

### 실패/비용/진행

- Run 실패 또는 라운드 패배.
- 비용은 gold, space, stamina, 조합 타이밍.
- 공간을 차지하는 curse/hazard도 빌드에 따라 이득이 될 수 있다.

### 자동전투 번역

`GridInventory` 모듈로 채택한다.

- 6x8 또는 7x7 고정 격자.
- 아이템은 인접 조건, 방향, 태그, 쿨다운을 가진다.
- 전투는 20~40초 tick sim.
- 미세 배치가 DPS/방어/발동주기를 바꾼다.

### 복사/단순화/회피

- 복사: 공간 기반 시너지, recipe merge, fatigue timer.
- 단순화: 전체 인벤토리 대신 charm/relic board에 제한.
- 회피: 과도한 shop RNG와 미세 배치 피로.

## 통합 설계 제안

가장 이식성 높은 모듈은 6개다.

- `TraitGraph`: Siralim식 유닛/장비 패시브 조건문.
- `CapacityModding`: Warframe식 슬롯 비용/극성.
- `SkillThresholdGear`: Monster Hunter식 부위 합산 스킬 레벨.
- `SpellSequencer`: Noita식 순서 기반 자동스킬.
- `GridInventory`: Backpack류 배치 퍼즐.
- `AccessoryFusionChain`: Terraria식 버릴 것 없는 액세서리 합성.

권장 순서:

1. `GridInventory` + `SkillThresholdGear`를 V1 보조 장비 표면으로 검토한다.
2. `TraitGraph`는 동료/소환수 시스템을 넣을 때까지 미룬다.
3. `CapacityModding`은 중후반 장비 투자층으로 둔다.
4. `SpellSequencer`는 고급 스킬 아이템으로 제한한다.
5. `AccessoryFusionChain`은 낮은 티어 드랍을 계속 의미 있게 만드는 장기 파밍 축으로 쓴다.

## 4차 딥다이브 보강

자세한 구현 단위는 `08-spatial-program-and-modular-systems.md`에 분리했다.
기존 6개 모듈은 아래처럼 더 구체적인 구현 표면으로 갱신한다.

- `GridInventory` -> `CharmGridBoard` / `SpatialGrid`: `shapeCells`, 회전, 인접/대각/행/열 조건, recipe discovery, craft resolve.
- `SpellSequencer` -> `SpellProgram`: 플레이어에게는 좌->우 실행 블록으로 보이고, 내부는 fixed tick bytecode로 컴파일한다.
- `CapacityModding` -> `ModuleBudget`: capacity, drain, polarity, rank, negative affix compensation, underused-base rescue.
- `TraitGraph` -> `RecipeTraitLab`: recipe unlock, salvage bits, 3-slot mod cap, attachable trait, auto trigger.
- `AccessoryFusionChain`은 `RecipeUnlock`과 결합해 낮은 티어 드랍을 연구/청사진 재료로 계속 의미 있게 만든다.

Prototype에는 `CharmGridBoard`, `RecipeUnlock`, `SalvageResource`만 반영한다.
`SpellProgram`, `ModuleBudget`, `AttachableTrait` 전체판은 V1 이후로 미룬다.

## 소스

- https://store.steampowered.com/app/1289810/Siralim_Ultimate/
- https://siralimultimate.wiki.gg/wiki/Artifacts
- https://siralimultimate.wiki.gg/wiki/Spell_Gems
- https://www.warframe.com/news/mods-guide
- https://support.warframe.com/hc/en-us/articles/200500194-Mod-Guide-Use-Fusion-Transmutation-Sale
- https://support.warframe.com/hc/en-us/articles/38385820873741-Foundry-and-Crafting-FAQ
- https://game.capcom.com/manual/MHRISE/en/steam/page/9/1
- https://monsterhunterworld.wiki.fextralife.com/Armor+Sets
- https://monsterhunterworld.wiki.fextralife.com/Decorations
- https://noitagame.com/
- https://noita.wiki.gg/wiki/Wands
- https://noita.wiki.gg/wiki/Spells
- https://terraria.wiki.gg/wiki/Reforged
- https://terraria.wiki.gg/wiki/Modifiers
- https://terraria.wiki.gg/wiki/Accessories
- https://store.steampowered.com/app/1970580/Backpack_Hero/
- https://store.steampowered.com/app/2427700/Backpack_Battles/
- https://backpackbattles.wiki.gg/wiki/Items
- https://backpackbattles.wiki.gg/wiki/Fatigue
- https://backpackhero.wiki.gg/wiki/Cursed_Items
