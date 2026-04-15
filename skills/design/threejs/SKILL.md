---
name: threejs
description: Three.js — 3D scenes, particle systems, WebGL hero sections. Use for hero sections that need real visual impact beyond CSS. Pairs with React Three Fiber (R3F) for React/Next.js builds.
---

# Three.js — 3D Web Graphics

## React Three Fiber (use this, not raw Three.js in React)
```bash
npm install three @react-three/fiber @react-three/drei
```

## Basic Scene
```tsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Sphere, MeshDistortMaterial } from '@react-three/drei'

export function HeroScene() {
  return (
    <Canvas camera={{ position: [0, 0, 5] }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} />
      <Sphere args={[1, 100, 200]} scale={2.4}>
        <MeshDistortMaterial
          color="#3d1c8e"
          attach="material"
          distort={0.5}
          speed={2}
        />
      </Sphere>
      <OrbitControls enableZoom={false} />
    </Canvas>
  )
}
```

## Particle System (hero backgrounds)
```tsx
import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

export function Particles({ count = 5000 }) {
  const mesh = useRef()
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 10
      pos[i * 3 + 1] = (Math.random() - 0.5) * 10
      pos[i * 3 + 2] = (Math.random() - 0.5) * 10
    }
    return pos
  }, [count])

  useFrame((state) => {
    mesh.current.rotation.x = state.clock.elapsedTime * 0.05
    mesh.current.rotation.y = state.clock.elapsedTime * 0.075
  })

  return (
    <points ref={mesh}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" count={count} array={positions} itemSize={3} />
      </bufferGeometry>
      <pointsMaterial size={0.01} color="#ffffff" sizeAttenuation />
    </points>
  )
}
```

## When to Use
- Hero sections needing 3D orbs, particles, fluid shapes
- Product showcase with 3D model
- Abstract animated backgrounds

## When NOT to Use
- Simple animations → use Framer Motion or GSAP
- Static visuals → use CSS/SVG
- When performance is critical on mobile → test thoroughly

## Performance Rules
- Always set `dpr={[1, 2]}` on Canvas to cap pixel ratio
- Dispose geometries and materials on unmount
- Use `Suspense` for loading 3D assets
- Test on mobile — 3D is expensive, have a fallback


## Learned from Use (2026-03-22)
## Learned from Use (2026-03-22)

- **Canvas sizing is critical for Three.js deployment** — Agent Lounge scene failed because canvas was stuck at 300x150px due to CSS/HTML bugs in the build output, not the Three.js code itself. Always verify responsive canvas dimensions match viewport before handoff.

- **Three.js scenes need visual completeness for approval** — Forge's skeleton (camera, desks, activity dots) was technically correct but rejected because avatars, name labels, and accent colors were missing. Three.js implementations must include the full visual layer specified in the brief, not just structural geometry.

- **Brief clarity matters upstream of Three.js implementation** — Pixel's rejection traced back to Forge not understanding that visual requirements (avatars, backgrounds, labels) were mandatory, not optional. When briefing Three.js work, explicitly call out that rendering/visual assets are non-negotiable deliverables.
