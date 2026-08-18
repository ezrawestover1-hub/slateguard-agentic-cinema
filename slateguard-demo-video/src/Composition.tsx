import React from "react";
import {
  AbsoluteFill,
  Composition,
  Easing,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const FPS = 30;
const COLORS = {
  ink: "#07100c",
  panel: "#0b1710",
  green: "#72e89c",
  muted: "#adbaaf",
  cream: "#f1f2ec",
  yellow: "#efc64d",
  line: "rgba(175, 221, 189, 0.26)",
};

const reveal = (frame: number, start = 0, duration = 18) =>
  interpolate(frame, [start, start + duration], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

const Shell: React.FC<React.PropsWithChildren> = ({ children }) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(circle at 80% 0%, #163c24 0%, ${COLORS.ink} 46%)`,
      fontFamily: "Arial, Helvetica, sans-serif",
      overflow: "hidden",
    }}
  >
    {children}
  </AbsoluteFill>
);

const Footer = ({ duration }: { duration: number }) => {
  const frame = useCurrentFrame();
  const progress = interpolate(frame, [0, duration * FPS], [0, 100], { extrapolateRight: "clamp" });
  return (
    <>
      <div style={{ background: "rgba(255,255,255,.08)", bottom: 44, height: 4, left: 72, position: "absolute", right: 72 }}>
        <div style={{ background: COLORS.green, height: "100%", width: `${progress}%` }} />
      </div>
      <div style={{ bottom: 66, color: COLORS.muted, fontSize: 20, fontWeight: 700, left: 72, letterSpacing: 3, position: "absolute", textTransform: "uppercase" }}>
        SlateGuard · evidence-first change control
      </div>
    </>
  );
};

const Chapter = ({ number, title }: { number: string; title: string }) => (
  <div style={{ color: COLORS.muted, fontSize: 25, fontWeight: 700, letterSpacing: 4, textTransform: "uppercase" }}>
    <span style={{ color: COLORS.green, paddingRight: 16 }}>{number}</span>{title}
  </div>
);

const Caption = ({ children, delay = 0 }: React.PropsWithChildren<{ delay?: number }>) => {
  const frame = useCurrentFrame();
  return <div style={{ bottom: 126, color: COLORS.cream, fontSize: 37, fontWeight: 500, left: 72, lineHeight: 1.32, maxWidth: 1050, opacity: reveal(frame, delay), position: "absolute" }}>{children}</div>;
};

const Intro = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return <Shell>
    <div style={{ color: COLORS.cream, fontSize: 84, fontWeight: 800, left: 72, letterSpacing: -4, opacity: reveal(frame), position: "absolute", top: 116 }}>SLATE<span style={{ color: COLORS.green }}>GUARD</span></div>
    <div style={{ borderLeft: `2px solid ${COLORS.green}`, color: COLORS.cream, fontSize: 72, fontWeight: 650, left: 72, lineHeight: 1.05, opacity: reveal(frame, fps / 2), paddingLeft: 30, position: "absolute", top: 360, width: 1250 }}>Every creative change deserves evidence before action.</div>
    <div style={{ bottom: 245, color: COLORS.muted, fontSize: 31, lineHeight: 1.32, opacity: reveal(frame, fps), position: "absolute", right: 72, textAlign: "right", width: 540 }}>A ClickHouse-backed production change-control agent.</div>
    <Footer duration={15} />
  </Shell>;
};

const Risk = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return <Shell>
    <div style={{ left: 72, opacity: reveal(frame), position: "absolute", top: 76 }}><Chapter number="01" title="The production risk" /></div>
    <div style={{ color: COLORS.cream, fontSize: 70, fontWeight: 700, left: 72, letterSpacing: -2.5, opacity: reveal(frame, fps / 2), position: "absolute", top: 190 }}>Scene 12 changes from<br /><span style={{ color: COLORS.yellow }}>Blue jacket</span><span style={{ color: COLORS.green, padding: "0 25px" }}>→</span><span style={{ color: COLORS.green }}>Black jacket</span></div>
    <div style={{ border: `1px solid ${COLORS.line}`, borderRadius: 20, bottom: 265, color: COLORS.cream, left: 72, opacity: reveal(frame, fps), padding: "32px 40px", position: "absolute", width: 1040 }}>
      <div style={{ color: COLORS.green, fontSize: 22, fontWeight: 700, letterSpacing: 3, textTransform: "uppercase" }}>Why it cannot be a note in a spreadsheet</div>
      <div style={{ fontSize: 38, lineHeight: 1.32, marginTop: 16 }}>Scene 11 footage is already captured. Scenes 13 and 14 are scheduled next. A simple wardrobe change has a real continuity and scheduling blast radius.</div>
    </div>
    <Caption delay={fps * 2}>SlateGuard turns the request into a bounded, auditable decision loop.</Caption>
    <Footer duration={20} />
  </Shell>;
};

const ProofFrame = ({ image, number, title, caption, badgeColor }: { image: string; number: string; title: string; caption: string; badgeColor: string }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return <Shell>
    <div style={{ left: 72, opacity: reveal(frame), position: "absolute", top: 76 }}><Chapter number={number} title={title} /></div>
    <div style={{ border: `1px solid ${COLORS.line}`, borderRadius: 24, boxShadow: "0 36px 80px rgba(0,0,0,.45)", height: 740, opacity: reveal(frame, fps / 3), overflow: "hidden", position: "absolute", right: 72, top: 180, width: 1045 }}>
      <Img src={staticFile(image)} style={{ height: "100%", objectFit: "cover", objectPosition: "top left", scale: interpolate(frame, [0, 20 * fps], [1, 1.055], { extrapolateRight: "clamp" }), width: "100%" }} />
    </div>
    <div style={{ color: COLORS.cream, fontSize: 46, fontWeight: 650, left: 72, lineHeight: 1.16, opacity: reveal(frame, fps), position: "absolute", top: 300, width: 515 }}>{caption}</div>
    <div style={{ background: badgeColor, borderRadius: 99, color: COLORS.ink, fontSize: 21, fontWeight: 800, left: 72, letterSpacing: 2, padding: "14px 18px", position: "absolute", textTransform: "uppercase", top: 640 }}>Live production proof</div>
    <Footer duration={40} />
  </Shell>;
};

const Architecture = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const nodes = [["Command Desk", "Typed revision only"], ["Cloud Run", "Deterministic rules"], ["Official MCP", "Separate reader / writer"], ["ClickHouse Cloud", "Curated evidence + append-only events"]];
  return <Shell>
    <div style={{ left: 72, opacity: reveal(frame), position: "absolute", top: 76 }}><Chapter number="04" title="Trust boundary" /></div>
    <div style={{ color: COLORS.cream, fontSize: 60, fontWeight: 700, left: 72, letterSpacing: -2, opacity: reveal(frame, fps / 2), position: "absolute", top: 182 }}>The model explains facts. It does not control the system.</div>
    <div style={{ display: "flex", gap: 24, left: 72, position: "absolute", right: 72, top: 405 }}>
      {nodes.map(([title, detail], index) => <React.Fragment key={title}>
        <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.line}`, borderRadius: 18, minHeight: 230, opacity: reveal(frame, fps + index * 8), padding: 28, width: 360 }}>
          <div style={{ color: COLORS.green, fontSize: 20, fontWeight: 800, letterSpacing: 2 }}>0{index + 1}</div>
          <div style={{ color: COLORS.cream, fontSize: 31, fontWeight: 700, lineHeight: 1.1, marginTop: 30 }}>{title}</div>
          <div style={{ color: COLORS.muted, fontSize: 22, lineHeight: 1.35, marginTop: 18 }}>{detail}</div>
        </div>
        {index < nodes.length - 1 ? <div style={{ alignSelf: "center", color: COLORS.green, fontSize: 38, opacity: reveal(frame, fps + index * 8 + 5) }}>→</div> : null}
      </React.Fragment>)}
    </div>
    <Caption delay={fps * 3}>No browser or model input becomes SQL. A human alone creates the consequential follow-up.</Caption>
    <Footer duration={30} />
  </Shell>;
};

const Closing = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return <Shell>
    <div style={{ color: COLORS.cream, fontSize: 84, fontWeight: 750, left: 72, letterSpacing: -3, lineHeight: 1.04, opacity: reveal(frame), position: "absolute", top: 200, width: 1320 }}>Evidence before action.<br /><span style={{ color: COLORS.green }}>A durable decision after.</span></div>
    <div style={{ color: COLORS.muted, fontSize: 34, left: 72, lineHeight: 1.35, opacity: reveal(frame, fps), position: "absolute", top: 540, width: 930 }}>SlateGuard is an evidence-first production change-control agent built for the moments when a small creative revision becomes an operational risk.</div>
    <div style={{ bottom: 250, color: COLORS.green, fontSize: 33, fontWeight: 800, letterSpacing: 3, opacity: reveal(frame, fps * 2), position: "absolute", right: 72, textTransform: "uppercase" }}>SlateGuard · Agentic Cinema</div>
    <Footer duration={35} />
  </Shell>;
};

export const SlateGuardProofCut: React.FC = () => <AbsoluteFill>
  <Sequence durationInFrames={15 * FPS}><Intro /></Sequence>
  <Sequence from={15 * FPS} durationInFrames={20 * FPS}><Risk /></Sequence>
  <Sequence from={35 * FPS} durationInFrames={40 * FPS}><ProofFrame image="05-impact-pulse-deployed.jpg" number="02" title="The protected core loop" caption="Before action, the reader MCP narrows memory to four relevant evidence records and two affected scenes. The constrained writer then records the revision." badgeColor={COLORS.yellow} /></Sequence>
  <Sequence from={75 * FPS} durationInFrames={40 * FPS}><ProofFrame image="06-deployed-decision-receipt.jpg" number="03" title="Human decision, verified result" caption="Only after seeing the evidence does the script supervisor create a follow-up. The app reads back the durable readiness update through the reader path." badgeColor={COLORS.green} /></Sequence>
  <Sequence from={115 * FPS} durationInFrames={30 * FPS}><Architecture /></Sequence>
  <Sequence from={145 * FPS} durationInFrames={35 * FPS}><Closing /></Sequence>
</AbsoluteFill>;

export const SlateGuardComposition: React.FC = () => <Composition id="SlateGuardProofCut" component={SlateGuardProofCut} durationInFrames={180 * FPS} fps={FPS} height={1080} width={1920} />;
