import {existsSync} from 'node:fs';
import {join} from 'node:path';
import {homedir} from 'node:os';
import {spawnSync} from 'node:child_process';
const bundled=join(homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe');
const python=process.env.ACADEMIC_PYTHON || (existsSync(bundled)?bundled:'python');
const result=spawnSync(python,['scripts/build_content.py'],{stdio:'inherit'});
if(result.error){console.error('Set ACADEMIC_PYTHON to a Python installation with requirements.txt installed.');console.error(result.error.message)}
process.exit(result.status??1);
