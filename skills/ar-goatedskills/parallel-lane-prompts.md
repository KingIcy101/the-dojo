# Parallel Lane Prompt Skeletons

Use these as starting prompts for sub-agents.

## Lane A: Research Track A
`@research Run deep comparative research across OPTIONS against CRITERIA. Prioritize current evidence and clear assumptions. Return output schema: summary, changes, commands, verification, risks/blockers, nextAction.`

## Lane B: Research Track B (Independent)
`@research Run an independent comparative analysis over the same OPTIONS and CRITERIA using a different reasoning path. Focus on contradiction finding and alternative conclusions. Return output schema: summary, changes, commands, verification, risks/blockers, nextAction.`

## Lane C: Quant Synthesis
`@analyze Build weighted decision matrix, Base/Growth/Stress TCO, and sensitivity analysis from Lane A and B outputs. Show score deltas and break-even thresholds. Output schema: summary, changes, commands, verification, risks/blockers, nextAction.`

## Lane D: QA/Contradiction
`@qa Audit lane outputs for unsupported claims, stale sources, and contradictory findings. Produce confirmed/disputed/weak claim labels and unresolved unknowns. Output schema: summary, changes, commands, verification, risks/blockers, nextAction.`

## Future Add-on Lane (Not default)
`@research Use provider-native Deep Research mode (OpenAI/Gemini) only when explicitly enabled for this run and account/tooling access is confirmed.`
