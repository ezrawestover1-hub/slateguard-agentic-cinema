-- All names, scenes, source records, and excerpts below are fictional for the public demo.
INSERT INTO core.scenes VALUES
('scene-11', 11, 'Station corridor exit', 'shot', '2026-08-15', '2026-08-14 10:00:00.000'),
('scene-12', 12, 'Briefing room arrival', 'prepared', '2026-08-16', '2026-08-14 10:00:00.000'),
('scene-13', 13, 'Evidence locker', 'scheduled', '2026-08-16', '2026-08-14 10:00:00.000'),
('scene-14', 14, 'Squad car exterior', 'scheduled', '2026-08-16', '2026-08-14 10:00:00.000'),
('scene-15', 15, 'Archive stairwell', 'planned', '2026-08-18', '2026-08-14 10:00:00.000'),
('scene-16', 16, 'Rooftop handoff', 'planned', '2026-08-19', '2026-08-14 10:00:00.000');

INSERT INTO core.scene_fact_versions VALUES
(toUUID('00000000-0000-0000-0000-000000000011'), 'scene-11', 'wardrobe', 'blue jacket', '2026-08-15 08:00:00.000', 'src-fact-11-v4', '2026-08-15 08:00:00.000'),
(toUUID('00000000-0000-0000-0000-000000000012'), 'scene-12', 'wardrobe', 'blue jacket', '2026-08-14 09:00:00.000', 'src-fact-12-v4', '2026-08-14 09:00:00.000'),
(toUUID('00000000-0000-0000-0000-000000000013'), 'scene-13', 'wardrobe', 'blue jacket', '2026-08-14 09:00:00.000', 'src-fact-13-v4', '2026-08-14 09:00:00.000'),
(toUUID('00000000-0000-0000-0000-000000000014'), 'scene-14', 'wardrobe', 'blue jacket', '2026-08-14 09:00:00.000', 'src-fact-14-v4', '2026-08-14 09:00:00.000');

INSERT INTO core.source_evidence VALUES
('ev-dailies-11-blue', 'scene-11', 'dailies', 'blue jacket', 'shot', 'Scene 11 dailies: Maya exits the corridor in the blue jacket.', '2026-08-15 15:20:00.000'),
('ev-fact-12-blue', 'scene-12', 'fact', 'blue jacket', 'prepared', 'Prepared Scene 12 wardrobe record: blue jacket.', '2026-08-14 09:00:00.000'),
('ev-call-sheet-13', 'scene-13', 'call_sheet', 'blue jacket', 'scheduled', 'Tomorrow call sheet: Scene 13, blue jacket continuity.', '2026-08-15 18:00:00.000'),
('ev-call-sheet-14', 'scene-14', 'call_sheet', 'blue jacket', 'scheduled', 'Tomorrow call sheet: Scene 14, blue jacket continuity.', '2026-08-15 18:00:00.000');

INSERT INTO core.scene_dependencies VALUES
('dep-12-13', 'scene-12', 'scene-13', 'wardrobe_continuity', '2026-08-16', 'scheduled', 'ev-call-sheet-13'),
('dep-12-14', 'scene-12', 'scene-14', 'wardrobe_continuity', '2026-08-16', 'scheduled', 'ev-call-sheet-14');
