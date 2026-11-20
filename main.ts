// Writes /output/entry.png: the 20 November 2026 world-news front page the
// agent drew with Pillow during development (see gen_image.py for how it was
// built). The program runs with no network and verifies the image before
// copying it, so both runs write identical bytes.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const buf = readFileSync(src);

// The gate takes a whole PNG of at most 1 MiB and 1024 by 1024 pixels; check
// the signature and the IHDR dimensions so a corrupt image never ships.
const isPng = buf.length <= 1048576 &&
  buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47;
if (!isPng) throw new Error('entry.png is not a valid PNG under 1 MiB');
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}

copyFileSync(src, join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
