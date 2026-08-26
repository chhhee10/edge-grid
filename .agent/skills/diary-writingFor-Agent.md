Create a comprehensive end-of-day engineering diary/report based on the complete chat history, code changes, decisions, debugging sessions, and task execution performed today.

The diary should be written so that:
1. Any future coding agent can immediately continue the work without losing context.
2. I can quickly understand everything completed, blocked, pending, and learned today.
3. It improves future development speed, debugging efficiency, and collaboration quality.

The report must be highly structured, detailed, and technically precise.

Include the following sections:

# 1. Executive Summary
- High-level overview of the day
- Main objectives worked on
- Major accomplishments
- Overall project status

# 2. Tasks Completed
For every completed task include:
- Task title
- Purpose of the task
- Files/modules/components affected
- What was changed
- Why the change was needed
- Important implementation details
- Dependencies introduced/removed
- Commands executed
- Final outcome

# 3. Issues & Debugging Log
For every issue encountered:
- Exact error/problem
- Root cause analysis
- How the issue was identified
- Debugging steps attempted
- Failed approaches tried before the solution
- Final fix applied
- Why the fix worked
- Preventive measures for the future
- Logs/error messages if relevant

# 4. Pending Work / Incomplete Tasks
Clearly list:
- What is unfinished
- Current progress status
- Blocking issues
- What should be done next
- Recommended order of execution
- Risks or dependencies

# 5. Architecture / Technical Decisions
Document all important decisions:
- Why a particular approach was chosen
- Alternatives considered
- Tradeoffs
- Long-term implications
- Performance/security/scalability considerations

# 6. Code Intelligence Notes
Generate future-facing notes that help both humans and coding agents:
- Important patterns used
- Reusable utilities/functions created
- Naming conventions
- Folder structure insights
- Hidden assumptions
- Environment setup requirements
- Important configs
- Common pitfalls
- Areas that are fragile or tightly coupled
- Technical debt introduced
- Refactor recommendations

# 7. Efficiency Improvements
Based on today's work, identify:
- Repetitive tasks that should be automated
- Better workflows
- Faster debugging approaches
- Missing scripts/tools
- Recommended IDE/plugins/extensions
- Better prompts or agent instructions
- Knowledge that should be documented permanently
- Opportunities for reusable templates/components

# 8. Agent Collaboration Context
Generate context specifically useful for future AI coding agents:
- Current mental model of the project
- Active objectives
- Important project constraints
- Existing assumptions
- APIs/services currently in use
- Expected coding style
- Important recent changes
- Files that must be read first before editing
- Unsafe areas where changes may break functionality
- Recommended next prompts for future agents

# 9. Important Commands & References
Include:
- Commands executed today
- Build/test/deploy commands
- URLs/repositories/docs referenced
- Environment variables/configuration used
- Database/API references

# 10. Learning & Insights
Summarize:
- Key technical learnings
- Mistakes avoided
- Better approaches discovered
- Unexpected behavior observed
- Best practices identified

# 11. Suggested Next Session Plan
Create a prioritized action plan for the next work session:
- Immediate next steps
- Recommended execution order
- Estimated complexity
- Dependencies
- Quick wins first

Formatting Requirements:
- Use clean markdown
- Use tables where useful
- Use bullet points for readability
- Include code snippets where relevant
- Be concise but highly informative
- Prefer actionable insights over generic summaries
- Preserve technical precision
- Infer missing context intelligently from the full chat history and work performed

Critical Instruction:
Do NOT generate a shallow summary.
Generate a true engineering memory system that acts as:
- a development journal,
- debugging archive,
- project continuation guide,
- and operational intelligence layer for future coding agents and humans.