import {existsSync} from 'node:fs';
import {join} from 'node:path';
import {homedir} from 'node:os';
import {spawn} from 'node:child_process';
// Prefer the bundled runtime on this machine: Node 24.13 can abort on Windows
// while Vinext shuts down after prerendering; 24.19 completes normally.
const bundled=join(homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe');
const node=existsSync(bundled)?bundled:process.execPath;
const child=spawn(node,['node_modules/vinext/dist/cli.js',...process.argv.slice(2)],{stdio:'inherit'});
child.on('error',error=>{console.error(error.message);process.exitCode=1});
child.on('exit',code=>{process.exitCode=code??1});
