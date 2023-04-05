# tree-of-thought
LLM-powered autonomous agent with hierarchical task management

### Motivation
The goal with Tree of Thought is to get as close to AGI as possible with existing base models. We believe that AGI is likely to be first achieved by scaling inference compute with sub-AGI models. We think one of the more productive ways to scale inference compute with LLMs is to call an LLM in a loop, while giving it a persistent state.

While we don’t believe we’re quite going to achieve AGI by building an autonomous agent system powered by GPT-4, we do think we can get quite close. GPT-4 seems to be the first LLM with sufficient context window and reasoning ability for this kind of autonomous agent to be possible.

We think that an autonomous agent with roughly human-level intelligence is the safest form of AGI that could be built, because each reasoning step it takes can be understood by a human. We think it’s best to start building and studying these systems now, while human-level LLMs (GPT-4) are still slow and expensive.

### How the task tree works
LLMs don’t have built-in memory; they only have access to what you give them in their prompt. That means that the core challenge in building an autonomous agent is getting the right information into the prompt at the right time. A dynamic tree structure is a natural way to organize tasks. Most tasks that we, as humans, perform are in the service of some larger goal. We break down huge tasks, like building a successful company, into smaller and smaller subtasks until we get to the point where we can actually act on one of them. These tasks change over time as we receive new information.

The Tree of Thought, the task tree is initialized with a human-provided task description. This becomes the root task, and the agent is not allowed to edit this task. The agent can then choose to directly solve the task, or break it into an ordered list of subtasks. For a given task (i.e. objective) the agent can attempt it as many times as it wants, and the objective only changes when the agent either decides to break the task down, marks the task as complete, or edits the task tree such that there is either a new preceding task or a new parent task.

### Prompt, parser, and operating system
The agent has three components: prompt, parser, and operating system. It runs continuously, with each agent response informing its next prompt to enable continuity of state.

Prompt
- Objective
- Context
- Actions

Parser
- Parses the agent response and performs the requested action(s)

Operating system (keeps track of state)
- Determines what Objective, Context, and Actions go into the prompt
- This is done via a dynamic task tree

### Objective, Context, Actions (OCA)
Since LLMs are stateless, we have to provide sufficient information in the prompt to effectively give them a state. There are three main components needed: the Objective they should be focusing on, the Context they need to understand what’s going on, and the Actions they’re allowed to take.

This is what goes in the agent prompt:

Objective
- Task tree context
- Constitution

Context
- Conversation history
- Agent notes
- Agent action log

Actions
- Available actions, with their descriptions and formatting instructions
- Task tree management actions
  - Break task down
  - Mark task complete
  - Edit sibling tasks
  - Edit parent task

### ActionInterface and Action Sets
The actions that a Tree of Thought agent can take are defined by the Action Sets that are given to it. An Action Set is a set of Actions, where each action is a Python function along with some supporting documentation to tell the agent how and when to use it.

There is one default Action Set that can’t be removed, and that is the Task Tree Management Action Set. This contains the functions that let the agent manipulate its task tree, such as breaking a task into subtasks or marking a task as complete. Aside from this, you’re free to add as many additional Action Sets as you want, subject to context window constraints.

Our goal with this project is to make it really easy to create your own custom Action Sets. That’s the primary way you can customize Tree of Thought to work for your use case.

### Agent action log
The agent action log is an essential component of the prompt, because it’s what allows the agent to see the outcome of its actions and learn from its mistakes. We’ve observed an impressive ability for the agent to observe errors and then adjust its plans accordingly. Right now the action log just shows the 10 most recent actions, so there’s certainly room for improvement here by selecting a more relevant set of action logs to include in the prompt.

### Knowledge retrieval integrations
Most complex tasks require some sort of knowledge retrieval. This is supported in Tree of Thought by adding a knowledge retrieval action.

### Human guidance and interaction
While the goal of building this system is to build a highly autonomous agent that doesn’t rely on human intervention, there are still many scenarios where having some human interaction with the agent can be desirable. For many writing or coding tasks, for example, it generally isn’t feasible to fully specify the objective at the beginning.

We haven’t implemented human interaction yet, but it’s at the top of the list and will be implemented soon.

### Agency and safety
Is this better for interpretability and safety than just using a huge model and doing a handful of agent loop steps? We think so. Each time the agent completes a complex task, we get a detailed log of all the steps it took, including its reasoning for why it did what it did.

Would an LLM system following a task tree, as described above, be an autonomous agent in the AI safety sense of the term? Would it be goal-directed? Yes, it would be trying to achieve its root goal at the top of the task tree. But it would be doing so by trying to emulate human thinking and behavior, since that’s the training objective for LLMs. If we trained an agent with RL to optimally traverse the task tree and perform actions, then that would be more agentic and potentially more dangerous. This task tree could also be used to build more of a genie or an oracle than an agent. All three forms of AI systems benefit from the ability to break things up into small connected pieces.

### Limitations
- No context window management, meaning there’s nothing to stop the prompt from exceeding the 8k token limit
- No long-term memory
- GPT-4 is pretty slow and expensive, and we haven’t been able to get it to work well with any other models yet (although it’s probably possible)
- Limited functionality with default Action Sets
