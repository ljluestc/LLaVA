PR Description — Issue #271: Use Stage-1 Pretrained Model for Inference

Summary
This PR adds support for running inference directly with stage-1 pretrained checkpoints (feature alignment stage) in LLaVA, primarily for debugging, ablation studies, and early pipeline validation.
Closes #271.

Background
Issue #271 asks whether the stage-1 pretrained model can be used for inference. Stage-1 checkpoints are usually used as an intermediate training artifact and may not have fully instruction-tuned conversational quality, but they are still useful for validating end-to-end serving setup, inspecting multimodal alignment behavior, and running controlled experiments before stage-2 tuning.

Problem Statement
Current inference workflows and documentation focus on stage-2 or final checkpoints. As a result, users trying to load stage-1 artifacts may face unclear configuration, missing guardrails, or confusing runtime errors.

Goals
Enable inference execution with stage-1 checkpoints.
Keep existing stage-2 inference behavior unchanged.
Provide clear messaging about expected capability and quality limitations.
Document how to opt in explicitly to stage-1 inference mode.

Non-Goals
Improving stage-1 conversational quality to match stage-2 instruction tuning.
Redesigning all checkpoint loading flows.
Changing defaults away from stage-2 or final checkpoints.

Proposed Changes
Checkpoint loading compatibility:
Extend model loading path to accept stage-1 checkpoint metadata or config shape where needed.
Ensure tokenizer and vision-language connector components initialize consistently.

Inference path enablement:
Allow stage-1 checkpoints through inference entry points with explicit opt-in behavior.
Add user-facing warnings or notes indicating expected response quality differences.

Validation and safeguards:
Add sanity checks for missing stage-2-specific artifacts and provide actionable error messages.
Preserve strict behavior for unsupported checkpoint combinations.

Documentation:
Add usage examples for stage-1 inference invocation.
Document limitations and recommended use cases such as debugging and analysis rather than production chat quality.

Compatibility and Risk
Backward compatibility: Stage-2 inference remains default and unaffected.
Risk: Users may expect stage-2 quality from stage-1 checkpoints.
Mitigation: Explicit warnings, documentation clarifications, and opt-in flags.

Testing Plan
Loader-level checks for stage-1 checkpoint acceptance.
Inference smoke tests using representative stage-1 checkpoints.
Regression tests to verify stage-2 checkpoints still load and run unchanged.

Manual Verification
Launch inference with a stage-1 checkpoint configuration.
Run an image plus text prompt and verify the model responds without loading or runtime failures.
Confirm warning or help text appears when stage-1 mode is used.

Rollout Plan
Merge as opt-in support.
Publish notes in docs or changelog.
Gather feedback on additional stage-1 checkpoint variants encountered by users.

Checklist
Full local PR description drafted.
Implementation details to be attached in code-change PR.
Test outputs or logs to be added once implementation is complete.

Notes
This change is about capability enablement and developer ergonomics for experimentation; it does not claim parity between stage-1 and stage-2 instruction-following quality.
