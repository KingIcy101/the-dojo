---
name: timing
description: Interpolation curves in Remotion - linear, easing, spring animations
metadata:
  tags: spring, bounce, easing, interpolation
---

A simple linear interpolation is done using the `interpolate` function.

```ts title="Going from 0 to 1 over 100 frames"
import { interpolate } from "remotion";

const opacity = interpolate(frame, [0, 100], [0, 1]);
```

By default, values are not clamped. Clamp like this:

```ts
const opacity = interpolate(frame, [0, 100], [0, 1], {
  extrapolateRight: "clamp",
  extrapolateLeft: "clamp",
});
```

## Spring animations

Spring animations have a more natural motion. They go from 0 to 1 over time.

```ts
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const scale = spring({ frame, fps });
```

### Physical properties

Default: `mass: 1, damping: 10, stiffness: 100` (has bounce before settling).

```ts
const smooth = { damping: 200 };              // Smooth, no bounce (subtle reveals)
const snappy = { damping: 20, stiffness: 200 }; // Snappy, minimal bounce (UI elements)
const bouncy = { damping: 8 };                // Bouncy entrance (playful animations)
const heavy = { damping: 15, stiffness: 80, mass: 2 }; // Heavy, slow, small bounce
```

### Delay

```tsx
const entrance = spring({
  frame: frame - ENTRANCE_DELAY,
  fps,
  delay: 20,
});
```

### Duration

```tsx
const anim = spring({
  frame,
  fps,
  durationInFrames: 40,
});
```

### Combining spring() with interpolate()

```tsx
const springProgress = spring({ frame, fps });
const rotation = interpolate(springProgress, [0, 1], [0, 360]);
<div style={{ rotate: rotation + "deg" }} />;
```

### In + Out springs

```tsx
const inAnimation = spring({ frame, fps });
const outAnimation = spring({
  frame,
  fps,
  durationInFrames: 1 * fps,
  delay: durationInFrames - 1 * fps,
});
const scale = inAnimation - outAnimation;
```

## Easing

```ts
import { interpolate, Easing } from "remotion";

const value = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.inOut(Easing.quad),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

Curves (most linear → most curved): `Easing.quad`, `Easing.sin`, `Easing.exp`, `Easing.circle`
Convexities: `Easing.in`, `Easing.out`, `Easing.inOut`

Cubic bezier:
```ts
easing: Easing.bezier(0.8, 0.22, 0.96, 0.65)
```
