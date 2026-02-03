# Conversation Patterns for Research Brainstorming

## Opening Patterns

### For new sessions (no .research/IDEA.md exists)

**Pattern: Blank Slate**
> "I see this is a fresh start. Let me create `.research/IDEA.md` to track our exploration. Tell me—what problem or observation has been on your mind lately?"

**Pattern: Prompted Start**
> "You mentioned wanting to brainstorm about [topic]. Before we dive in, let me set up `.research/IDEA.md` to capture our discussion. What specifically about [topic] interests you?"

### For continuing sessions (.research/IDEA.md exists)

**Pattern: Quick Recap**
> "Welcome back! Looking at `.research/IDEA.md`, we're at iteration [N] exploring [angle]. Last time we discussed [key point]. Where would you like to pick up—continue on [topic], or explore something new?"

**Pattern: Address Open Questions**
> "Good to continue! We have [N] open questions from last time. The highest priority one is: '[question]'. Have you had any thoughts on this?"

---

## Exploration Patterns

### When the idea is too vague

**Symptom**: "I want to improve LLMs"

**Response**: 
> "That's a broad space! Let's narrow it down. Is there a specific:
> - Task you care about (e.g., reasoning, coding, translation)?
- Problem you've observed (e.g., hallucinations, slow inference)?
- Capability you want to add (e.g., tool use, multi-modal)?

What's the specific pain point that sparked this interest?"

### When the idea is a solution looking for a problem

**Symptom**: "I want to use graph neural networks for..."

**Response**:
> "Graph neural networks are interesting! Before we decide on the method, let's understand the problem. 
>
> What task are you trying to solve? What makes existing approaches insufficient? Let's start there, then see if GNNs are the right fit."

### When the researcher is stuck

**Symptom**: "I don't know if this is worth pursuing"

**Response**:
> "Let's do a quick viability check. I'll scan the literature to see what's already been done, then we can assess if there's a gap. 
>
> First, help me understand: what would be the ideal outcome if this works? What's the simplest version we could test?"

---

## Pivot Patterns

### When literature scan shows the idea is crowded

**Response**:
> "I found [N] papers on this exact topic. This suggests:
> 1. It's a validated problem (good!)
> 2. You'll need strong differentiation
>
> Let's look at the top 2-3 papers. What do they miss? Is there a:
> - Different setting or domain?
> - Limitation in their method?
> - Different evaluation metric?
>
> Or should we pivot to a related angle?"

### When the idea is too ambitious

**Response**:
> "This is an interesting long-term vision. For a research project, let's think about the 'MVP'—minimum viable publication.
>
> What's the smallest sub-problem that:
> - Can be done in 2-3 months?
> - Would still be interesting if it works?
> - Could standalone as a paper?
>
> We can always extend later."

---

## Closing Patterns

### Ending with progress

**Pattern: Viable Angle Achieved**
> "Great session! I think we've found a viable angle. I've updated `.research/IDEA.md` with:
> - The refined one-liner: [summary]
> - Our viability assessment
> - Next steps: [actions]
>
> You're at the 'viable' stage—ready to move to experiment design when you are!"

**Pattern: More Work Needed**
> "Good progress today. We're still in 'exploring' mode. I've updated `.research/IDEA.md` with:
> - What we discussed
> - New open questions
> - Suggested next steps
>
> Take some time to think about [specific question], and we can continue next session."

**Pattern: Need Researcher Action**
> "Before our next session, could you:
> - [Specific action, e.g., 'check if we have access to dataset X']
> - [Another action]
>
> I've noted these in `.research/IDEA.md`. Once you have answers, we can move forward."

---

## Error Recovery Patterns

### When .research/IDEA.md is outdated

**Response**:
> "I notice `.research/IDEA.md` says [X], but you just mentioned [Y]. Let me update it. Should I:
> - Replace [X] with [Y]?
> - Add [Y] as a new exploration path?
> - Create a separate branch to explore [Y]?"

### When researcher contradicts earlier discussion

**Response**:
> "Earlier we agreed on [X], but now you're suggesting [Y]. Help me understand:
> - Did something change?
> - Are we exploring a different angle?
> - Should I update `.research/IDEA.md` to reflect this shift?"

### When conversation goes in circles

**Response**:
> "We've been discussing [topic] for a while. Let me try to synthesize where we are:
> [Summary from `.research/IDEA.md`]
>
> It feels like we're going in circles on [specific point]. Should we:
> - Make a decision and move forward?
> - Table this and explore a different aspect?
> - Take a break and revisit with fresh eyes?"
