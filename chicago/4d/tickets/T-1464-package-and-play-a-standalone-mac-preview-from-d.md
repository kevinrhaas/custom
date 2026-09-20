---
id: T-1464
title: Package and play a standalone Mac preview from dev
state: claimed
epic: PIPELINE
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: T-1356
opened: 2026-09-20
closed: null
pr: null
claimed_by: local-mac 9/20/2026, 11:04:11 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Package and play a standalone Mac preview from dev.

**Executor: LOCAL MAC WITH UNREAL + XCODE.** Owner explicitly requested latest `dev`, Mac first, and a standalone game before streaming on 2026-09-20. This bounded local slice is independent of T-1361's hosting prerequisites and does not close T-1358's bundle update contract or T-1360's renderer parity.

**Acceptance:** Package a native Apple Silicon Mac application using current committed terrain and structure glTF/sidecars from dev snapshot `253f026570358dfcdab62fb2593c4082b058de07`. Start directly in Chicago with a body-free walking character and demonstrate the packaged app launching without the editor or streaming server. Record source/engine/toolchain, controls, output location, normal movement/collision observations, missing renderer features, and distribution limitations. Commit reproducible Unreal project and import/build source to dev through an isolated branch. Do not close streaming/parity tickets based on this preview.

The owner prioritised this local build now. Remote web workers cannot complete this without the engine, SDK and graphical Mac session. If local execution stops unfinished, restore blocked-tech with the concrete remaining prerequisite.

### Owner-reported fence, 2026-09-20

The owner reported a fence near the fort hanging in the air. Include the Unreal
placement correction in this local build: match the existing browser's lowest
rotated-footprint terrain anchoring, measure the fort garden fence/palisade offsets,
and rebuild the app. Do not invent new geometry or historical dimensions.
