"""In-memory model of the slice of Risu state that Lua scripts can observe.

This is intentionally small for M1; M2 fills out lorebooks, modules, persona
images, request mocking, etc. The shape mirrors what the host API in
scriptings.ts reads/writes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class Message:
    role: str  # 'user' | 'char'
    data: str
    time: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {"role": self.role, "data": self.data, "time": self.time}


@dataclass
class RisuState:
    # Chat
    messages: List[Message] = field(default_factory=list)
    chat_vars: Dict[str, str] = field(default_factory=dict)
    global_vars: Dict[str, str] = field(default_factory=dict)
    note: str = ""  # authors note

    # Character (selected)
    char_name: str = "Risu"
    char_desc: str = ""
    char_first_message: str = ""
    background_html: str = ""

    # Persona
    persona_name: str = "User"
    persona_desc: str = ""

    # Lorebooks (searched by getLoreBooks; upsertLocalLoreBook writes local_lore)
    local_lore: List[Dict[str, Any]] = field(default_factory=list)
    global_lore: List[Dict[str, Any]] = field(default_factory=list)
    module_lore: List[Dict[str, Any]] = field(default_factory=list)

    # Image inlays returned by the image host calls (mockable)
    char_image_inlay: str = ""
    persona_image_inlay: str = ""

    # --- Observability (filled during a run) ---
    logs: List[Any] = field(default_factory=list)
    alerts: List[Dict[str, Any]] = field(default_factory=list)
    llm_calls: List[Dict[str, Any]] = field(default_factory=list)
    request_calls: List[str] = field(default_factory=list)
    image_calls: List[Dict[str, Any]] = field(default_factory=list)
    reload_display_count: int = 0
    reloaded_chats: List[int] = field(default_factory=list)
    last_error: Optional[str] = None

    # --- Mocks for external/non-deterministic host calls ---
    # Either a dict (returned as-is) or a callable(prompt_json, kind) -> dict.
    mock_llm: Any = field(
        default_factory=lambda: {"success": True, "result": "MOCKED"}
    )
    # request(url): callable(url)->{status,data}, a url->response dict, or a
    # single {status,data} default applied to every URL.
    mock_http: Any = field(default_factory=lambda: {"status": 404, "data": ""})
    # similarity(source, values): callable(source, values)->list, a fixed list,
    # or None to echo the input values back.
    mock_similarity: Any = None
    mock_image: str = "{{inlay::mock-image}}"
    mock_loaded_lorebooks: List[Dict[str, Any]] = field(default_factory=list)

    # Queues consumed by alertInput / alertSelect / alertConfirm in order.
    input_responses: List[str] = field(default_factory=list)
    select_responses: List[int] = field(default_factory=list)
    confirm_responses: List[bool] = field(default_factory=list)

    def seed_messages(self, pairs: List[tuple]) -> "RisuState":
        """Convenience: seed_messages([('user','hi'), ('char','hello')])."""
        for role, data in pairs:
            self.messages.append(Message(role=role, data=data))
        return self
