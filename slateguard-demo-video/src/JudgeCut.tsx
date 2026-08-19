import React from "react";
import {
  AbsoluteFill,
  Audio,
  Composition,
  Easing,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { JudgeCaptions } from "./JudgeCaptions";

const FPS = 30;
const palette = {
  paper: "#fbfdf9",
  cream: "#f3f7f2",
  green: "#16853d",
  greenDeep: "#075d2c",
  ink: "#17392a",
  line: "#dce5dd",
  muted: "#687a70",
  yellow: "#b96f0a",
};

const ease = (frame: number, start = 0, duration = 18) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

const Background: React.FC<React.PropsWithChildren> = ({ children }) => (
  <AbsoluteFill
    style={{
      background: palette.paper,
      fontFamily: "Arial, Helvetica, sans-serif",
      overflow: "hidden",
    }}
  >
    {children}
  </AbsoluteFill>
);

const FrameHeader: React.FC<{ eyebrow: string; section: string }> = ({ eyebrow, section }) => (
  <div
    style={{
      alignItems: "center",
      color: palette.muted,
      display: "flex",
      fontSize: 18,
      fontWeight: 800,
      gap: 16,
      left: 72,
      letterSpacing: 2.8,
      position: "absolute",
      textTransform: "uppercase",
      top: 56,
    }}
  >
    <span style={{ color: palette.green }}>{eyebrow}</span>
    <span style={{ background: palette.line, height: 1, width: 54 }} />
    <span>{section}</span>
  </div>
);

const Progress: React.FC<{ duration: number }> = ({ duration }) => {
  const frame = useCurrentFrame();
  const width = interpolate(frame, [0, duration * FPS], [0, 100], {
    extrapolateRight: "clamp",
  });
  return (
    <>
      <div style={{ background: "rgba(255,255,255,.1)", bottom: 38, height: 3, left: 72, position: "absolute", right: 72 }}>
        <div style={{ background: palette.green, height: "100%", width: `${width}%` }} />
      </div>
      <div style={{ bottom: 58, color: palette.muted, fontSize: 16, fontWeight: 800, left: 72, letterSpacing: 2.4, position: "absolute", textTransform: "uppercase" }}>
        SlateGuard · Evidence-first production change control
      </div>
    </>
  );
};

const AppShot: React.FC<{
  duration: number;
  image: string;
  kicker: string;
  label: string;
  note: string;
  section: string;
}> = ({ duration, image, kicker, label, note, section }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const imageOpacity = ease(frame, fps / 3);
  const zoom = interpolate(frame, [0, duration * fps], [1, 1.028], {
    extrapolateRight: "clamp",
  });

  return (
    <Background>
      <FrameHeader eyebrow={section} section={kicker} />
      <div
        style={{
          background: "#ffffff",
          border: `1px solid ${palette.line}`,
          borderRadius: 24,
          boxShadow: "0 32px 90px rgba(20, 62, 37, .12)",
          height: 744,
          left: 72,
          opacity: imageOpacity,
          overflow: "hidden",
          position: "absolute",
          right: 72,
          top: 132,
        }}
      >
        <Img
          src={staticFile(image)}
          style={{
            height: "100%",
            objectFit: "contain",
            scale: zoom,
            width: "100%",
          }}
        />
      </div>
      <div
        style={{
          background: "#ffffff",
          border: `1px solid ${palette.line}`,
          borderRadius: 999,
          color: palette.greenDeep,
          fontSize: 15,
          fontWeight: 850,
          letterSpacing: 2,
          opacity: ease(frame, fps),
          padding: "12px 18px",
          position: "absolute",
          right: 92,
          textTransform: "uppercase",
          top: 152,
        }}
      >
        {label}
      </div>
      <div style={{ color: palette.muted, fontSize: 20, left: 92, opacity: ease(frame, fps * 1.2), position: "absolute", top: 154 }}>
        {note}
      </div>
      <Progress duration={duration} />
    </Background>
  );
};

const Opening: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Background>
      <div style={{ color: palette.ink, fontSize: 88, fontWeight: 820, left: 72, letterSpacing: -4, opacity: ease(frame), position: "absolute", top: 118 }}>
        SLATE<span style={{ color: palette.green }}>GUARD</span>
      </div>
      <div style={{ background: palette.green, height: 2, left: 72, opacity: ease(frame, fps / 3), position: "absolute", top: 252, width: 360 }} />
      <div style={{ color: palette.ink, fontSize: 66, fontWeight: 700, left: 72, letterSpacing: -2.6, lineHeight: 1.04, opacity: ease(frame, fps / 2), position: "absolute", top: 345, width: 1220 }}>
        Evidence before action.<br />A durable decision after.
      </div>
      <div style={{ color: palette.muted, fontSize: 28, left: 76, lineHeight: 1.32, opacity: ease(frame, fps), position: "absolute", top: 570, width: 620 }}>
        A ClickHouse-backed production change-control agent.
      </div>
      <div style={{ alignItems: "center", bottom: 300, display: "flex", gap: 20, left: 76, opacity: ease(frame, fps * 1.5) }}>
        <span style={{ color: palette.yellow, fontSize: 31 }}>△</span>
        <span style={{ color: palette.ink, fontSize: 25, fontWeight: 700 }}>Continuity risk identified</span>
      </div>
      <Progress duration={10} />
    </Background>
  );
};

const SiteTour: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const stageIndex = Math.min(2, Math.floor(frame / ((20 * fps) / 3)));
  const stage = [
    { copy: "One supported production change keeps the review focused before the agent touches a tool.", eyebrow: "01 · Change queue", title: "Start with a clear request." },
    { copy: "The decision brief makes the proposed change, readiness, and cited ClickHouse evidence readable in one place.", eyebrow: "02 · Evidence review", title: "See why the decision matters." },
    { copy: "Risk, affected scenes, and human owners stay visible beside the decision—not buried in an agent transcript.", eyebrow: "03 · Decision context", title: "Know who changes next." },
  ][stageIndex];
  const focus = [
    { height: 430, left: 91, top: 216, width: 190 },
    { height: 430, left: 294, top: 216, width: 480 },
    { height: 430, left: 787, top: 216, width: 190 },
  ][stageIndex];

  return (
    <Background>
      <FrameHeader eyebrow="02" section="Inside the live review workspace" />
      <div style={{ background: "#ffffff", border: `1px solid ${palette.line}`, borderRadius: 24, boxShadow: "0 30px 80px rgba(20,62,37,.1)", height: 698, left: 72, overflow: "hidden", position: "absolute", top: 142, width: 930 }}>
        <Img src={staticFile("04-live-review-workspace.png")} style={{ height: "100%", objectFit: "cover", width: "100%" }} />
        <div style={{ border: `3px solid ${palette.green}`, borderRadius: 11, boxShadow: "0 0 0 999px rgba(248,252,248,.32)", height: focus.height, left: focus.left - 72, position: "absolute", top: focus.top - 142, width: focus.width }} />
      </div>
      <div style={{ left: 1070, opacity: ease(frame, fps / 2), position: "absolute", right: 92, top: 250 }}>
        <div style={{ color: palette.greenDeep, fontSize: 15, fontWeight: 850, letterSpacing: 2.1, textTransform: "uppercase" }}>{stage.eyebrow}</div>
        <div style={{ color: palette.ink, fontSize: 43, fontWeight: 770, letterSpacing: -1.6, lineHeight: 1.08, marginTop: 22 }}>{stage.title}</div>
        <div style={{ color: palette.muted, fontSize: 23, lineHeight: 1.38, marginTop: 24 }}>{stage.copy}</div>
      </div>
      <div style={{ background: "#edf7ee", border: "1px solid #cfe4d2", borderRadius: 999, color: palette.greenDeep, fontSize: 15, fontWeight: 820, letterSpacing: 1.6, padding: "12px 17px", position: "absolute", right: 92, textTransform: "uppercase", top: 670 }}>
        Built for a human decision
      </div>
      <Progress duration={20} />
    </Background>
  );
};

const MemoryBoundary: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const steps = ["Scene 12 revision", "Curated current window", "Reader MCP", "Grounded evidence"];

  return (
    <Background>
      <FrameHeader eyebrow="06" section="Why ClickHouse belongs in the agent" />
      <div style={{ color: palette.ink, fontSize: 60, fontWeight: 760, left: 72, letterSpacing: -2.4, lineHeight: 1.06, opacity: ease(frame, fps / 2), position: "absolute", top: 156, width: 1220 }}>
        Current context is the agent’s memory.
      </div>
      <div style={{ color: palette.muted, fontSize: 25, left: 76, lineHeight: 1.35, opacity: ease(frame, fps), position: "absolute", top: 320, width: 920 }}>
        ClickHouse supplies a fast, governed evidence path—not a pile of historical data for the model to guess through.
      </div>
      <div style={{ display: "flex", gap: 16, left: 72, position: "absolute", right: 72, top: 510 }}>
        {steps.map((step, index) => (
          <React.Fragment key={step}>
            <div style={{ background: "#ffffff", border: `1px solid ${palette.line}`, borderRadius: 18, boxShadow: "0 18px 45px rgba(20,62,37,.08)", color: index === steps.length - 1 ? palette.greenDeep : palette.ink, flex: 1, fontSize: 25, fontWeight: 730, minHeight: 166, opacity: ease(frame, fps + index * 7), padding: 24 }}>
              <div style={{ color: palette.green, fontSize: 13, letterSpacing: 2, marginBottom: 28 }}>0{index + 1}</div>
              {step}
            </div>
            {index < steps.length - 1 ? <div style={{ alignSelf: "center", color: palette.green, fontSize: 28, opacity: ease(frame, fps + index * 7 + 4) }}>→</div> : null}
          </React.Fragment>
        ))}
      </div>
      <div style={{ background: "#edf7ee", border: "1px solid #cfe4d2", borderRadius: 999, color: palette.greenDeep, fontSize: 16, fontWeight: 820, letterSpacing: 1.8, opacity: ease(frame, fps * 1.75), padding: "13px 19px", position: "absolute", right: 72, textTransform: "uppercase", top: 800 }}>
        No arbitrary SQL · no stale context
      </div>
      <Progress duration={20} />
    </Background>
  );
};

const Closing: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Background>
      <div style={{ color: palette.ink, fontSize: 68, fontWeight: 790, left: 72, letterSpacing: -2.8, lineHeight: 1.04, opacity: ease(frame, fps / 2), position: "absolute", top: 248, width: 1250 }}>
        Current context. Grounded decision.<br /><span style={{ color: palette.green }}>Human action.</span>
      </div>
      <div style={{ color: palette.muted, fontSize: 27, left: 76, lineHeight: 1.35, opacity: ease(frame, fps), position: "absolute", top: 465, width: 750 }}>
        SlateGuard makes creative changes operationally safe before a small mismatch becomes a shoot-day problem.
      </div>
      <div style={{ color: palette.greenDeep, fontSize: 20, fontWeight: 840, letterSpacing: 2.4, opacity: ease(frame, fps * 1.4), position: "absolute", right: 72, textTransform: "uppercase", top: 760 }}>
        07 · SlateGuard · Agentic Cinema
      </div>
      <Progress duration={10} />
    </Background>
  );
};

type JudgeCutProps = {
  narrationSrc?: string;
};

export const SlateGuardJudgeCut: React.FC<JudgeCutProps> = ({ narrationSrc }) => (
  <AbsoluteFill>
    {narrationSrc ? <Audio src={staticFile(narrationSrc)} /> : null}
    <Sequence durationInFrames={10 * FPS}><Opening /></Sequence>
    <Sequence from={10 * FPS} durationInFrames={20 * FPS}>
      <AppShot
        duration={20}
        image="04-live-review-workspace.png"
        kicker="One change, clear consequence"
        label="Live review workspace"
        note="Evidence · risk · owners · action"
        section="01"
      />
    </Sequence>
    <Sequence from={30 * FPS} durationInFrames={20 * FPS}><SiteTour /></Sequence>
    <Sequence from={50 * FPS} durationInFrames={20 * FPS}>
      <AppShot
        duration={20}
        image="05-impact-pulse-deployed.jpg"
        kicker="Reader MCP · impact pulse"
        label="Live ClickHouse query"
        note="4 evidence records · 2 affected scenes"
        section="03"
      />
    </Sequence>
    <Sequence from={70 * FPS} durationInFrames={20 * FPS}>
      <AppShot
        duration={20}
        image="02-revision-trace-confirmed.png"
        kicker="The protected core loop"
        label="Writer → Reader → Packet"
        note="Constrained identities · verified trace"
        section="04"
      />
    </Sequence>
    <Sequence from={90 * FPS} durationInFrames={20 * FPS}>
      <AppShot
        duration={20}
        image="06-deployed-decision-receipt.jpg"
        kicker="Human decision, verified result"
        label="Reader-verified receipt"
        note="The operator owns the consequential action"
        section="05"
      />
    </Sequence>
    <Sequence from={110 * FPS} durationInFrames={20 * FPS}><MemoryBoundary /></Sequence>
    <Sequence from={130 * FPS} durationInFrames={10 * FPS}><Closing /></Sequence>
    <JudgeCaptions />
  </AbsoluteFill>
);

export const SlateGuardJudgeComposition: React.FC = () => (
  <Composition
    component={SlateGuardJudgeCut}
    defaultProps={{ narrationSrc: undefined }}
    durationInFrames={140 * FPS}
    fps={FPS}
    height={1080}
    id="SlateGuardJudgeCut"
    width={1920}
  />
);
