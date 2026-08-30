import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const ThreeJSRocket: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // --- Scene Setup ---
    const canvas = document.createElement('canvas');
    containerRef.current.appendChild(canvas);
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
    camera.position.z = 7;

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0); // Transparent void
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;

    // --- Environment (realistic metal reflections) ---
    const pmrem = new THREE.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;

    // --- Postprocessing (Bloom) ---
    const renderScene = new RenderPass(scene, camera);
    const bloomPass = new UnrealBloomPass(
      new THREE.Vector2(window.innerWidth, window.innerHeight),
      0.9,   // strength
      0.5,   // radius
      0.12   // threshold
    );
    const composer = new EffectComposer(renderer);
    composer.addPass(renderScene);
    composer.addPass(bloomPass);

    // --- Reactor Geometry ---
    const reactorGroup = new THREE.Group();
    reactorGroup.rotation.x = -0.28; // tilt for realistic 3D viewing angle
    scene.add(reactorGroup);

    // 1. Plasma Core (hot, emissive)
    const coreGeo = new THREE.SphereGeometry(0.55, 64, 64);
    const coreMat = new THREE.MeshStandardMaterial({
      color: 0xff5a4a,
      emissive: 0xff2a1a,
      emissiveIntensity: 2.4,
      roughness: 0.35,
      metalness: 0.0
    });
    const core = new THREE.Mesh(coreGeo, coreMat);
    reactorGroup.add(core);

    // 1b. White-hot center
    const innerGeo = new THREE.SphereGeometry(0.22, 32, 32);
    const innerMat = new THREE.MeshBasicMaterial({ color: 0xffe6dc });
    const inner = new THREE.Mesh(innerGeo, innerMat);
    reactorGroup.add(inner);

    // 2. Faint energy cage (icosahedron shell)
    const shellGeo = new THREE.IcosahedronGeometry(0.95, 1);
    const shellMat = new THREE.MeshStandardMaterial({
      color: 0x110000,
      emissive: 0x440000,
      wireframe: true,
      transparent: true,
      opacity: 0.3
    });
    const shell = new THREE.Mesh(shellGeo, shellMat);
    reactorGroup.add(shell);

    // 3. Backing housing disc (recesses the core)
    const housingGeo = new THREE.CylinderGeometry(1.9, 1.9, 0.3, 64);
    const housingMat = new THREE.MeshStandardMaterial({
      color: 0x15171c,
      metalness: 0.95,
      roughness: 0.35
    });
    const housing = new THREE.Mesh(housingGeo, housingMat);
    housing.rotation.x = Math.PI / 2;
    housing.position.z = -0.4;
    reactorGroup.add(housing);

    // 4. Outer polished metal ring
    const ringGeo = new THREE.TorusGeometry(1.85, 0.18, 32, 200);
    const ringMat = new THREE.MeshStandardMaterial({
      color: 0x2a2d33,
      metalness: 1.0,
      roughness: 0.18,
      envMapIntensity: 1.4
    });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    reactorGroup.add(ring);

    // 5. Segmented paddle ring (arc reactor signature, 12 segments)
    const segGroup = new THREE.Group();
    const segGeo = new THREE.BoxGeometry(0.16, 0.55, 0.14);
    const segMat = new THREE.MeshStandardMaterial({
      color: 0x3a3d44,
      metalness: 1.0,
      roughness: 0.22,
      envMapIntensity: 1.2
    });
    for (let i = 0; i < 12; i++) {
      const s = new THREE.Mesh(segGeo, segMat);
      const a = (i / 12) * Math.PI * 2;
      s.position.set(Math.cos(a) * 1.5, Math.sin(a) * 1.5, 0);
      s.rotation.z = a;
      segGroup.add(s);
    }
    reactorGroup.add(segGroup);

    // 6. Thin red accent torus
    const accentGeo = new THREE.TorusGeometry(1.3, 0.02, 16, 160);
    const accentMat = new THREE.MeshBasicMaterial({ color: 0xff3b4e });
    const accentRing = new THREE.Mesh(accentGeo, accentMat);
    reactorGroup.add(accentRing);

    // 7. Blue holographic secondary ring
    const holoGeo = new THREE.TorusGeometry(1.05, 0.015, 16, 120);
    const holoMat = new THREE.MeshBasicMaterial({ color: 0x4f9dff, transparent: true, opacity: 0.55 });
    const holoRing = new THREE.Mesh(holoGeo, holoMat);
    reactorGroup.add(holoRing);

    // 8. Particle Dust
    const dustGeo = new THREE.BufferGeometry();
    const dustCount = 1400;
    const posArray = new Float32Array(dustCount * 3);
    for (let i = 0; i < dustCount * 3; i++) {
      posArray[i] = (Math.random() - 0.5) * 15;
    }
    dustGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const dustMat = new THREE.PointsMaterial({
      size: 0.02,
      color: 0xff5a4a,
      blending: THREE.AdditiveBlending,
      transparent: true,
      opacity: 0.4
    });
    const dust = new THREE.Points(dustGeo, dustMat);
    scene.add(dust);

    // --- Lighting ---
    const ambientLight = new THREE.AmbientLight(0x332222, 0.6);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 1.4);
    keyLight.position.set(3, 4, 5);
    scene.add(keyLight);

    const rimLight = new THREE.PointLight(0xff3b30, 6, 14);
    rimLight.position.set(0, 0, -1.5);
    scene.add(rimLight);

    const holoLight = new THREE.PointLight(0x4f9dff, 2.4, 14);
    holoLight.position.set(2.5, -1.5, 1.5);
    scene.add(holoLight);

    // light spilling from the hot core
    const coreLight = new THREE.PointLight(0xff5a4a, 3, 8);
    coreLight.position.set(0, 0, 0.6);
    reactorGroup.add(coreLight);

    // --- Interaction & Animation ---
    let scrollY = window.scrollY;
    let mouseX = 0;
    let mouseY = 0;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    window.addEventListener('scroll', () => {
      scrollY = window.scrollY;
    });

    document.addEventListener('mousemove', (event) => {
      if (prefersReducedMotion) return;
      mouseX = (event.clientX / window.innerWidth) - 0.5;
      mouseY = (event.clientY / window.innerHeight) - 0.5;
    });

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
      composer.setSize(window.innerWidth, window.innerHeight);
    });

    const clock = new THREE.Clock();

    function animate() {
      requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      if (!prefersReducedMotion) {
        // core pulse + hot center
        const pulse = Math.sin(elapsedTime * 2) * 0.08 + 1;
        core.scale.set(pulse, pulse, pulse);
        inner.scale.setScalar(0.9 + Math.sin(elapsedTime * 3) * 0.1);
        coreMat.emissiveIntensity = 2.2 + Math.sin(elapsedTime * 2) * 0.4;

        // rings spin at different rates for depth
        ring.rotation.z -= 0.004;
        segGroup.rotation.z += 0.006;
        accentRing.rotation.z += 0.005;
        holoRing.rotation.y -= 0.008;
        holoRing.rotation.z += 0.004;
        shell.rotation.y += 0.005;
        shell.rotation.x += 0.002;

        dust.rotation.y = elapsedTime * 0.02;
      }

      // Scroll pushes camera in (z: 7 -> ~3.8)
      const maxScroll = document.body.scrollHeight - window.innerHeight;
      const scrollRatio = maxScroll > 0 ? scrollY / maxScroll : 0;
      const targetZ = 7 - (scrollRatio * 3.2);
      camera.position.z += (targetZ - camera.position.z) * 0.05;
      reactorGroup.rotation.y = scrollRatio * Math.PI * 0.5;

      // Pointer parallax (subtle 3D viewing)
      if (!prefersReducedMotion) {
        const targetX = mouseX * 1.6;
        const targetY = -mouseY * 1.6;
        camera.position.x += (targetX - camera.position.x) * 0.05;
        camera.position.y += (targetY - camera.position.y) * 0.05;
      }

      composer.render();
    }

    animate();

    // Cleanup
    return () => {
      // Dispose geometries and materials
      coreGeo.dispose();
      coreMat.dispose();
      innerGeo.dispose();
      innerMat.dispose();
      shellGeo.dispose();
      shellMat.dispose();
      housingGeo.dispose();
      housingMat.dispose();
      ringGeo.dispose();
      ringMat.dispose();
      segGeo.dispose();
      segMat.dispose();
      accentGeo.dispose();
      accentMat.dispose();
      holoGeo.dispose();
      holoMat.dispose;
      dustGeo.dispose();
      dustMat.dispose();
      
      // Dispose lights
      ambientLight.dispose();
      keyLight.dispose();
      rimLight.dispose();
      holoLight.dispose();
      coreLight.dispose();
      
      // Dispose renderer
      renderer.dispose();
      
      // Remove event listeners
      window.removeEventListener('scroll', () => {});
      document.removeEventListener('mousemove', () => {});
      window.removeEventListener('resize', () => {});
    };
  }, []);

  return <div ref={containerRef} style={{ width: '100%', height: '100%', position: 'fixed', inset: 0, zIndex: -1 }} />;
};

export default ThreeJSRocket;