import { Scene } from '@babylonjs/core/scene';
import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { MeshBuilder } from '@babylonjs/core/Meshes/meshBuilder';
import { TransformNode } from '@babylonjs/core/Meshes/transformNode';
import { Vector3, Vector4 } from '@babylonjs/core/Maths/math.vector';
import { Color3 } from '@babylonjs/core/Maths/math.color';
import type { PBRMaterial } from '@babylonjs/core/Materials/PBR/pbrMaterial';
import { VertexData } from '@babylonjs/core/Meshes/mesh.vertexData';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial';

import '@babylonjs/core/Meshes/thinInstanceMesh';

/**
 * The Old Joliet architectural kit.
 *
 * Boyington's vocabulary is small and repetitive, which is a gift: a coursed
 * rusticated wall, a corbelled cap, octagonal tower cabs on tapered shafts,
 * segmental-arched openings, stepped buttresses. Building these as parametric
 * generators rather than hand-modelled meshes means every scene gets the same
 * proportions, and the whole site is a few hundred KB of code.
 *
 * Dimensions come from docs/RESEARCH.md. Where research could not establish a
 * figure, the default is marked ESTIMATED and listed in
 * docs/HISTORICAL-LIBERTIES.md.
 */

export interface KitContext {
  scene: Scene;
  /** Everything registered here gets shadow-cast, collision and world UVs. */
  register(
    mesh: Mesh,
    opts?: {
      collide?: boolean;
      cast?: boolean;
      surface?: string;
      /** Texture repeats per metre. Omit for the global default. */
      uvDensity?: number;
      /** Skip UV reprojection (for meshes with authored UVs). */
      keepUV?: boolean;
    },
  ): void;
}

/* -------------------------------------------------------------------------- */
/*  World-space UV projection                                                 */
/* -------------------------------------------------------------------------- */

/**
 * Re-project a mesh's UVs into world-space units.
 *
 * Materials in the library are shared and frozen, so their uScale/vScale is a
 * single constant — which means an 88 m wall and a 0.7 m corbel would get the
 * same number of texture repeats, and the wall's stone would stretch into flat
 * mush. (It did. That was iteration 3.)
 *
 * This rewrites each vertex's UV from its position, projected on whichever
 * axis its normal points down — box mapping. Texel density is then identical on
 * every surface in the game regardless of object size, seams land on face
 * boundaries where the geometry already breaks, and no scene has to think about
 * tiling at all.
 *
 * `density` is texture repeats per metre: 1/3 means one tile covers 3 m.
 */
export function worldUV(mesh: Mesh, density = 1 / 3, offset = 0): void {
  const positions = mesh.getVerticesData('position');
  const normals = mesh.getVerticesData('normal');
  if (!positions || !normals) return;

  const uvs = new Float32Array((positions.length / 3) * 2);
  for (let i = 0, j = 0; i < positions.length; i += 3, j += 2) {
    const px = positions[i];
    const py = positions[i + 1];
    const pz = positions[i + 2];
    const nx = Math.abs(normals[i]);
    const ny = Math.abs(normals[i + 1]);
    const nz = Math.abs(normals[i + 2]);

    let u: number;
    let v: number;
    if (ny >= nx && ny >= nz) {
      // Floor / ceiling: project on XZ.
      u = px;
      v = pz;
    } else if (nx >= nz) {
      // Facing ±X: project on ZY.
      u = pz;
      v = py;
    } else {
      // Facing ±Z: project on XY.
      u = px;
      v = py;
    }
    uvs[j] = u * density + offset;
    uvs[j + 1] = v * density + offset;
  }
  mesh.setVerticesData('uv', uvs, false);
}

/* -------------------------------------------------------------------------- */
/*  Perimeter wall                                                            */
/* -------------------------------------------------------------------------- */

export interface WallOptions {
  length: number;
  /** Wall height to the underside of the cap. Reference: ~25 ft ≈ 7.6 m. */
  height?: number;
  thickness?: number;
  /** Corbel blocks projecting under the cap course. */
  corbels?: boolean;
  /** The line of thin steel posts + slack barbed wire along the top. */
  barbedWire?: boolean;
}

/**
 * A run of perimeter wall, built along +X, centred on the origin.
 *
 * The distinguishing features in the reference are the corbel course under the
 * cap and the thin barbed-wire stanchions above it — both are what makes the
 * silhouette read as Joliet rather than generic prison.
 */
export function buildWall(
  ctx: KitContext,
  mats: { stone: PBRMaterial; metal: PBRMaterial },
  o: WallOptions,
): TransformNode {
  const { length, height = 7.6, thickness = 1.1, corbels = true, barbedWire = true } = o;
  const root = new TransformNode('wall', ctx.scene);

  // Main mass. Slight batter (taper) — the real wall is thicker at the base.
  const body = MeshBuilder.CreateBox(
    'wallBody',
    { width: length, height, depth: thickness },
    ctx.scene,
  );
  body.position.y = height / 2;
  body.material = mats.stone;
  body.parent = root;
  ctx.register(body, { collide: true, cast: true, surface: 'stone' });

  if (corbels) {
    // Corbel course: a row of projecting blocks just under the cap. Built as
    // thin instances — there can be 200 of them along one wall run.
    const corbel = MeshBuilder.CreateBox(
      'corbel',
      { width: 0.34, height: 0.3, depth: thickness + 0.34 },
      ctx.scene,
    );
    corbel.material = mats.stone;
    corbel.parent = root;

    const spacing = 0.92;
    const count = Math.floor(length / spacing);
    const matrices = new Float32Array(count * 16);
    for (let i = 0; i < count; i++) {
      const x = -length / 2 + spacing * (i + 0.5);
      const offset = i * 16;
      // Identity with translation — no rotation needed.
      matrices[offset + 0] = 1;
      matrices[offset + 5] = 1;
      matrices[offset + 10] = 1;
      matrices[offset + 15] = 1;
      matrices[offset + 12] = x;
      matrices[offset + 13] = height - 0.5;
      matrices[offset + 14] = 0;
    }
    corbel.thinInstanceSetBuffer('matrix', matrices, 16);
    ctx.register(corbel, { collide: false, cast: true });

    // Cap course sits on the corbels and oversails slightly.
    const cap = MeshBuilder.CreateBox(
      'wallCap',
      { width: length, height: 0.34, depth: thickness + 0.42 },
      ctx.scene,
    );
    cap.position.y = height + 0.17;
    cap.material = mats.stone;
    cap.parent = root;
    ctx.register(cap, { collide: true, cast: true, surface: 'stone' });
  }

  if (barbedWire) {
    root.addChild(buildBarbedWireLine(ctx, mats.metal, length, height + 0.34));
  }

  return root;
}

/**
 * The barbed-wire line: thin vertical posts with slack catenary strands.
 *
 * Slack matters. Taut straight lines read as CAD; the reference wire visibly
 * sags between every post and that sag is the whole silhouette against the
 * sky.
 */
export function buildBarbedWireLine(
  ctx: KitContext,
  metal: PBRMaterial,
  length: number,
  baseY: number,
): TransformNode {
  const root = new TransformNode('barbedWire', ctx.scene);
  const spacing = 2.4;
  const posts = Math.max(2, Math.floor(length / spacing) + 1);
  const postH = 1.35;

  const post = MeshBuilder.CreateCylinder(
    'wirePost',
    { height: postH, diameter: 0.05, tessellation: 6 },
    ctx.scene,
  );
  post.material = metal;
  post.parent = root;
  const pm = new Float32Array(posts * 16);
  for (let i = 0; i < posts; i++) {
    const x = -length / 2 + spacing * i;
    const o = i * 16;
    pm[o] = pm[o + 5] = pm[o + 10] = pm[o + 15] = 1;
    pm[o + 12] = x;
    pm[o + 13] = baseY + postH / 2;
    pm[o + 14] = 0;
  }
  post.thinInstanceSetBuffer('matrix', pm, 16);
  ctx.register(post, { collide: false, cast: true });

  // Strands as tube ribbons with catenary sag.
  const strandHeights = [0.28, 0.62, 0.96, 1.28];
  for (let s = 0; s < strandHeights.length; s++) {
    const pts: Vector3[] = [];
    const segs = posts * 6;
    for (let i = 0; i <= segs; i++) {
      const t = i / segs;
      const x = -length / 2 + t * length;
      // Sag between each pair of posts.
      const local = ((x + length / 2) % spacing) / spacing;
      const sag = Math.sin(local * Math.PI) * 0.055 * (1 + s * 0.12);
      pts.push(new Vector3(x, baseY + strandHeights[s] - sag, 0));
    }
    const strand = MeshBuilder.CreateTube(
      `strand${s}`,
      { path: pts, radius: 0.008, tessellation: 4, updatable: false },
      ctx.scene,
    );
    strand.material = metal;
    strand.parent = root;
    ctx.register(strand, { collide: false, cast: true });
  }

  return root;
}

/* -------------------------------------------------------------------------- */
/*  Guard tower                                                               */
/* -------------------------------------------------------------------------- */

export interface TowerOptions {
  /** Height from grade to the underside of the corbel collar. */
  shaftHeight?: number;
  /** Radius at the base. The shaft tapers to ~0.82 of this at the collar. */
  baseRadius?: number;
  /** 'octagon' = the classic glazed cab; 'crenellated' = the corner turrets. */
  cab?: 'octagon' | 'crenellated' | 'none';
}

/**
 * A wall tower. The reference type is a tapered rusticated stone shaft, a
 * heavy corbelled collar of stepped blocks, and an octagonal glazed cab with a
 * hipped shingle roof and a small finial.
 */
export function buildTower(
  ctx: KitContext,
  mats: { stone: PBRMaterial; metal: PBRMaterial; glass: PBRMaterial; roof: PBRMaterial },
  o: TowerOptions = {},
): TransformNode {
  const { shaftHeight = 9.4, baseRadius = 1.85, cab = 'octagon' } = o;
  const root = new TransformNode('tower', ctx.scene);

  // Tapered shaft. 16-sided reads as round at any distance the player can get
  // to it, and costs a third of a smooth cylinder.
  const shaft = MeshBuilder.CreateCylinder(
    'towerShaft',
    {
      height: shaftHeight,
      diameterTop: baseRadius * 2 * 0.82,
      diameterBottom: baseRadius * 2,
      tessellation: 16,
    },
    ctx.scene,
  );
  shaft.position.y = shaftHeight / 2;
  shaft.material = mats.stone;
  shaft.parent = root;
  ctx.register(shaft, { collide: true, cast: true, surface: 'stone' });

  // Corbelled collar: three stepped rings, each oversailing the last. This is
  // the tower's signature and it must not be a plain flare.
  const collarR = baseRadius * 0.82;
  for (let i = 0; i < 3; i++) {
    const ring = MeshBuilder.CreateCylinder(
      `collar${i}`,
      {
        height: 0.32,
        diameterTop: (collarR + 0.16 * (i + 1)) * 2,
        diameterBottom: (collarR + 0.16 * i) * 2,
        tessellation: 16,
      },
      ctx.scene,
    );
    ring.position.y = shaftHeight + 0.16 + i * 0.32;
    ring.material = mats.stone;
    ring.parent = root;
    ctx.register(ring, { collide: false, cast: true });
  }

  const collarTop = shaftHeight + 0.16 + 3 * 0.32;

  if (cab === 'octagon') {
    const cabR = collarR + 0.5;
    const cabH = 2.1;

    // Sill band.
    const sill = MeshBuilder.CreateCylinder(
      'cabSill',
      { height: 0.42, diameter: cabR * 2, tessellation: 8 },
      ctx.scene,
    );
    sill.position.y = collarTop + 0.21;
    sill.material = mats.stone;
    sill.parent = root;
    ctx.register(sill, { collide: true, cast: true });

    // Glazing: an octagonal band. Most panes in the reference are broken or
    // boarded, so the scene can hide individual faces.
    const glazing = MeshBuilder.CreateCylinder(
      'cabGlazing',
      { height: cabH, diameter: cabR * 2 * 0.985, tessellation: 8 },
      ctx.scene,
    );
    glazing.position.y = collarTop + 0.42 + cabH / 2;
    glazing.material = mats.glass;
    glazing.parent = root;
    ctx.register(glazing, { collide: true, cast: false });

    // Mullions between the panes.
    const mullion = MeshBuilder.CreateBox(
      'mullion',
      { width: 0.09, height: cabH, depth: 0.09 },
      ctx.scene,
    );
    mullion.material = mats.metal;
    mullion.parent = root;
    const mm = new Float32Array(8 * 16);
    for (let i = 0; i < 8; i++) {
      const a = (i / 8) * Math.PI * 2 + Math.PI / 8;
      const o2 = i * 16;
      const ca = Math.cos(a);
      const sa = Math.sin(a);
      // Rotation about Y by `a`, translation to the octagon vertex.
      mm[o2 + 0] = ca;
      mm[o2 + 2] = -sa;
      mm[o2 + 5] = 1;
      mm[o2 + 8] = sa;
      mm[o2 + 10] = ca;
      mm[o2 + 15] = 1;
      mm[o2 + 12] = Math.cos(a) * cabR * 0.96;
      mm[o2 + 13] = collarTop + 0.42 + cabH / 2;
      mm[o2 + 14] = Math.sin(a) * cabR * 0.96;
    }
    mullion.thinInstanceSetBuffer('matrix', mm, 16);
    ctx.register(mullion, { collide: false, cast: true });

    // Hipped shingle roof with a deep overhang and a finial.
    const roof = MeshBuilder.CreateCylinder(
      'cabRoof',
      { height: 0.95, diameterTop: 0.12, diameterBottom: cabR * 2 + 0.55, tessellation: 8 },
      ctx.scene,
    );
    roof.position.y = collarTop + 0.42 + cabH + 0.475;
    roof.material = mats.roof;
    roof.parent = root;
    ctx.register(roof, { collide: false, cast: true });

    const finial = MeshBuilder.CreateSphere('finial', { diameter: 0.17, segments: 6 }, ctx.scene);
    finial.position.y = collarTop + 0.42 + cabH + 1.0;
    finial.material = mats.metal;
    finial.parent = root;
    ctx.register(finial, { collide: false, cast: true });
  } else if (cab === 'crenellated') {
    root.addChild(buildCrenellation(ctx, mats.stone, collarR + 0.2, collarTop));
  }

  return root;
}

/** Merlons + embrasures for the corner turrets on the admin block. */
export function buildCrenellation(
  ctx: KitContext,
  stone: PBRMaterial,
  radius: number,
  y: number,
  count = 10,
): TransformNode {
  const root = new TransformNode('crenellation', ctx.scene);
  const merlon = MeshBuilder.CreateBox(
    'merlon',
    { width: 0.52, height: 0.72, depth: 0.42 },
    ctx.scene,
  );
  merlon.material = stone;
  merlon.parent = root;

  const m = new Float32Array(count * 16);
  for (let i = 0; i < count; i++) {
    const a = (i / count) * Math.PI * 2;
    const o = i * 16;
    const ca = Math.cos(a);
    const sa = Math.sin(a);
    m[o + 0] = ca;
    m[o + 2] = -sa;
    m[o + 5] = 1;
    m[o + 8] = sa;
    m[o + 10] = ca;
    m[o + 15] = 1;
    m[o + 12] = ca * radius;
    m[o + 13] = y + 0.36;
    m[o + 14] = sa * radius;
  }
  merlon.thinInstanceSetBuffer('matrix', m, 16);
  ctx.register(merlon, { collide: false, cast: true });
  return root;
}

/* -------------------------------------------------------------------------- */
/*  Openings                                                                  */
/* -------------------------------------------------------------------------- */

/**
 * A barred window opening: a recessed reveal, a segmental arch head, a stone
 * sill, and a grid of bars. Used across the cell house and shop elevations.
 */
export function buildBarredWindow(
  ctx: KitContext,
  mats: { stone: PBRMaterial; metal: PBRMaterial; glass?: PBRMaterial },
  o: { width?: number; height?: number; bars?: number; arched?: boolean } = {},
): TransformNode {
  const { width = 1.15, height = 2.35, bars = 5, arched = true } = o;
  const root = new TransformNode('window', ctx.scene);

  // Reveal box — the dark recess. Depth is what sells a masonry opening.
  const reveal = MeshBuilder.CreateBox(
    'reveal',
    { width, height, depth: 0.52 },
    ctx.scene,
  );
  reveal.position.z = 0.3;
  const dark = new StandardMaterial('revealDark', ctx.scene);
  dark.diffuseColor = new Color3(0.012, 0.013, 0.015);
  dark.specularColor = Color3.Black();
  dark.disableLighting = true;
  reveal.material = dark;
  reveal.parent = root;
  ctx.register(reveal, { collide: false, cast: false });

  // Sill: projects and is sloped to shed water.
  const sill = MeshBuilder.CreateBox(
    'sill',
    { width: width + 0.4, height: 0.16, depth: 0.42 },
    ctx.scene,
  );
  sill.position.set(0, -height / 2 - 0.08, -0.08);
  sill.rotation.x = -0.07;
  sill.material = mats.stone;
  sill.parent = root;
  ctx.register(sill, { collide: false, cast: true });

  if (arched) {
    // Segmental arch: voussoirs on a shallow arc.
    const n = 7;
    const rise = 0.28;
    const R = (width * width) / (8 * rise) + rise / 2;
    for (let i = 0; i < n; i++) {
      const t = (i + 0.5) / n;
      const a = (t - 0.5) * (width / R);
      const v = MeshBuilder.CreateBox(
        `voussoir${i}`,
        { width: (width * 1.18) / n, height: 0.34, depth: 0.44 },
        ctx.scene,
      );
      v.position.set(Math.sin(a) * R, height / 2 + Math.cos(a) * R - R + rise, -0.02);
      v.rotation.z = -a;
      v.material = mats.stone;
      v.parent = root;
      ctx.register(v, { collide: false, cast: true });
    }
  }

  // Bars: vertical primaries with two horizontal ties, as in the reference.
  const bar = MeshBuilder.CreateBox('bar', { width: 0.035, height, depth: 0.035 }, ctx.scene);
  bar.material = mats.metal;
  bar.parent = root;
  const total = bars + 2;
  const bm = new Float32Array(total * 16);
  for (let i = 0; i < bars; i++) {
    const x = -width / 2 + (width * (i + 1)) / (bars + 1);
    const o2 = i * 16;
    bm[o2] = bm[o2 + 5] = bm[o2 + 10] = bm[o2 + 15] = 1;
    bm[o2 + 12] = x;
    bm[o2 + 14] = 0.1;
  }
  // Two horizontals, expressed as a rotated+scaled instance.
  for (let j = 0; j < 2; j++) {
    const o2 = (bars + j) * 16;
    const s = width / height;
    bm[o2 + 0] = 0;
    bm[o2 + 1] = s;
    bm[o2 + 4] = -1;
    bm[o2 + 5] = 0;
    bm[o2 + 10] = 1;
    bm[o2 + 15] = 1;
    bm[o2 + 13] = -height / 4 + (j * height) / 2;
    bm[o2 + 14] = 0.1;
  }
  bar.thinInstanceSetBuffer('matrix', bm, 16);
  ctx.register(bar, { collide: false, cast: true });

  return root;
}

/* -------------------------------------------------------------------------- */
/*  Ground                                                                    */
/* -------------------------------------------------------------------------- */

/**
 * A ground plane with gentle noise displacement so it never reads as a
 * billiard table, plus a subdivision count tuned so the shadow cascades have
 * something to land on.
 */
export function buildGround(
  ctx: KitContext,
  material: PBRMaterial,
  o: { size?: number; subdivisions?: number; amplitude?: number; surface?: string } = {},
): Mesh {
  const { size = 160, subdivisions = 96, amplitude = 0.12, surface = 'gravel' } = o;
  const g = MeshBuilder.CreateGround(
    'ground',
    { width: size, height: size, subdivisions, updatable: true },
    ctx.scene,
  );
  const positions = g.getVerticesData('position');
  if (positions && amplitude > 0) {  // amplitude 0 keeps the clean flat plane
    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i];
      const z = positions[i + 2];
      positions[i + 1] =
        (Math.sin(x * 0.21) * Math.cos(z * 0.17) + Math.sin(x * 0.63 + z * 0.4) * 0.4) * amplitude;
    }
    g.updateVerticesData('position', positions);
    VertexData.ComputeNormals(
      positions,
      g.getIndices()!,
      g.getVerticesData('normal')!,
    );
    g.updateVerticesData('normal', g.getVerticesData('normal')!);
  }
  g.material = material;
  ctx.register(g, { collide: true, cast: false, surface });
  return g;
}

export { Vector4 };
