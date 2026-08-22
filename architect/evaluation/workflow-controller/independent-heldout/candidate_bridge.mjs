import fs from 'node:fs';
import { pathToFileURL } from 'node:url';

const modulePath = process.argv[2];
if (!modulePath) {
  console.error('candidate module path required');
  process.exit(2);
}

const candidate = await import(pathToFileURL(modulePath).href);
const input = JSON.parse(fs.readFileSync(0, 'utf8'));

function invoke(op) {
  const a = op.args ?? {};
  switch (op.fn) {
    case 'expectedOwner': return candidate.expectedOwner(a.state, a.blockerOwner ?? null);
    case 'canTransition': return candidate.canTransition(a.from, a.to, a.options ?? {});
    case 'validateRevision': return candidate.validateRevision(a.expectedRevision, a.submittedRevision);
    case 'validateTaskAuthority': return candidate.validateTaskAuthority(a.actor, a.taskType, a.options ?? {});
    case 'retryDirective': return candidate.retryDirective(a.errorClass, a.attempt);
    case 'requiresReconciliation': return candidate.requiresReconciliation(a.taskType, a.outcomeKnown);
    case 'validateApproval': return candidate.validateApproval(a.payload);
    case 'validateArtifactJoin': return candidate.validateArtifactJoin(a.refs);
    case 'routeInquiry': return candidate.routeInquiry(a.payload);
    case 'unknownExceptionDirective': return candidate.unknownExceptionDirective();
    default: throw new Error(`unknown fn: ${op.fn}`);
  }
}

const out = input.map((op, index) => {
  try {
    return { index, ok: true, value: invoke(op) };
  } catch (error) {
    return { index, ok: false, error: String(error?.message ?? error) };
  }
});

process.stdout.write(JSON.stringify(out));
