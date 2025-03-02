from cat.mad_hatter.decorators import hook
from langchain.docstore.document import Document

from cat.looking_glass.cheshire_cat import CheshireCat
from cat.looking_glass import prompts

from cat.plugins.multicat.types import Agent
from cat.plugins.multicat.refactory.stray_cat.son import SonStrayCat

from cat.log import log


@hook()
def before_cat_stores_episodic_memory(doc: Document, cat):
    doc.metadata["chat_id"] = cat.chat_id

    return doc

@hook()
def before_cat_recalls_episodic_memories(episodic_recall_config: dict, cat) -> dict:
    if not episodic_recall_config.get("metadata"):
        episodic_recall_config["metadata"] = {}

    episodic_recall_config["metadata"]["chat_id"] = cat.chat_id

    return episodic_recall_config

@hook()
def before_rabbithole_insert_memory(doc: Document, cat):
    doc.metadata["user_id"] = cat.user_id

    return doc

@hook()
def before_cat_recalls_declarative_memories(declarative_recall_config: dict, cat) -> dict:
    if not declarative_recall_config.get("metadata"):
        declarative_recall_config["metadata"] = {}

    declarative_recall_config["metadata"]["user_id"] = cat.user_id

    return declarative_recall_config

@hook()
def after_cat_bootstrap(cat: CheshireCat):
    cat.agents = {}  # [str, Agent] Agent in multicat.types

    cat.agents["default"] = Agent(
        id="default",
        _class=type(cat.main_agent),
        name="Main Agent",
        instructions=prompts.MAIN_PROMPT_PREFIX,
        metadata={}
    )

@hook(priority=0)
def agent_prompt_prefix(prefix, cat):
    if isinstance(cat, SonStrayCat):
        return  cat.get_instructions() or prefix
    
    return prefix
