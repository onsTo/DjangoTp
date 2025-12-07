# mcp_server.py
import os
import django
from mcp.server.fastmcp import FastMCP
from asgiref.sync import sync_to_async

# -----------------------------------------------------
# Configuration Django
# -----------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GestionConference.settings")
django.setup()

# Importer les modèles après setup()
from ConferenceApp.models import Conference
from SessionApp.models import Session

# -----------------------------------------------------
# Création du serveur MCP (global)
# -----------------------------------------------------
mcp = FastMCP("Conference Assistant")


# =====================================================
# Tool 1 : Lister toutes les conférences
# =====================================================
@mcp.tool()
async def list_conferences() -> str:
    """List all conferences"""

    @sync_to_async
    def _get_conferences():
        return list(Conference.objects.all())

    conferences = await _get_conferences()

    if not conferences:
        return "No conferences found."

    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date})"
        for c in conferences
    ])


# =====================================================
# Tool 2 : Obtenir les détails d’une conférence
# =====================================================
@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Get details of a specific conference"""

    @sync_to_async
    def _get_conf():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"

    c = await _get_conf()

    if c == "MULTIPLE":
        return f"Multiple conferences match '{name}'. Please be more specific."
    if not c:
        return f"Conference '{name}' not found."

    return (
        f"Name: {c.name}\n"
        f"Theme: {c.get_theme_display()}\n"
        f"Location: {c.location}\n"
        f"Dates: {c.start_date} to {c.end_date}\n"
        f"Description: {c.description}"
    )


# =====================================================
# Tool 3 : Lister les sessions d’une conférence
# =====================================================
@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """List all sessions for a given conference"""

    @sync_to_async
    def _get_sessions():
        try:
            conf = Conference.objects.get(name__icontains=conference_name)
            return list(conf.sessions.all()), conf
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None

    sessions, conf = await _get_sessions()

    if sessions == "MULTIPLE":
        return f"Multiple conferences match '{conference_name}'. Please be more specific."
    if conf is None:
        return f"Conference '{conference_name}' not found."
    if not sessions:
        return f"No sessions found for '{conf.name}'."

    return "\n".join([
        f"- {s.title} ({s.start_time} → {s.end_time}) – Room {s.room}\nTopic: {s.topic}"
        for s in sessions
    ])


# =====================================================
# Tool 4 : Filtrer les conférences par thème (tool libre)
# =====================================================
@mcp.tool()
async def filter_conferences_by_theme(theme: str) -> str:
    """Filter conferences by theme"""

    @sync_to_async
    def _filter():
        return list(Conference.objects.filter(theme=theme))

    conferences = await _filter()

    if not conferences:
        return f"No conferences found for theme '{theme}'."

    return "\n".join([f"- {c.name}" for c in conferences])


# =====================================================
# Lancement du serveur MCP
# =====================================================
if __name__ == "__main__":
    mcp.run(transport="stdio")
