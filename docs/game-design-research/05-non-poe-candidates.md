# POE와 다른 하드코어 아이템/크래프팅 후보 리서치

작성일: 2026-05-25

## Deep Dive

### Siralim Ultimate

- 포함 이유: 자동전투, 파티 빌드, 장기 파밍이 목표 장르와 가깝다.
- 연구 단위: creatures, traits, artifacts, spell gems, crafting/enhancement, endgame loop, UI complexity.
- 차용 포인트: 크리처 6마리 각각이 trait + artifact + spell gem을 들고, artifact socket이 자동 발동 조건까지 정의하는 빌드 회로.
- 목표 게임 번역: 플레이어 장비 외에 소환수/동료/유물 보드를 두고 자동전투 조건을 조립한다.

### Warframe

- 포함 이유: 장비 affix보다 mod, capacity, polarity, fusion, forma가 빌드의 본체다.
- 연구 단위: mod slot, capacity, polarity, fusion, riven, valence fusion, foundry, economy.
- 차용 포인트: 강한 효과를 넣기 위한 슬롯 예산 퍼즐. 중복 장비 흡수로 상한을 추격하는 Valence Fusion.
- 목표 게임 번역: POE형 affix 장비와 별도로 "카드/모드형 아이템 문법"을 만든다.

### Monster Hunter World/Rise/Sunbreak/Wilds

- 포함 이유: 드랍 affix보다 재료-장비-스킬 포인트 조합이 핵심이다.
- 연구 단위: monster material, weapon tree, armor skill, decoration, talisman, augmentation, qurious crafting, endgame target farming.
- 차용 포인트: 방어구 5피스 + 장식품 + 탈리스만이 스킬 레벨을 합산하는 장비 조합표.
- 목표 게임 번역: 특정 맵/보스가 특정 장비 문법의 재료를 주게 만든다.

### Noita

- 포함 이유: wand가 spell list를 순서대로 해석하는 "아이템 내부 프로그래밍"이다.
- 연구 단위: wand stats, spell categories, modifier, multicast, trigger, timer, failure risk, UI complexity.
- 차용 포인트: projectile/modifier/trigger가 자동전투 스킬 젬 조합으로 바로 번역된다.
- 목표 게임 번역: 일부 아이템은 affix가 아니라 스킬 실행 순서를 가진다.

### Magicraft

- 포함 이유: Noita식 완드 문법을 더 빠른 탑다운/자동전투 친화 UI로 보여준다.
- 연구 단위: wand slot, boost scope, passive slot, MP, cooldown, scatter, wand spirit.
- 차용 포인트: 좌->우 주문 실행을 플레이어가 읽기 쉽게 만들고, 자동 발사 완드로 변환하는 방식.
- 목표 게임 번역: `SpellProgram`의 V1 기준. hidden wrap은 제외하고 fixed tick bytecode로 컴파일한다.

### Backpack Battles

- 포함 이유: 상점-배치-자동전투-레시피 루프가 목표 게임의 전투/제작 리듬과 직접 맞다.
- 연구 단위: item shape, grid expansion, adjacency recipe, catalyst, lock, shop reroll, auto battle trigger.
- 차용 포인트: 아이템 모양과 인접 배치가 레시피와 전투 성능을 동시에 결정한다.
- 목표 게임 번역: 전체 인벤토리가 아니라 `CharmGridBoard` 제한 보드로 가져온다.

### Backpack Hero

- 포함 이유: 인벤토리 배치 자체가 빌드 표면이다.
- 연구 단위: item shape, adjacency, orientation, synergy, trigger, UI complexity.
- 차용 포인트: 위치/인접/형상에 따라 효과가 바뀌는 공간형 장비 슬롯.
- 목표 게임 번역: 전체 인벤토리 테트리스가 아니라 charm/relic board로 제한한다.

### The Slormancer

- 포함 이유: 픽셀 ARPG 톤, 무기 정체성 성장, opt-in 부정 옵션이 목표 게임과 맞다.
- 연구 단위: Slorm Reaper, weapon XP, evolution, primordial form, benediction/malediction, reforge preview.
- 차용 포인트: 무기가 단순 베이스가 아니라 "이 빌드를 하게 만드는" 정체성으로 성장한다.
- 목표 게임 번역: `IdentityWeaponXP`를 V1 장기 무기 성장층으로 둔다.

### Terraria

- 포함 이유: 레트로 감성, 긴 crafting chain, accessory fusion, reforging이 목표 톤과 맞다.
- 연구 단위: accessory, modifier/reforge, crafting station, material chain, boss-gated progression, hardmode transition.
- 차용 포인트: 액세서리 합성으로 상위 유틸리티 아이템을 만들고, reforging은 간단한 gold sink로 작동한다.
- 목표 게임 번역: 자동전투 맵/보스별 재료가 accessory branch를 해금한다.

## Medium

### Caves of Qud

- 포함 이유: data disk, bits, item mod cap이 작은 제작 경제를 단단하게 만든다.
- 연구 단위: data disk, schematic, disassemble bits, item mod cap, tinker tier.
- 차용 포인트: 레시피 발견 -> 장비 분해 -> 제한 mod 슬롯으로 이어지는 제작 루프.
- 목표 게임 번역: `RecipeUnlock`과 `SalvageResource`를 Prototype에 포함한다.

### Black Desert Online

- 포함하되 경계. enhancement, failstack, Cron Stone, Caphras는 강력하지만 MMO식 고통과 경제 압박이 크다.
- 차용 포인트: Caphras처럼 실패 강화와 별개로 누적 성장/부분 회수/강제 돌파를 제공하는 보조 레일.

### Lost Ark

- 포함하되 제한. honing, engraving, ability stone은 유용하지만 raid MMO treadmill이 강하다.
- 차용 포인트: Ability Stone faceting의 positive/negative node 깎기.

### Old School RuneScape / RuneScape

- 장비 제작보다 경제 참고 가치가 크다.
- 차용 포인트: 제작물이 장비 가치보다 XP, 시장 수요, item sink 때문에 소비되는 구조.
- 목표 게임에서는 NPC/시뮬레이션 경제로 축약해야 한다.

### Borderlands

- crafting은 약하지만 gun parts, manufacturer, anointment, mayhem loot scaling이 유용하다.
- 차용 포인트: 같은 named item도 part/anointment로 chase가 생긴다.

### Deep Rock Galactic: Survivor

- 자동전투 장르 안에서 weapon upgrade/overclock을 쓰는 참고점.
- 차용 포인트: 자동 발사 무기가 level, upgrade, overclock으로 행동을 바꾼다.
- 목표 게임 번역: 런 중 업그레이드와 장기 아이템 크래프팅의 연결 방식을 비교한다.

## Reference Only

### Vampire Survivors

- Deep itemization 후보는 아니다.
- 차용 포인트: weapon + passive item 조건으로 evolve되는 명확한 조합 문법, reroll/skip/banish로 선택지 풀을 제어하는 UX.
- 목표 게임에서는 전투 UX와 메타 진행의 단순성 기준으로만 쓴다.

### Halls of Torment

- 목표 장르와 겉모양은 가깝지만 아이템/제작 깊이는 얕다.
- 차용 포인트: quest-based meta progression과 Diablo풍 horde survivor의 trait/item/ability synergy.

## 제외

- EVE Online: 경제/제작은 깊지만 ARPG 자동전투 아이템 문법과 거리가 너무 멀다.

## 소스

- https://store.steampowered.com/app/1289810/Siralim_Ultimate/
- https://siralimultimate.wiki.gg/wiki/Artifacts
- https://siralimultimate.wiki.gg/wiki/Creatures
- https://www.warframe.com/news/mods-guide
- https://wiki.warframe.com/w/Polarization
- https://wiki.warframe.com/w/Valence_Fusion
- https://game.capcom.com/manual/MHRISE/en/switch/page/9/4
- https://game.capcom.com/manual/MHRISE/en/steam/page/9/1
- https://mhworld.kiranico.com/index.php/en/guide/equipment
- https://noita.wiki.gg/wiki/Spells
- https://noita.wiki.gg/wiki/Wands
- https://noita.wiki.gg/wiki/Guide:_Wand_Mechanics
- https://store.steampowered.com/app/2103140/_Magicraft/
- https://magicraft.fandom.com/wiki/Wands
- https://backpackhero.wiki.gg/
- https://store.steampowered.com/app/2427700/Backpack_Battles/
- https://backpackbattles.wiki.gg/wiki/Recipe
- https://terraria.wiki.gg/wiki/Modifiers
- https://terraria.wiki.gg/wiki/Accessories
- https://store.steampowered.com/app/1104280/The_Slormancer/
- https://slormancer.fandom.com/wiki/Slorm_Reapers
- https://wiki.cavesofqud.com/wiki/Item_mods
- https://wiki.cavesofqud.com/wiki/Data_disk
- https://www.naeu.playblackdesert.com/en-us/Wiki?wikiNo=146
- https://www.playlostark.com/en-us/news/articles/lost-ark-academy-progression
- https://oldschool.runescape.wiki/w/Smithing
- https://borderlands.2k.com/news/borderlands-3-mayhem-mode/
- https://deeprockgalactic.wiki.gg/wiki/Survivor:Weapons
- https://vampire.survivors.wiki/w/Evolution
- https://store.steampowered.com/app/2218750/Halls_of_Torment/
