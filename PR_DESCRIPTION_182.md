# PR Description — Issue #182: Support RedPajama Models

## Summary
This PR adds support for RedPajama model families in LLaVA, with a focus on enabling lightweight deployments (for example, 3B-class checkpoints) while preserving the existing loading, serving, and multimodal interaction workflows.

Closes #182.

## Problem Statement
Issue #182 requests RedPajama support so users can run faster and more resource-efficient models. Today, users who want to use RedPajama checkpoints must patch model registration/loading code manually, which creates friction and inconsistent behavior across environments.

## Goals
- Add first-class RedPajama model support in model registration and loading paths.
- Keep current behavior unchanged for already-supported backbones.
- Ensure inference and conversation formatting remain stable for multimodal chat usage.
- Provide clear configuration and usage documentation.

## Non-Goals
- Reworking unrelated model backbones.
- Large-scale performance optimization beyond compatibility enablement.
- Changing default model choices for existing users.

## Proposed Changes
1. **Model registration**
   - Add RedPajama model identifiers/aliases to the model mapping layer.
   - Ensure checkpoint path resolution works consistently with existing conventions.

2. **Model loading integration**
   - Wire RedPajama backbone selection through model builder/loader code paths.
   - Validate tokenizer/model initialization compatibility with existing runtime flags.

3. **Conversation/inference compatibility**
   - Verify generation settings and prompt formatting remain compatible.
   - Preserve backward-compatible defaults for non-RedPajama models.

4. **Documentation**
   - Add usage notes for selecting RedPajama models in training/inference entry points.
   - Document any known constraints and recommended minimum hardware settings.

## Compatibility & Risk
- **Backward compatibility**: Existing model families should behave unchanged.
- **Primary risk**: Configuration drift or naming mismatch in model aliases.
- **Mitigation**: Add explicit mapping coverage and validation checks in loader paths.

## Testing Plan
- Unit/integration checks for:
  - RedPajama model registration and alias resolution.
  - Successful model/tokenizer initialization for supported checkpoints.
  - Basic inference path sanity (single-turn and multi-turn conversation).
- Regression checks to confirm existing backbones are unaffected.

## Manual Verification
- Launch inference with a RedPajama-backed configuration.
- Run a simple multimodal prompt and confirm successful generation.
- Compare behavior against an existing supported backbone for baseline sanity.

## Rollout Plan
- Merge behind normal model-selection configuration.
- Publish release notes/doc updates indicating RedPajama support.
- Collect early user feedback for additional checkpoint variants.

## Checklist
- [x] Full PR description drafted locally.
- [ ] Implementation details to be finalized during code changes.
- [ ] Validation logs/screenshots to be attached in the actual implementation PR.

## Notes
The originating request emphasized support for lightweight RedPajama variants (including 3B-scale models) to improve speed and accessibility for resource-constrained environments.
