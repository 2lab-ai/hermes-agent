# Research Completion Audit

작성일: 2026-05-25

이 문서는 현재 리서치 산출물이 원래 목표를 충족하는지 요구사항별로 점검한 것이다.
범위는 "아이템/크래프팅 중심 오토류 게임 설계를 위한 조사와 기획 단위 정의"까지이며, 실제 게임 구현은 포함하지 않는다.

## 원래 목표 요약

만들려는 게임:

- Steam Windows/Mac에서 돌아가는 8비트풍 자동전투/뱀서류 게임.
- 전투는 자동 시뮬레이션 tick 중심.
- 아이템, 장착, 특성 트리, 스킬, 아이템 강화, 맵 키는 하드코어 ARPG 수준으로 깊게 설계.
- POE형 아이템은 POE식 크래프팅, MapleStory형 아이템은 MapleStory식 강화, Diablo II형 아이템은 Diablo II식 소켓/룬워드처럼 출신 문법별로 다른 제작 UI와 실패 모델을 가짐.

## 요구사항별 증거

| 요구사항 | 증거 파일 | 상태 |
|---|---|---|
| POE1/2와 다른 아이템/크래프팅 게임 후보 리스트업 | `00-target-games-and-research-units.md` | 충족 |
| 게임별 조사할 기획 단위 정의 | `00-target-games-and-research-units.md`의 `공통 조사 단위`와 각 게임별 bullet | 충족 |
| POE1 item/items/equips/crafting 조사 | `00-target-games-and-research-units.md`, `01-poe1-poe2.md`, `11-mechanics-comparison-matrix.md` | 충족 |
| POE1 skill/passive tree/map 조사 | `01-poe1-poe2.md`, `14-skill-support-taxonomy.md`, `15-map-key-modifiers.md` | 충족 |
| POE2 item/crafting/skill/tree/waystone 조사 | `00-target-games-and-research-units.md`, `01-poe1-poe2.md`, `14-skill-support-taxonomy.md`, `15-map-key-modifiers.md` | 충족 |
| Torchlight: Infinite 조사 | `00-target-games-and-research-units.md`, `04-other-arpgs.md`, `11-mechanics-comparison-matrix.md` | 충족 |
| Diablo II item/equip/socket/runeword/cube 조사 | `00-target-games-and-research-units.md`, `02-diablo2.md`, `11-mechanics-comparison-matrix.md`, `13-craft-actions-spec.md` | 충족 |
| Lineage 1 enchant/economy/risk 조사 | `00-target-games-and-research-units.md`, `03-maplestory-lineage1.md`, `11-mechanics-comparison-matrix.md`, `13-craft-actions-spec.md` | 충족 |
| MapleStory starforce/flame/potential/trace 조사 | `00-target-games-and-research-units.md`, `03-maplestory-lineage1.md`, `11-mechanics-comparison-matrix.md`, `13-craft-actions-spec.md` | 충족 |
| Last Epoch/Undecember 등 hardcore crafting 후보 심화 | `04-other-arpgs.md`, `06-last-epoch-undecember-deep-dive.md`, `11-mechanics-comparison-matrix.md` | 충족 |
| 기타 POE와 다른 빌드/아이템 문법 조사 | `05-non-poe-candidates.md`, `07-non-poe-build-systems-deep-dive.md`, `11-mechanics-comparison-matrix.md` | 충족 |
| 공간 인벤토리/아이템 배치 문법 조사 | `08-spatial-program-and-modular-systems.md`, `11-mechanics-comparison-matrix.md` | 충족 |
| 좌->우 주문 프로그램/완드 문법 조사 | `08-spatial-program-and-modular-systems.md`, `12-prototype-data-schema.md` | 충족 |
| capacity/polarity/부정 옵션 보상/무기 정체성 성장 조사 | `08-spatial-program-and-modular-systems.md`, `10-target-game-system-draft.md` | 충족 |
| recipe unlock/salvage bits/trait 부착 문법 조사 | `08-spatial-program-and-modular-systems.md`, `12-prototype-data-schema.md` | 충족 |
| 목표 게임에 넣을 prototype module 우선순위 | `10-target-game-system-draft.md`, `11-mechanics-comparison-matrix.md` | 충족 |
| Prototype 데이터 스키마 | `12-prototype-data-schema.md` | 충족 |
| Family별 craft action/input/output/failure enum | `13-craft-actions-spec.md` | 충족 |
| Skill support taxonomy | `14-skill-support-taxonomy.md` | 충족 |
| MapKey danger/reward/family-bias modifier | `15-map-key-modifiers.md` | 충족 |
| Source-backed research anchors | 각 리서치 문서의 `소스` 또는 `소스 앵커` 섹션 | 충족 |

## 산출물 목록

- `00-target-games-and-research-units.md`: 대상 게임 목록, 게임별 조사 단위, 우선순위, 소스 앵커.
- `01-poe1-poe2.md`: POE1/2 아이템, 제작, 스킬, 패시브, 맵/웨이스톤 조사.
- `02-diablo2.md`: D2/D2R 아이템, 소켓, 룬워드, 큐브, crafted family 조사.
- `03-maplestory-lineage1.md`: MapleStory/Lineage 1 다층 강화, 파괴, trace, safe enchant 조사.
- `04-other-arpgs.md`: Torchlight: Infinite, Last Epoch, Grim Dawn, Chronicon, Undecember 1차 조사.
- `05-non-poe-candidates.md`: Siralim, Warframe, Monster Hunter, Noita, Terraria, Backpack, BDO, Lost Ark 등 후보 정리.
- `06-last-epoch-undecember-deep-dive.md`: Last Epoch/Undecember 데이터 모델, 제작 행동, 실패 모델, UI 요구 심화.
- `07-non-poe-build-systems-deep-dive.md`: Siralim, Warframe, Monster Hunter, Noita, Terraria, Backpack 계열 심화.
- `08-spatial-program-and-modular-systems.md`: Backpack/Noita/Magicraft/Warframe/Slormancer/Siralim/Qud의 공간, 주문 프로그램, 모듈 예산, 레시피/trait 문법 심화.
- `10-target-game-system-draft.md`: 목표 게임 통합 시스템 초안.
- `11-mechanics-comparison-matrix.md`: 게임별 data model, craft action, failure cost, build depth, target module 비교.
- `12-prototype-data-schema.md`: Prototype JSON-like schema.
- `13-craft-actions-spec.md`: Family별 제작 동사, 입력, 출력, 실패 결과.
- `14-skill-support-taxonomy.md`: 자동전투 active skill/support category.
- `15-map-key-modifiers.md`: MapKey modifier, biome, corruption, failure reward.
- `99-research-completion-audit.md`: 요구사항별 완료 증거.

## 남은 것은 리서치가 아니라 구현/제품 결정

아래는 리서치 목표 밖의 후속 작업이다.

- 실제 게임 엔진 선택.
- Windows/Mac 빌드 파이프라인.
- 저장 파일 포맷 구현.
- 전투 시뮬레이터 구현.
- 제작 UI 와이어프레임.
- 수치 밸런싱.
- 플레이테스트.

## 완료 판단

현재 산출물은 원래 요청한 "조사 대상 게임 리스트업", "게임별 조사 단위", "병렬 조사 결과", "목표 게임 설계를 위해 필요한 item/crafting/skill/tree/map-key 메커닉 조사"를 문서 기준으로 충족한다.
다음 작업은 리서치 계속이 아니라, 이 리서치를 바탕으로 실제 프로토타입 spec 또는 implementation plan을 작성하는 단계다.
