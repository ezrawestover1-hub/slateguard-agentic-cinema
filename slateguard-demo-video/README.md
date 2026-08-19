# SlateGuard judge video

This is the source for SlateGuard's captioned functional demo, built with Remotion. It is not a cinematic concept trailer: the cut shows the deployed product's core evidence-first loop for the ClickHouse track.

## What the judge cut proves

1. A Scene 12 wardrobe revision begins the workflow.
2. The current SlateGuard Review Workspace shows the evidence, decision brief, owners, and readiness context.
3. Curated ClickHouse reader-MCP queries reduce the decision context to relevant current production records.
4. A constrained writer → reader → Gemini Change Packet path produces a grounded decision brief.
5. A human-created follow-up ends in a reader-verified readiness receipt.

The demo uses self-authored fictional production data. The output video is intentionally ignored by Git; its public YouTube or Vimeo URL belongs in the Devpost submission, while this directory lets reviewers inspect and reproduce the cut.

## Requirements

- Node.js 20+
- pnpm 10+

## Commands

From this directory:

```sh
pnpm install --frozen-lockfile
pnpm run lint
pnpm run dev
pnpm run render:judge
```

`render:judge` produces `out/slateguard-judge-cut-140s.mp4`, a 2:20, 1920×1080 H.264 captioned visual master. The natural narration guide is in [`NARRATION.md`](./NARRATION.md).

## Source assets

- `public/04-live-review-workspace.png` is a capture of the current deployed SlateGuard workspace.
- `public/judge-captions.json` contains the timed English captions.
- `src/JudgeCut.tsx` is the judge-cut composition and timeline.
- `src/JudgeCaptions.tsx` renders captions from the shared timed-captions file.

The repository-wide [MIT License](../LICENSE) applies to this source.
