# Spatial, Program, and Modular Item Systems Deep Dive

작성일: 2026-05-25

이 문서는 POE형 affix 제작과 다른 "아이템 문법"을 목표 게임에 옮기기 위한
4차 딥다이브 결과다. 대상은 Backpack Battles/Hero/God of Weapons,
Noita/Magicraft, Warframe/The Slormancer, Siralim Ultimate/Caves of Qud다.

핵심 결론은 네 가지다.

- `SpatialGrid`: 아이템의 모양, 위치, 인접성이 전투 성능과 레시피를 결정한다.
- `SpellProgram`: 아이템이 좌에서 우로 실행되는 주문/투사체 프로그램을 가진다.
- `ModuleBudget`: 장비가 capacity, polarity, drain, negative option budget을 가진다.
- `RecipeTraitLab`: 레시피를 발견하고, 장비를 분해해 bits를 얻고, 제한 슬롯에 trait를 붙인다.

## 1. SpatialGrid

참조: Backpack Battles, Backpack Hero, God of Weapons.

핵심 규칙:

- 제한된 격자에 아이템을 배치하고, 배치 결과가 전투 성능을 바꾼다.
- 아이템은 `shapeCells`와 회전을 가진다. 공간을 차지하는 것 자체가 비용이다.
- 인접, 대각, 행, 열, 같은 태그, 소켓 방향 같은 위치 조건으로 효과나 레시피가 켜진다.
- 일부 레시피는 재료를 인접 배치한 뒤 다음 상점/웨이브 단계에서 합성된다.
- 전투 중에는 배치를 계속 재계산하지 않고, 웨이브 시작 시 snapshot으로 고정하는 편이 예측 가능하다.

필요 데이터:

```ts
ItemShape {
  cells: [x: number, y: number][],
  allowedRotations: number[]
}

GridItemDef {
  id: string,
  tags: string[],
  rarity: string,
  shape: ItemShape,
  effects: EffectDef[],
  socketRules?: SocketRule[],
  recipeRefs?: string[]
}

GridItemInstance {
  defId: string,
  x: number,
  y: number,
  rotation: number,
  locked: boolean,
  location: "grid" | "storage" | "shop"
}

AdjacencyRule {
  mode: "orthogonal" | "diagonal" | "row" | "column" | "network" | "socket_edge",
  requiredTags?: string[],
  requiredItemIds?: string[],
  minCount?: number
}

GridRecipe {
  id: string,
  ingredients: string[],
  requiresAdjacency: boolean,
  catalystIds: string[],
  resultId: string,
  discoveryState: "hidden" | "hinted" | "known"
}
```

목표 게임 적용:

- Prototype 전체 인벤토리에 적용하지 말고 `CharmGridBoard` 또는 `RelicGridBoard`로 제한한다.
- 초기 크기는 `6x5`, 아이템 45개, 레시피 20개, 상태효과 8개, 웨이브 10개가 적절하다.
- POE/D2/Maple 장비와 충돌하지 않도록, 격자 보드는 보조 빌드 표면으로 둔다.
- `star/diamond` 같은 원작 고유 명칭과 레시피 테마는 쓰지 않는다. `socket edge`, `rune edge`, `link marker`로 새 시각 언어를 만든다.

출처 앵커:

- Backpack Battles: https://store.steampowered.com/app/2427700/Backpack_Battles/
- Backpack Battles Recipe: https://backpackbattles.wiki.gg/wiki/Recipe
- Backpack Battles Game Mechanics: https://backpackbattles.wiki.gg/wiki/Game_Mechanics
- Backpack Hero: https://store.steampowered.com/app/1970580/Backpack_Hero/
- God of Weapons: https://store.steampowered.com/app/2342950/God_Of_Weapons/

## 2. SpellProgram

참조: Noita, Magicraft.

핵심 규칙:

- 완드/무기 내부에 주문 슬롯이 있고, 기본 실행 순서는 좌->우다.
- 주문은 `projectile`, `modifier`, `multicast`, `trigger`, `timer`, `passive`로 나뉜다.
- modifier는 현재 cast state를 바꾸고, multicast는 뒤의 N개 주문을 묶어 실행한다.
- 자원은 `manaMax`, `manaRegen`, `castDelay`, `recharge`, `cooldown`으로 분리한다.
- hidden wrap, 무제한 shuffle, payload 내부 예외는 예측성이 낮으므로 고급/희귀 아이템으로 격리한다.

필요 데이터:

```ts
ProgrammableItem {
  id: string,
  slots: SpellInstance[],
  fixedPrefixSlots: SpellInstance[],
  shuffle: boolean,
  seededShufflePerCycle: boolean,
  spellsPerCast: number,
  castDelayFrames: number,
  rechargeFrames: number,
  manaMax: number,
  manaRegenPerFrame: number,
  spreadDeg: number,
  rngSeed: number
}

SpellDef {
  id: string,
  kind: "projectile" | "modifier" | "multicast" | "trigger" | "timer" | "passive",
  manaCost: number,
  castDelayDelta: number,
  rechargeDelta: number,
  drawCount: number,
  projectilePattern?: "single" | "spread" | "ring" | "beam" | "orbit" | "chain" | "trap" | "summon",
  modifierOps?: ModifierOp[],
  payloadRule?: "next" | "right_spell" | "on_hit" | "while_flying",
  charges?: number,
  scopeRule?: "next_spell" | "next_n" | "until_projectile" | "payload_only"
}

CompiledSpellBytecode {
  tickRate: number,
  opcodes: string[],
  deterministicRngStreams: string[]
}
```

목표 게임 적용:

- 플레이어 UI는 `좌->우 실행 블록`으로 보이고, 내부는 fixed tick bytecode로 컴파일한다.
- `scope bracket`을 반드시 표시한다. 어떤 modifier가 어떤 projectile/payload에 걸리는지 선으로 보여줘야 한다.
- `wrap`은 Prototype에서 금지하거나 1회만 허용한다.
- `always cast`는 숨기지 않고 별도 고정 슬롯으로 표시한다.
- 자동 전투 리플레이를 위해 슬롯 index, tick, RNG stream을 모두 seed 기반으로 고정한다.

출처 앵커:

- Noita Wands: https://noita.wiki.gg/wiki/Wands
- Noita Spells: https://noita.wiki.gg/wiki/Spells
- Noita Wand Mechanics: https://noita.wiki.gg/wiki/Guide:Wand_Mechanics
- Noita Expert Draw: https://noita.wiki.gg/wiki/Expert_Guide:Draw
- Magicraft: https://store.steampowered.com/app/2103140/_Magicraft/
- Magicraft Wands: https://magicraft.fandom.com/wiki/Wands
- Magicraft Spells: https://magicraft.fandom.com/wiki/Spells

## 3. ModuleBudget

참조: Warframe, The Slormancer.

핵심 규칙:

- 장비는 mod slot과 capacity를 가진다.
- 모듈은 `drain`을 먹고, rank가 오르면 효과와 drain이 함께 오른다.
- 슬롯 polarity와 모듈 polarity가 맞으면 비용을 줄이고, 틀리면 비용을 늘린다.
- negative affix가 있으면 positive budget을 키워준다.
- 약한/덜 쓰이는 베이스에는 수동 `dispositionScalar`를 줘서 고점을 보정할 수 있다.
- 무기 자체는 XP, kill count, milestone으로 정체성과 슬롯을 성장시킬 수 있다.

필요 데이터:

```ts
ModuleItem {
  id: string,
  rank: number,
  maxRank: number,
  drainByRank: number[],
  polarity: string,
  tags: string[],
  effects: EffectDef[]
}

ModuleSlot {
  index: number,
  polarity?: string,
  acceptsTags: string[],
  installedModuleId?: string
}

ModuleBudgetBoard {
  carrierItemId: string,
  carrierLevel: number,
  baseCapacity: number,
  capacityMultiplier: number,
  slots: ModuleSlot[],
  remainingCapacity: number
}

RiskRewardAffix {
  positiveBudget: number,
  negativeTag?: string,
  compensationScalar: number,
  blockedBuildTags: string[]
}

IdentityWeaponXP {
  weaponLevel: number,
  killCount: number,
  identityMilestones: string[],
  evolutionForm?: string,
  primordialToggle?: boolean
}
```

목표 게임 적용:

- `ModCapacityBoard`는 Prototype이 아니라 V1 후보로 둔다.
- `negative_as_build_hook`을 사용한다. 예: 치명타 불가 대신 감전 자동발동, 회복 불가 대신 처치 보호막.
- disposition은 라이브 통계 자동 조정이 아니라 내부 티어표/시즌 수동값으로 둔다.
- 긴 재레벨링, 무한 reroll, 거래 시장 중심 Riven 경제는 가져오지 않는다.
- 무기는 20~30개의 강한 정체성 무기로 시작하고, 수집량 자체를 콘텐츠로 삼지 않는다.

출처 앵커:

- Warframe Mods Guide: https://www.warframe.com/en/news/mods-guide
- Warframe Riven Mods: https://wiki.warframe.com/w/Riven_Mods
- Warframe Polarity: https://wiki.warframe.com/w/Polarity
- The Slormancer: https://store.steampowered.com/app/1104280/The_Slormancer/
- Slorm Reapers: https://slormancer.fandom.com/wiki/Slorm_Reapers
- Slormancer Crafting: https://slormancer.fandom.com/wiki/Crafting

## 4. RecipeTraitLab

참조: Siralim Ultimate, Caves of Qud.

핵심 규칙:

- 레시피는 data disk/inscription/blueprint 형태로 드랍되고, 사용하면 영구 제작법이 열린다.
- 장비나 artifact를 분해하면 bits/salvage resource가 나온다.
- item mod는 제한된 슬롯 수만 허용한다. Qud식 기준은 3칸이 좋은 시작점이다.
- trait는 생물 고유 효과가 아니라 장비, 소환수, 자동스킬에 부착 가능한 `trait_id` atom으로 취급한다.
- 자동 발동은 `on_attack`, `on_hit`, `on_kill`, `on_dodge`, `on_low_hp`, `start_wave` 정도로 압축한다.

필요 데이터:

```ts
RecipeUnlock {
  recipeId: string,
  targetType: "item" | "mod" | "spell" | "summon" | "trait",
  source: string,
  consumedOnUse: boolean,
  learnedPermanent: boolean,
  requiredTier: number
}

SalvageResource {
  resourceId: string,
  sourceItemId: string,
  disassembleRule: string,
  guaranteedYield: string[],
  randomYield: string[]
}

SlotBudget {
  carrierType: "item" | "summon" | "skill" | "artifact",
  slotType: "mod" | "trait" | "spell" | "trigger",
  cap: number,
  unlockRule: string,
  compatibleTags: string[]
}

AttachableTrait {
  traitId: string,
  source: string,
  carrier: "item" | "summon" | "skill" | "artifact",
  triggerEvent: string,
  condition: string,
  effect: EffectDef,
  stackRule: string
}
```

목표 게임 적용:

- `RecipeUnlock`은 낮은 티어 드랍을 계속 의미 있게 만든다.
- `SalvageResource`는 하드코어 제작의 중심 경제로 쓴다: 장비 분해 -> bits -> mod 장착.
- `AttachableTrait`는 소환수/장비/자동스킬을 하나의 빌드 언어로 묶는다.
- Siralim식 6v6 파티, 1200+ creature, 40 specialization은 제외한다.
- Caves of Qud의 artifact 식별 실패/파손, per-run bit remapping, 전 오브젝트 시뮬레이션은 제외한다.

출처 앵커:

- Siralim Creatures: https://siralimultimate.wiki.gg/wiki/Creatures
- Siralim Artifacts: https://siralimultimate.wiki.gg/wiki/Artifacts
- Siralim Spell Gems: https://siralimultimate.wiki.gg/wiki/Spell_Gems
- Siralim Trait Materials: https://siralimultimate.wiki.gg/wiki/Category:Trait_Materials
- Caves of Qud Data Disk: https://wiki.cavesofqud.com/wiki/Data_disk
- Caves of Qud Bits: https://wiki.cavesofqud.com/wiki/Bits
- Caves of Qud Item Mods: https://wiki.cavesofqud.com/wiki/Item_mods
- Caves of Qud Scrap: https://wiki.cavesofqud.com/wiki/Scrap

## Prototype / V1 배치

Prototype:

- `CharmGridBoard`: SpatialGrid의 제한판. `6x5`, 아이템 45개, 레시피 20개.
- `SpellProgram`: 실제 완드 프로그램은 미루고, `SkillSupportBoard`의 고급 support로 일부만 반영.
- `RecipeUnlock`: 제작법 드랍과 연구 도감.
- `SalvageResource`: 장비 분해 -> bits/shards/runes.

V1:

- `ProgrammableSkillItem`: Noita/Magicraft식 좌->우 실행 완드.
- `ModCapacityBoard`: Warframe식 capacity/polarity.
- `IdentityWeaponXP`: Slormancer식 무기 정체성 성장.
- `AttachableTrait`: Siralim/Qud식 trait 부착.

Later:

- full companion party circuit.
- full spell queue wrapping/shuffle.
- live disposition economy.
- large-scale recipe industry.
