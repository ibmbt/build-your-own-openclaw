"""Built-in slash command handlers."""

from typing import TYPE_CHECKING

from mybot.core.commands.base import Command
from mybot.utils.def_loader import DefNotFoundError

if TYPE_CHECKING:
    from mybot.core.agent import AgentSession


class SessionCommand(Command):
    """Show current session details."""

    name = "session"
    description = "Show current session details"

    async def execute(self, args: str, session: "AgentSession") -> str:
        info = session.agent.history_store.get_session_info(session.session_id)

        # Handle case where session not found in index
        created_str = info.created_at if info else "Unknown"

        lines = [
            f"**Session ID:** `{session.session_id}`",
            f"**Agent:** {session.agent.agent_def.name} (`{session.agent.agent_def.id}`)",
            f"**Created:** {created_str}",
            f"**Messages:** {len(session.state.messages)}",
        ]
        return "\n".join(lines)


class HelpCommand(Command):
    """Show available commands."""

    name = "help"
    aliases = ["?"]
    description = "Show available commands"

    async def execute(self, args: str, session: "AgentSession") -> str:
        lines = ["**Available Commands:**"]
        for cmd in session.command_registry.list_commands():
            names = [f"/{cmd.name}"] + [f"/{a}" for a in cmd.aliases]
            lines.append(f"{', '.join(names)} - {cmd.description}")
        return "\n".join(lines)


class SkillsCommand(Command):
    """List all skills or show skill details."""

    name = "skills"
    description = "List all skills or show skill details"

    async def execute(self, args: str, session: "AgentSession") -> str:
        if not args:
            skills = session.agent.skill_loader.discover_skills()
            if not skills:
                return "No skills configured."

            lines = ["**Skills:**"]
            for skill in skills:
                lines.append(f"- `{skill.id}`: {skill.description}")
            return "\n".join(lines)

        # Show specific skill details
        skill_id = args.strip()
        try:
            skill = session.agent.skill_loader.load_skill(skill_id)
        except DefNotFoundError:
            return f"✗ Skill `{skill_id}` not found."

        lines = [
            f"**Skill:** `{skill.id}`",
            f"**Name:** {skill.name}",
            f"**Description:** {skill.description}",
            f"\n---\n\n**SKILL.md:**\n```\n{skill.content}\n```",
        ]
        return "\n".join(lines)


class EchoCommand(Command):
    """Echo back the text provided by the user."""

    name = "echo"
    aliases = ["e", "repeat"]
    description = "Repeats exactly what you type after the command"

    async def execute(self, args: str, session: "AgentSession") -> str:
        if not args.strip():
            return "You didn't give me anything to echo!"
        return args