# Multicat

[![awesome plugin](https://custom-icon-badges.demolab.com/static/v1?label=&message=awesome+plugin&color=F4F4F5&style=for-the-badge&logo=cheshire_cat_black)](https://)

## Multicat Plugin for Cheshire Cat

Transform Cheshire Cat into a complete multi-cat framework.

Multicat extends the Cheshire Cat AI framework with native multichat and multiagent capabilities, enabling simultaneous independent conversations, file management per chat session, and the creation of custom agents.

By default declarative memory and episodic are separated for users.

**All without needing to modify the core project.**

### Key Features

- **Multi-chat**: Manage multiple conversations simultaneously, keeping them completely separate
- **Multi-agent**: Create and customize different agents with specific personalities (currently only via prompts)
- **Conversation caching**: Automatic saving of conversations to continue at any time
- **Complete API**: Dedicated endpoints for integration with other applications
- **File management per chat**: Associate and organize specific documents for each conversation

### Enhance Your Cheshire Cat with Native Multichat Support

## Quick Start

### Installation

1. Install the MultiCat plugin from the registry (within the admin panel)
2. Activate the plugin from settings
3. **Restart your Cheshire Cat instance**

Now MultiCat will be loaded with Cheshire Cat and automatically start working.

## Django Integration

For a ready-to-use chat interface with multichat support, use our companion Django project:  
[DjangoMultiCat Repository](https://github.com/davidebizzocchi/DjangoMultiCat)

Key features of the Django interface:

- Intuitive chat management
- Visual organization of files for each conversation
- Easy integration with existing Cheshire Cat instances
- Responsive and customizable user interface

### Usage

#### Basic Usage

Once installed, you can:

- When send a message specify a `chat_id`, the plugin will automatically create a new SonStrayCat and start a new chat.
- When response the CatMessage contains the `chat_id`

#### Working with Files and Metadata

##### Uploading Files with Metadata

Upload a file to the RabbitHole with specific metadata:

```python
# Python example
metadata = {
    "file_id": "unique_file_id",  # Unique identifier for your file
    "chats_id": ["chat1", "chat2"],  # Associate with specific chats
    "custom_field": "custom value"  # Any custom metadata
}

# Using requests
import requests
files = {"file": open("document.pdf", "rb")}
payload = {"metadata": json.dumps(metadata)}
response = requests.post(
    "http://localhost:1865/rabbithole/",
    files=files,
    data=payload,
    headers={"user_id": "your_user_id"}
)
```

##### Associating Files with Chats

Associate existing files with chats:

```python
# Add file to chats
response = requests.patch(
    "http://localhost:1865/memory/collections/declarative/points/edit_chat_ids?mode=add",
    json={
        "search_metadata": {"file_id": "unique_file_id"},
        "chats_id": ["chat3", "chat4"]
    },
    headers={"user_id": "your_user_id"}
)

# Remove file from chats
response = requests.patch(
    "http://localhost:1865/memory/collections/declarative/points/edit_chat_ids?mode=remove",
    json={
        "search_metadata": {"file_id": "unique_file_id"},
        "chats_id": ["chat1"]
    },
    headers={"user_id": "your_user_id"}
)
```

##### Updating File Metadata

Update metadata for existing files:

```python
response = requests.patch(
    "http://localhost:1865/memory/collections/declarative/points/metadata",
    json={
        "search": {"file_id": "unique_file_id"},
        "update": {"new_field": "new_value"}
    },
    headers={"user_id": "your_user_id"}
)
```

##### Retrieving File Information

Get file metadata:

```python
response = requests.get(
    "http://localhost:1865/memory/collections/declarative/points/by_metadata",
    params={"metadata": json.dumps({"file_id": "unique_file_id"})},
    headers={"user_id": "your_user_id"}
)
```

#### Using with Django Integration

When using with DjangoMultiCat, file management is simplified:

```python
from cheshire_cat.client import connect_user

cat = connect_user("user_id")

# Upload file
cat.upload_file(file_object, metadata={"file_id": "unique_id"})

# Associate file with chats
cat.add_file_to_chats(file_id, ["chat1", "chat2"])

# Get file metadata
file_data = cat.get_file_metadata(file_id)
```

## Roadmap

- [x] Multi-chat agent
- [x] File-chat association: RabbitHole + endpoints
- [x] Multi-agent: prompt hook + endpoints + stored
- [x] Web interface integration
- [x] Re-build conversation: endpoint
- [x] Cache: SonStrayCat
- [ ] Capabilities for agents: plugins, vector search, ...
- [ ] Custom tool creation

## Contributions

Contributions and feedback are welcome! Open an issue or a pull request on the repository.
