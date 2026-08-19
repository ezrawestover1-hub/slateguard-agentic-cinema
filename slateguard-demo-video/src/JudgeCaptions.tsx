import type { Caption } from "@remotion/captions";
import React, { useCallback, useEffect, useState } from "react";
import {
  AbsoluteFill,
  Easing,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useDelayRender,
  useVideoConfig,
} from "remotion";

const CaptionPage: React.FC<{ caption: Caption; durationInFrames: number }> = ({ caption, durationInFrames }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 9, Math.max(10, durationInFrames - 8), durationInFrames], [0, 1, 1, 0], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const translateY = interpolate(frame, [0, 12], [18, 0], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end", pointerEvents: "none" }}>
      <div
        style={{
          background: "rgba(255, 255, 255, 0.96)",
          border: "1px solid #cbd9cf",
          borderRadius: 18,
          boxShadow: "0 18px 50px rgba(20, 62, 37, .16)",
          color: "#17392a",
          fontFamily: "Arial, Helvetica, sans-serif",
          fontSize: 34,
          fontWeight: 650,
          lineHeight: 1.28,
          marginBottom: 92,
          maxWidth: 1260,
          opacity,
          padding: "22px 34px",
          textAlign: "center",
          translate: `0 ${translateY}px`,
        }}
      >
        {caption.text}
      </div>
    </AbsoluteFill>
  );
};

export const JudgeCaptions: React.FC = () => {
  const [captions, setCaptions] = useState<Caption[] | null>(null);
  const { cancelRender, continueRender, delayRender } = useDelayRender();
  const [handle] = useState(() => delayRender("Load judge captions"));
  const { fps } = useVideoConfig();

  const loadCaptions = useCallback(async () => {
    try {
      const response = await fetch(staticFile("judge-captions.json"));
      if (!response.ok) {
        throw new Error(`Unable to load captions: ${response.status}`);
      }
      setCaptions((await response.json()) as Caption[]);
      continueRender(handle);
    } catch (error) {
      cancelRender(error);
    }
  }, [cancelRender, continueRender, handle]);

  useEffect(() => {
    loadCaptions();
  }, [loadCaptions]);

  if (!captions) {
    return null;
  }

  return (
    <AbsoluteFill>
      {captions.map((caption) => {
        const from = Math.round((caption.startMs / 1000) * fps);
        const durationInFrames = Math.max(1, Math.round(((caption.endMs - caption.startMs) / 1000) * fps));
        return (
          <Sequence durationInFrames={durationInFrames} from={from} key={`${caption.startMs}-${caption.text}`} layout="none">
            <CaptionPage caption={caption} durationInFrames={durationInFrames} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
